⚡ TaskFlow

Aplicação de gerenciamento de tarefas estilo Kanban, desenvolvida com Django REST Framework no backend e JavaScript puro no frontend.


📸 Preview

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
│   └── manage.py
└── frontend/
    ├── index.html       # login/cadastro
    └── board.html       # kanban
    
⚙️ Como rodar localmente

Backend

bashcd backend
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

A API estará disponível em http://127.0.0.1:8000/api/

Frontend

Abra a pasta frontend/ no VS Code e use a extensão Live Server para abrir o index.html.


O frontend espera a API rodando em http://127.0.0.1:8000. Ajuste a constante API nos arquivos .html caso necessário.

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
Deploy do backend no Railway
Deploy do frontend no Vercel
Testes automatizados
Edição de boards e colunas
Melhorias de UX/UI

👤 Autor

Jonatas Doroteu
GitHub · LinkedIn