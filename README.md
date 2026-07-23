## Step 1: Create Template Repo

```bash
mkdir fastapi-project-template
cd fastapi-project-template
git init
```

## Step 2: Install Cookiecutter

```bash
sudo apt update
sudo apt install pipx
pipx install cookiecutter
source ~/.bashrc
cookiecutter --version
```

## Step 3: FastAPI Template Structure

### Structure

```text
fastapi-project-template
├── README.md
├── cookiecutter.json
└── {{cookiecutter.project_slug}}
    ├── README.md
    ├── alembic
    │   ├── env.py
    │   ├── script.py.mako
    │   └── versions
    ├── alembic.ini
    ├── app
    │   ├── core
    │   │   ├── config.py
    │   │   ├── exceptions.py
    │   │   ├── logging.py
    │   │   └── security.py
    │   ├── db
    │   │   ├── base.py
    │   │   ├── base_class.py
    │   │   └── session.py
    │   ├── dependencies
    │   │   ├── db.py
    │   ├── main.py
    │   ├── middlewares
    │   │   ├── __init__.py
    │   │   └── cors.py
    │   ├── mixins
    │   │   ├── __init__.py
    │   │   └── audit_mixin.py
    │   │   └── base_model_mixin.py
    │   │   └── soft_delete.py
    │   │   └── time_mixin.py
    │   ├── modules
    │   │   └── users
    │   │       ├── dependency.py
    │   │       ├── models
    │   │       │   ├── user_model.py
    │   │       │   └── __init__.py
    │   │       ├── repositories
    │   │       │   ├── user_repo.py
    │   │       │   └── __init__.py
    │   │       ├── routers
    │   │       │   ├── user_router.py
    │   │       │   └── __init__.py
    │   │       ├── schemas
    │   │       │   ├── user_schema.py
    │   │       │   └── __init__.py
    │   │       └── services
    │   │           ├── user_service.py
    │   │           └── __init__.py
    │   └── utils
    ├── docker
    │   ├── Dockerfile
    │   └── compose.yaml
    └── requirements.txt
```

### Command for making the Structure

```bash
mkdir -p "{{cookiecutter.project_slug}}"/{alembic/versions,app/core,app/db,app/dependencies,app/middlewares,app/modules/users/models,app/modules/users/repositories,app/modules/users/routers,app/modules/users/schemas,app/modules/users/services,app/utils,docker} && \
touch cookiecutter.json README.md \
"{{cookiecutter.project_slug}}"/README.md \
"{{cookiecutter.project_slug}}"/requirements.txt \
"{{cookiecutter.project_slug}}"/alembic.ini \
"{{cookiecutter.project_slug}}"/alembic/{env.py,script.py.mako} \
"{{cookiecutter.project_slug}}"/app/main.py \
"{{cookiecutter.project_slug}}"/app/core/{config.py,exceptions.py,logging.py,security.py} \
"{{cookiecutter.project_slug}}"/app/db/{base.py,base_class.py,session.py} \
"{{cookiecutter.project_slug}}"/app/dependencies/{db.py} \
"{{cookiecutter.project_slug}}"/app/middlewares/{__init__.py,cors.py} \
"{{cookiecutter.project_slug}}"/app/mixins/{__init__.py,audit_mixin.py,base_model_mixin.py,soft_delete.py,time_mixin.py} \
"{{cookiecutter.project_slug}}"/app/modules/users/dependency.py \
"{{cookiecutter.project_slug}}"/app/modules/users/models/{user_model.py,__init__.py} \
"{{cookiecutter.project_slug}}"/app/modules/users/repositories/{user_repo.py,__init__.py} \
"{{cookiecutter.project_slug}}"/app/modules/users/routers/{user_router.py,__init__.py} \
"{{cookiecutter.project_slug}}"/app/modules/users/schemas/{user_schema.py,__init__.py} \
"{{cookiecutter.project_slug}}"/app/modules/users/services/{user_service.py,__init__.py} \
"{{cookiecutter.project_slug}}"/docker/{Dockerfile,compose.yaml,entrypoint.sh,nginx.conf}
```

## Step 4: cookiecutter.json

```bash
{
  "project_name": "FastAPI Project",
  "project_slug": "fastapi_project",
  "author": "your_name",
  "python_version": "3.11"
}
```

## Step 5: Entry Point

### app/main.py

```bash
from fastapi import FastAPI
from app.api.v1.router import router

app = FastAPI(title="{{ cookiecutter.project_name }}")

app.include_router(router, prefix="/api/v1")
```

## Step 6: Router Aggregation

### app/core/main.py

```bash
from fastapi import APIRouter
from app.modules.users.user_router import health      # Example

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["Health"])

```

### app/modules/users/user_router.py

```bash
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def health_check():
    return {"status": "ok"}
```

## Step 7: Core Config

### app/core/config.py
```bash
settings = Settings()
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"
    
    SYNC_DATABASE_URL: str
    ASYNC_DATABASE_URL: str
    
    REDIS_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

## Step 8: Database Setup

### app/db/session.py
```bash
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.ASYNC_DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=False
)

AsyncSessionLocal = sessionmaker(
    # autocommit=False,
    # autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
```

## Step 9: Dependency Injection

### app/dependencies/db.py

```bash
from app.db.session import AsyncSessionLocal

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            session.close()
```

## Step 10: JWT Auth Setup

### app/core/security.py

```bash
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = "change-me"
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```
## Step 11: Services and Repository Pattern

### app/modules/users/services/user_service.py

```bash
class UserService:

    def __init__(self, session: AsyncSession):
        self.session=session
        self.repo=UserRepo(session=self.session)

    def create_user(self, data):
        return self.repo.create(data)
```

### app/modules/users/repositories/user_repo.py

```bash
class UserRepo:

    def __init__(self, session: AsyncSession):
        self.session = self.session

    def create(self, data):
        pass
```

## Step 12: Alembic (Migrations)

### alembic/env.py (minimal)

```bash
from app.core.database import engine
from app.models import Base

target_metadata = Base.metadata

```

## Step 13: requirements.txt

```bash
fastapi
uvicorn
sqlalchemy
alembic
psycopg2-binary
pydantic-settings
python-jose
```

## Step 14: Docker Setup

### Dockerfile

```bash
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /{{ cookiecutter.project_slug }}

RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    libpq-dev \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x /{{ cookiecutter.project_slug }}/docker/entrypoint.sh

EXPOSE 8000
```

### compose.yaml

```bash
name: {{ cookiecutter.project_name }}

services:
  postgres:
    image: postgres:17
    restart: unless-stopped

    environment:
      - POSTGRES_DB=test_db
      - POSTGRES_USER=test_user
      - POSTGRES_PASSWORD=password

    volumes:
      - postgres_data:/var/lib/postgresql/data

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test_user -d test_db"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  redis:
    image: redis
    restart: unless-stopped

    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s

  web:
    build:
      context: ..
      dockerfile: docker/Dockerfile

    entrypoint: /{{ cookiecutter.project_slug }}/docker/entrypoint.sh

    command: >
      uvicorn app.main:app
      --host 0.0.0.0
      --port 8000
      --workers 4

    environment:
      RUN_MIGRATIONS: "1"

    env_file:
      - ../.env

    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy

    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:8000/health"]
      interval: 30s
      timeout: 5s
      retries: 3

    restart: unless-stopped

  nginx:
    image: nginx:latest
    restart: unless-stopped
    ports:
      - "8085:80"
    volumes:
      - ../docker/nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/{{ cookiecutter.project_slug }}/staticfiles
    depends_on:
      web:
        condition: service_healthy

volumes:
  postgres_data:
  static_volume:
```

### entrypoint.sh

```bash
#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."

while ! nc -z postgres 5432; do
    sleep 1
done

echo "PostgreSQL is available."

if [ "$RUN_MIGRATIONS" = "1" ]; then
    echo "Running Alembic migrations..."
    alembic upgrade head
fi

echo "Starting FastAPI..."

exec "$@"
```

### nginx.conf

```bash
events {}

http {
    upstream uvicorn {
        server web:8000;
    }

    server {
        listen 80;
        server_name localhost;

        client_max_body_size 20M;

        location /static/ {
            alias /{{ cookiecutter.project_slug }}/staticfiles/;
        }

        location / {
            proxy_pass http://uvicorn;

            proxy_http_version 1.1;

            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;


        }
    }
}
```

## Step 15: .env

```bash
DATABASE_URL=postgresql://user:password@localhost:5432/db
SECRET_KEY=supersecret
```

## Step 16: .gitignore

```bash
__pycache__/
.env
*.pyc
```

## Step 17: Commit and Push

```bash
git add .
git commit -m "Initial FastAPI project template"
git remote add origin https://github.com/your-username/fastapi-project-template.git
git branch -M main
git push -u origin main
```

## Step 18: Make a Template for a new FastAPI Project

```bash
mkdir your_project
cd your_project
cookiecutter https://github.com/your-username/fastapi-project-template.git
```