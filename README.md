⚡ TaskFlow

Aplicação de gerenciamento de tarefas estilo Kanban, desenvolvida com Django REST Framework no backend e JavaScript puro no frontend.
🔗 **[Ver projeto ao vivo](https://taskflow-delta-eight.vercel.app/index.html)**


## 📸 Preview

### Login e Cadastro
![Login e Cadastro](screenshots/TaskFlow3.png)

### Kanban Board
![Kanban Board](screenshots/TaskFlow.png)

### Gerenciamento de Boards
![Boards](screenshots/TaskFlow2.png)



🚀 Funcionalidades


✅ Autenticação com JWT (login e cadastro)
✅ Criar, editar e deletar boards
✅ Criar, editar e deletar colunas
✅ Criar, editar e deletar tarefas
✅ Drag and drop de tarefas entre colunas
✅ Filtro de tarefas por prioridade (baixa, média, alta)
✅ Data de vencimento com alerta visual para tarefas atrasadas
✅ Cada usuário só visualiza seus próprios boards
✅ Feedback visual (toasts) para ações do usuário


🛠️ Tecnologias

Backend:


Python
Django
Django REST Framework
Simple JWT (autenticação)
django-cors-headers
dj-database-url
whitenoise
gunicorn
SQLite (dev) / PostgreSQL (produção)


Frontend:


HTML5
CSS3
JavaScript (Vanilla)


📁 Estrutura do projeto

taskflow/
├── backend/
│   ├── config/          # configurações Django
│   ├── tasks/           # app principal (models, views, serializers)
│   ├── requirements.txt
│   ├── Procfile         # comando de start para o Railway
│   ├── railpack.json    # configuração de build para o Railway
│   └── manage.py
└── frontend/
    ├── index.html       # login/cadastro
    └── board.html       # kanban
    
⚙️ Como rodar localmente

Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

A API estará disponível em http://127.0.0.1:8000/api/

Frontend

Abra a pasta frontend/ no VS Code e use a extensão Live Server para abrir o index.html.

O frontend espera a API rodando em http://127.0.0.1:8000. Ajuste a constante API nos arquivos .html caso necessário.

---

## ☁️ Deploy

### Backend — Railway

O backend está deployado no Railway com banco PostgreSQL.

**URL da API:** `https://taskflow-production-4bc2.up.railway.app/api/`

#### Configuração do Railway

1. Crie um novo projeto no [Railway](https://railway.app)
2. Adicione o serviço via **New → GitHub Repo** e selecione o repositório
3. Em **Settings → Root Directory**, coloque `backend`
4. Adicione um banco de dados via **New → Database → PostgreSQL**
5. Em **Variables**, adicione as seguintes variáveis de ambiente:

```
SECRET_KEY=sua-secret-key
DEBUG=False
ALLOWED_HOSTS=seu-projeto.up.railway.app
CSRF_TRUSTED_ORIGINS=https://seu-projeto.up.railway.app
CORS_ALLOWED_ORIGINS=https://seu-frontend.vercel.app
```

> A variável `DATABASE_URL` é adicionada automaticamente pelo Railway ao conectar o PostgreSQL.

6. No **Console** do serviço, rode as migrations:

```bash
python manage.py migrate
python manage.py createsuperuser
```

---

### Frontend — Vercel

O frontend está deployado no Vercel.

**URL:** `https://taskflow-delta-eight.vercel.app`

#### Configuração do Vercel

1. Acesse [vercel.com](https://vercel.com) e faça login com o GitHub
2. Clique em **New Project → Import Git Repository** e selecione o repositório
3. Em **Root Directory**, coloque `frontend`
4. Clique em **Deploy**

> Antes de fazer o deploy, atualize a constante `API` nos arquivos `board.html` e `index.html` com a URL do backend no Railway.

---

#### Atualizações automáticas

Qualquer `git push` na branch `main` dispara re-deploy automático no Railway e no Vercel.

---

📡 Endpoints da API

| Método         | Endpoint                    | Descrição             |
| -------------- | --------------------------- | --------------------- |
| POST           | `/api/register/`            | Cadastro de usuário   |
| POST           | `/api/token/`               | Login (JWT)           |
| GET/POST       | `/api/boards/`              | Listar/criar boards   |
| GET/PUT/DELETE | `/api/boards/{id}/`         | Detalhes do board     |
| GET/POST       | `/api/boards/{id}/columns/` | Colunas               |
| DELETE         | `/api/columns/{id}/`        | Deletar coluna        |
| GET/POST       | `/api/columns/{id}/tasks/`  | Tarefas               |
| PUT/DELETE     | `/api/tasks/{id}/`          | Editar/deletar tarefa |
| PATCH          | `/api/tasks/{id}/move/`     | Mover tarefa          |

🎯 Próximos passos
~~Deploy do backend no Railway~~ ✅
~~Deploy do frontend no Vercel~~ ✅
Testes automatizados
Edição de boards e colunas
Melhorias de UX/UI

👤 Autor

Jonatas Doroteu
GitHub · LinkedIn