from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, and_, or_, not_
from typing import Optional

from app.modules.users.models.UserModel import User
from fast_paginate import paginate

def build_query(filters, combine_with: Optional[str] = "and"):

    if combine_with == "and":
        combinator = and_(True, *filters)
    elif combine_with == "or":
        combinator = or_(*filters)
    else:
        if len(filters) > 1:
            raise ValueError(
                "Not filter can only be applied for a single condition or single grouped condition"
            )
        combinator = not_(filters[0])
    
    return combinator


async def list_users(*, session: AsyncSession, limit: int, offset: int):
    filters = [or_(User.is_deleted == False, User.email == "sahil4@yopmail.com")]
    combinator = build_query(filters, combine_with="not")
    orders = [User.created_at.desc(),]
    total, items = await paginate(session, User, limit, offset, combinator, orders)
    return total, items

async def filter_users(*, session: AsyncSession, filters: Optional[list] = [], orders: Optional[list] = []):
    items_stmt = select(User).where(and_(True, *filters)).order_by(*orders if orders is not [] else User.id.desc())
    result = await session.execute(items_stmt)
    items = result.scalars().all()

    return items

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

async def retrieve_user(*, session: AsyncSession, id: int) -> User:
    user = select(User).where(User.id == id, User.is_deleted == False)
    result = await session.execute(user)
    return result.scalar_one()

async def update_user(*, session: AsyncSession, user: User, data: dict) -> User:
    for key, value in data.items():
        setattr(user, key, value)
    
    await session.flush()
    await session.refresh(user)
    return user

async def delete_user(*, session: AsyncSession, user: User) -> User:
    setattr(user, "is_deleted", True)

    await session.flush()
    await session.refresh(user)

    return user
