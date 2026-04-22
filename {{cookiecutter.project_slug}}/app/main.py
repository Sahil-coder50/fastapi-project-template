from fastapi import FastAPI
from app.modules.users.router import router as user_router
from app.middlewares import setup_middlewares
from app.core.exceptions import global_exception_handler

app = FastAPI(title="Production FastAPI")

# Register middlewares
setup_middlewares(app)

# Exceptions
app.add_exception_handler(Exception, global_exception_handler)

app.include_router(user_router, prefix="/api/v1")
