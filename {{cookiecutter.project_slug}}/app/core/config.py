from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "{{ cookiecutter.project_name }}"
    DATABASE_URL: str
    SECRET_KEY: str

    class Config:
        env_file = ".env"

settings = Settings()