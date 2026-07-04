from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.repositories.UserRepo import *

async def register_user(session: AsyncSession, data):
    return await create_user(session, data)

async def list_paginate_user_service(*, session: AsyncSession, limit: int, offset: int):
    total, users =  await list_users(
        session=session,
        limit=limit,
        offset=offset
    )
    meta = {
        "total": total,
        "size": limit,
        "page": offset
    }
    return meta, users

async def create_user_service(*, session: AsyncSession, data: dict):
    async with session.begin():
        return await create_user(
            session=session,
            data=data
        )

async def retrieve_user_service(*, session: AsyncSession, id: int):
    try:
        user = await retrieve_user(
            session=session,
            id=id
        )
    except Exception as e:
        raise ValueError(
            f"{e}"
        )
    else:
        return user

async def update_user_service(*, session: AsyncSession, id: int, data: dict):
    async with session.begin():
        try:
            user = await retrieve_user(
                session=session ,
                id=id
            )
        except Exception as e:
            raise ValueError(
                f"{e}"
            )
        else:
            return await update_user(
                session=session, 
                user=user,
                data=data
            )
        
async def delete_user_service(*, session: AsyncSession, id: int):
    async with session.begin():
        try:
            user = await retrieve_user(
                session=session,
                id=id
            )
        except Exception as e:
            raise ValueError(
                f"{e}"
            )
        else:
            return await delete_user(
                session=session,
                user=user
            )
