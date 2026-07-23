from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.dependencies.db import get_async_db
from modules.users.services.user_service import UserService

def get_user_service(
    session: AsyncSession = Depends(get_async_db),
) -> UserService:
    return UserService(session)