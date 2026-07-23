from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, and_, or_, not_
from typing import Optional

from app.modules.users.models.user_model import User
from fast_paginate import paginate

from enum import StrEnum

class Operator(StrEnum):
    AND = and_
    OR = or_
    NOT = not_

def build_query(filters, combine_with: Optional[str] = Operator.AND):

    if combine_with == Operator.AND:
        combinator = and_(True, *filters)
    elif combine_with == Operator.OR:
        combinator = or_(*filters)
    else:
        if len(filters) > 1:
            raise ValueError(
                "Not filter can only be applied for a single condition or single grouped condition"
            )
        combinator = not_(filters[0])
    
    return combinator

class UserRepo:

    def __init__(self, session: AsyncSession):
        self.session = self.session

    async def list_users(self, *, limit: int, offset: int):
        filters = [or_(User.is_deleted == False, User.email == "sahil4@yopmail.com")]
        combinator = build_query(filters, combine_with=Operator.AND)
        orders = [User.created_at.desc(),]
        total, items = await paginate(self.session, User, limit, offset, combinator, orders)
        return total, items

    async def filter_users(self, *, filters: Optional[list] = [], orders: Optional[list] = []):
        items_stmt = select(User).where(and_(True, *filters)).order_by(*orders if orders is not [] else User.id.desc())
        result = await self.session.execute(items_stmt)
        items = result.scalars().all()

        return items

    async def create_user(self, *, data: dict) -> User:
        user = User(**data)
        self.session.add(user)
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def retrieve_user(self, *, id: int) -> User:
        user = select(User).where(User.id == id, User.is_deleted == False)
        result = await self.session.execute(user)
        return result.scalar_one()

    async def update_user(self, *, user: User, data: dict) -> User:
        for key, value in data.items():
            setattr(user, key, value)
        
        await self.session.flush()
        await self.session.refresh(user)
        return user

    async def delete_user(self, *, user: User) -> User:
        setattr(user, "is_deleted", True)

        await self.session.flush()
        await self.session.refresh(user)

        return user
