from fastapi import FastAPI

from app.modules.users.routers import user_router
from app.middlewares import setup_middlewares

from app.core import setup_exceptions

app = FastAPI(title="Production FastAPI")

# Register middlewares
setup_middlewares(app)

# Exceptions
setup_exceptions(app)

# Health endpoint
@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    return {
        "status": "healthy"
    }

app.include_router(user_router, prefix="/api/v1")
