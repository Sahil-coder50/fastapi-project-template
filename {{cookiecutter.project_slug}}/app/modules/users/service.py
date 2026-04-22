from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.repository import create_user, get_users

async def list_users(db: AsyncSession, limit: int, offset: int):
    return await get_users(db, limit, offset)

async def register_user(db: AsyncSession, data):
    return await create_user(db, data)