# README_TodoList

# TodoList API - Backend

API REST para gerenciamento de tarefas com autenticação JWT, desenvolvida em Django REST Framework.

## Funcionalidades

- Autenticação JWT (email + senha)
- Refresh token automático
- CRUD completo de tarefas
- Favoritar/desfavoritar tarefas
- Detalhes de tarefas com prioridade e status
- CORS configurado
- Deploy no Render

## Tecnologias

- Django 5.2
- Django REST Framework 3.15
- Simple JWT
- PostgreSQL / SQLite
- Gunicorn
- Python-dotenv

## Pré-requisitos

- Python 3.12+
- pip
- Virtualenv

## Instalação

1. Clone o repositório

```bash
git clone https://github.com/KLima12/TodoListBackend.git
cd TodoListBackend
```

1. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

1. Instale as dependências

```bash
pip install -r requirements.txt
```

1. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```
SECRET_KEY=sua_chave_secreta_aqui
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

1. Execute as migrações

```bash
python manage.py migrate
```

1. Rode o servidor

```bash
python manage.py runserver
```

A API estará disponível em [http://localhost:8000](http://localhost:8000/)

## Endpoints

### Autenticação

- `POST /api/login/` - Login com email e senha
- `POST /api/register/` - Registrar novo usuário
- `POST /api/token/refresh/` - Renovar token de acesso
- `POST /api/token/verify/` - Verificar token

### Tarefas (requer autenticação)

- `GET /api/tasks/` - Listar todas as tarefas
- `POST /api/tasks/` - Criar nova tarefa
- `GET /api/tasks/{id}/` - Obter detalhes de uma tarefa
- `PUT /api/tasks/{id}/` - Atualizar tarefa
- `PATCH /api/tasks/{id}/` - Atualizar parcialmente
- `DELETE /api/tasks/{id}/` - Deletar tarefa

### Detalhes de Tarefas (requer autenticação)

- `GET /api/detalhes/by_task/?todo_id={id}` - Buscar detalhes por tarefa
- `POST /api/detalhes/` - Criar detalhes
- `PATCH /api/detalhes/{id}/` - Atualizar detalhes

## Exemplo de Login

```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@email.com", "password": "senha123"}'
```

## Exemplo de Criar Tarefa

```bash
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Authorization: Bearer seu_access_token" \
  -H "Content-Type: application/json" \
  -d '{"nome": "Estudar Django", "quantidade": 1, "favorito": false}'
```

## Estrutura do Projeto

```
TodoListBackend/
├── TodoList/           # Configurações do projeto
├── Todo/              # App principal
├── manage.py
├── requirements.txt
├── .env
└── Procfile
```

## Deploy

O projeto está configurado para deploy no Render.

### Build Command

```bash
pip install -r requirements.txt && python manage.py migrate
```

### Start Command

```bash
gunicorn TodoList.wsgi:application
```

### Variáveis de Ambiente

- `SECRET_KEY` - Chave secreta do Django
- `DEBUG` - False em produção
- `DATABASE_URL` - URL do PostgreSQL

API disponível em: [https://todolistbackend-6gdn.onrender.com](https://todolistbackend-6gdn.onrender.com/)

## Dependências

```
Django==5.2.13
djangorestframework==3.15.2
djangorestframework-simplejwt==5.3.1
django-cors-headers==4.4.0
gunicorn==23.0.0
psycopg2-binary==2.9.9
dj-database-url==2.2.0
python-dotenv==1.0.1
```

## Licença

MIT

## Autor

Klima

GitHub: [@KLima12](https://github.com/KLima12)