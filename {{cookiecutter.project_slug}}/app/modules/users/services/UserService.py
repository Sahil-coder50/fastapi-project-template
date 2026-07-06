from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.repositories.UserRepo import *
from app.core.exceptions import AppException

import math

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
        "page": math.floor(offset / limit)+1
    }
    return meta, users

async def create_user_service(*, session: AsyncSession, data: dict):
    async with session.begin():
        if await user_exists(
            session=session,
            filters=User.email==data.get("email"),
        ):
            raise AppException(
                status_code=409,
                message="User with this Email Already Exists.",
                error="Duplicate Records",
            )

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
