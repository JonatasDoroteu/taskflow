from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Board, Column, Task


# ── HELPERS ─────────────────────────────────────────────────────────────────

def make_user(username='jonatas', password='senha123'):
    return User.objects.create_user(username=username, password=password)

def get_token(client, username='jonatas', password='senha123'):
    res = client.post('/api/token/', {'username': username, 'password': password}, format='json')
    return res.data['access']

def auth(client, token):
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')


# ── AUTENTICAÇÃO ─────────────────────────────────────────────────────────────

class RegisterTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_cadastro_com_dados_validos(self):
        res = self.client.post('/api/register/', {
            'username': 'novo', 'email': 'novo@email.com', 'password': 'senha123'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_cadastro_sem_senha_falha(self):
        res = self.client.post('/api/register/', {
            'username': 'novo'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cadastro_username_duplicado_falha(self):
        make_user('duplicado')
        res = self.client.post('/api/register/', {
            'username': 'duplicado', 'password': 'senha123'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class TokenTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        make_user()

    def test_login_retorna_tokens(self):
        res = self.client.post('/api/token/', {
            'username': 'jonatas', 'password': 'senha123'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('access', res.data)
        self.assertIn('refresh', res.data)

    def test_login_senha_errada_falha(self):
        res = self.client.post('/api/token/', {
            'username': 'jonatas', 'password': 'errada'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token(self):
        res = self.client.post('/api/token/', {
            'username': 'jonatas', 'password': 'senha123'
        }, format='json')
        refresh = res.data['refresh']
        res2 = self.client.post('/api/token/refresh/', {'refresh': refresh}, format='json')
        self.assertEqual(res2.status_code, status.HTTP_200_OK)
        self.assertIn('access', res2.data)


# ── BOARDS ───────────────────────────────────────────────────────────────────

class BoardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.other = make_user('outro', 'senha123')
        token = get_token(self.client)
        auth(self.client, token)

    def test_criar_board(self):
        res = self.client.post('/api/boards/', {'title': 'Meu Board'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], 'Meu Board')

    def test_listar_boards_proprios(self):
        Board.objects.create(title='B1', owner=self.user)
        Board.objects.create(title='B2', owner=self.other)
        res = self.client.get('/api/boards/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], 'B1')

    def test_criar_board_sem_titulo_falha(self):
        res = self.client.post('/api/boards/', {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_deletar_board_proprio(self):
        board = Board.objects.create(title='Deletar', owner=self.user)
        res = self.client.delete(f'/api/boards/{board.id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_nao_acessa_board_de_outro_usuario(self):
        board = Board.objects.create(title='Alheio', owner=self.other)
        res = self.client.get(f'/api/boards/{board.id}/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_sem_autenticacao_nao_acessa_boards(self):
        self.client.credentials()
        res = self.client.get('/api/boards/')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


# ── COLUMNS ──────────────────────────────────────────────────────────────────

class ColumnTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.other = make_user('outro', 'senha123')
        token = get_token(self.client)
        auth(self.client, token)
        self.board = Board.objects.create(title='Board', owner=self.user)

    def test_criar_coluna(self):
        res = self.client.post(f'/api/boards/{self.board.id}/columns/', {
            'title': 'A Fazer'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], 'A Fazer')

    def test_listar_colunas(self):
        Column.objects.create(title='Col1', board=self.board, order=0)
        Column.objects.create(title='Col2', board=self.board, order=1)
        res = self.client.get(f'/api/boards/{self.board.id}/columns/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_deletar_coluna(self):
        col = Column.objects.create(title='Deletar', board=self.board, order=0)
        res = self.client.delete(f'/api/columns/{col.id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_nao_cria_coluna_em_board_alheio(self):
        board_alheio = Board.objects.create(title='Alheio', owner=self.other)
        res = self.client.post(f'/api/boards/{board_alheio.id}/columns/', {
            'title': 'Invasão'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_criar_coluna_sem_titulo_falha(self):
        res = self.client.post(f'/api/boards/{self.board.id}/columns/', {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


# ── TASKS ─────────────────────────────────────────────────────────────────────

class TaskTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = make_user()
        self.other = make_user('outro', 'senha123')
        token = get_token(self.client)
        auth(self.client, token)
        self.board = Board.objects.create(title='Board', owner=self.user)
        self.col   = Column.objects.create(title='A Fazer', board=self.board, order=0)
        self.col2  = Column.objects.create(title='Feito', board=self.board, order=1)

    def test_criar_tarefa(self):
        res = self.client.post(f'/api/columns/{self.col.id}/tasks/', {
            'title': 'Tarefa 1', 'priority': 'high'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], 'Tarefa 1')
        self.assertEqual(res.data['priority'], 'high')

    def test_criar_tarefa_sem_titulo_falha(self):
        res = self.client.post(f'/api/columns/{self.col.id}/tasks/', {}, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listar_tarefas(self):
        Task.objects.create(title='T1', column=self.col, priority='low')
        Task.objects.create(title='T2', column=self.col, priority='high')
        res = self.client.get(f'/api/columns/{self.col.id}/tasks/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_editar_tarefa(self):
        task = Task.objects.create(title='Original', column=self.col, priority='low')
        res = self.client.put(f'/api/tasks/{task.id}/', {
            'title': 'Editada', 'priority': 'high', 'description': ''
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Editada')
        self.assertEqual(res.data['priority'], 'high')

    def test_deletar_tarefa(self):
        task = Task.objects.create(title='Deletar', column=self.col, priority='medium')
        res = self.client.delete(f'/api/tasks/{task.id}/')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    def test_mover_tarefa_entre_colunas(self):
        task = Task.objects.create(title='Mover', column=self.col, priority='medium')
        res = self.client.patch(f'/api/tasks/{task.id}/move/', {
            'column_id': self.col2.id, 'order': 0
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.column, self.col2)

    def test_prioridade_invalida_falha(self):
        res = self.client.post(f'/api/columns/{self.col.id}/tasks/', {
            'title': 'Tarefa', 'priority': 'urgente'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_nao_acessa_tarefa_de_outro_usuario(self):
        board2 = Board.objects.create(title='Outro', owner=self.other)
        col2   = Column.objects.create(title='Col', board=board2, order=0)
        task   = Task.objects.create(title='Alheia', column=col2, priority='low')
        res = self.client.get(f'/api/tasks/{task.id}/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_tarefa_com_data_vencimento(self):
        res = self.client.post(f'/api/columns/{self.col.id}/tasks/', {
            'title': 'Com data', 'priority': 'medium', 'due_date': '2026-12-31'
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['due_date'], '2026-12-31')