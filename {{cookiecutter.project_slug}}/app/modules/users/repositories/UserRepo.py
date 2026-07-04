from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists
from typing import Optional

from app.modules.users.models.UserModel import User
from app.pagination.limit_offset import paginate

async def list_users(*, session: AsyncSession, limit: int, offset: int):
    total, items = await paginate(session, User, limit, offset)
    return total, items

async def user_exists(*, session: AsyncSession, filters) -> bool:
    stmt = select(exists().where(filters))
    result = await session.execute(stmt)
    return result.scalar()

async def create_user(*, session: AsyncSession, data: dict) -> User:
    user = User(**data)
    session.add(user)
    await session.flush()
    await session.refresh(user)
    return user

async def retrieve_user(*, session: AsyncSession, id: int) -> Optional[User]:
    user = select(User).where(User.id == id)
    result = await session.execute(user)
    return result.scalar_one_or_none()

async def update_user(*, session: AsyncSession, user: User, data: dict):
    for key, value in data.items():
        setattr(user, key, value)
    
    await session.flush()
    await session.refresh(user)
    return user

async def delete_user(*, session: AsyncSession, user: User):
    setattr(user, "id_deleted", True)

    await session.flush()
    await session.refresh(user)

    return user
