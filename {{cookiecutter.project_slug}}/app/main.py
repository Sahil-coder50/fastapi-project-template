from fastapi import FastAPI
from sqlalchemy.exc import SQLAlchemyError

from app.modules.users.routers import user_router
from app.middlewares import setup_middlewares
from app.core.exceptions import global_exception_handler, sqlalchemy_exception_handler

app = FastAPI(title="Production FastAPI")

# Register middlewares
setup_middlewares(app)

# Exceptions
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# Health endpoint
@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    return {
        "status": "healthy"
    }

app.include_router(user_router, prefix="/api/v1")
