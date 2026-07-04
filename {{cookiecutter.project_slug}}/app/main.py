from fastapi import FastAPI
from app.modules.users.routers import user_router
from app.middlewares import setup_middlewares
from app.core.exceptions import global_exception_handler

app = FastAPI(title="Production FastAPI")

# Register middlewares
setup_middlewares(app)

# Exceptions
app.add_exception_handler(Exception, global_exception_handler)

# Health endpoint
@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }

app.include_router(user_router, prefix="/api/v1")
