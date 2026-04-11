from fastapi import FastAPI
from app.api.v1.router import router

app = FastAPI(title="{{ cookiecutter.project_name }}")

app.include_router(router, prefix="/api/v1")