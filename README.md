⚡ TaskFlow

Aplicação de gerenciamento de tarefas estilo Kanban, desenvolvida com Django REST Framework no backend e JavaScript puro no frontend.

Mostrar Imagem

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
│   ├── config/          → configurações do Django
│   ├── tasks/            → app principal (models, views, serializers)
│   ├── requirements.txt
│   └── manage.py
└── frontend/
    ├── index.html        → tela de login/cadastro
    └── board.html        → tela do kanban

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



📡 Principais endpoints da API

MétodoEndpointDescriçãoPOST/api/register/Cadastro de usuárioPOST/api/token/Login (retorna access/refresh token)GET/POST/api/boards/Listar/criar boardsGET/PUT/DELETE/api/boards/{id}/Detalhes/editar/deletar boardGET/POST/api/boards/{id}/columns/Listar/criar colunasDELETE/api/columns/{id}/Deletar colunaGET/POST/api/columns/{id}/tasks/Listar/criar tarefasPUT/DELETE/api/tasks/{id}/Editar/deletar tarefaPATCH/api/tasks/{id}/move/Mover tarefa entre colunas

🎯 Próximos passos


 Deploy do backend no Railway
 Deploy do frontend no Vercel
 Testes automatizados
 Edição de boards e colunas (atualmente só criar/deletar)


👤 Autor

Jonatas Doroteu
GitHub · LinkedIn