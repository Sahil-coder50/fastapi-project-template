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
├── cookiecutter.json
└── {{cookiecutter.project_slug}}
    ├── README.md
    ├── alembic
    │   ├── env.py
    │   └── versions
    ├── app
    │   ├── api
    │   │   ├── deps.py
    │   │   └── v1
    │   │       ├── endpoints
    │   │       │   └── health.py
    │   │       └── router.py
    │   ├── core
    │   │   ├── config.py
    │   │   ├── database.py
    │   │   ├── logging.py
    │   │   └── security.py
    │   ├── exceptions
    │   ├── main.py
    │   ├── middleware
    │   ├── models
    │   ├── repositories
    │   │   └── user_repo.py
    │   ├── schemas
    │   ├── services
    │   │   └── user_service.py
    │   ├── tests
    │   └── utils
    ├── docker
    │   ├── Dockerfile
    │   └── docker-compose.yml
    └── requirements.txt
```

### Command for making the Structure

```bash
mkdir -p "{{cookiecutter.project_slug}}"/{alembic/versions,app/api/v1/endpoints,app/core,app/{exceptions,middleware,models,repositories,schemas,services,tests,utils},docker} && \
touch cookiecutter.json "{{cookiecutter.project_slug}}"/{README.md,requirements.txt,alembic/env.py,app/main.py,app/api/deps.py,app/api/v1/router.py,app/api/v1/endpoints/health.py,app/core/{config.py,database.py,logging.py,security.py},app/repositories/user_repo.py,app/services/user_service.py,docker/{Dockerfile,docker-compose.yml}}
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

### api/v1/router.py

```bash
from fastapi import APIRouter
from app.api.v1.endpoints import health

router = APIRouter()

router.include_router(health.router, prefix="/health", tags=["Health"])

```

### api/v1/endpoints/health.py

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
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()
```

## Step 8: Database Setup

### app/core/database.py
```bash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

## Step 9: Dependency Injection

### app/api/deps.py

```bash
from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db_session(db: Session = Depends(get_db)):
    return db

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

### app/services/user_service.py

```bash
class UserService:

    def __init__(self, repo):
        self.repo = repo

    def create_user(self, data):
        return self.repo.create(data)
```

### app/repositories.user_repo.py

```bash
class UserRepository:

    def __init__(self, db):
        self.db = db

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
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### docker-compose.yml

```bash
version: "3.9"

services:
  web:
    build:
      context: ..
      dockerfile: docker/Dockerfile
    ports:
      - "8000:8000"

  db:
    image: postgres:15
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