from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from app.modules.users.repositories.user_repo import UserRepo
from app.core.exceptions import AppException, NoRecordException

class UserService:

    def __init__(self, session: AsyncSession):
        self.session=session
        self.repo=UserRepo(session=self.session)
        

    async def register_user(self, data):
        return await self.repo.create_user(data=data)

    async def list_paginate_user(self, *, limit: int, offset: int):
        total, users =  await self.repo.list_users(
            limit=limit,
            offset=offset
        )

        return total, users

    async def create_user(self, *, data: dict):
        async with self.session.begin():
            if await self.repo.filter_users(
                filters=[User.email==data.get("email")],
            ):
                raise AppException(
                    status_code=409,
                    message="User with this Email Already Exists.",
                    error="Duplicate Records",
                )

            return await self.repo.create_user(
                data=data
            )

    async def retrieve_user(self, *, id: int):
        try:
            user = await self.repo.retrieve_user(
                id=id
            )
        except NoResultFound:
            raise NoRecordException(
                    model="user"
                )
        else:
            return user

    async def update_user(self, *, id: int, data: dict):
        async with self.session.begin():
            try:
                user = await self.repo.retrieve_user(
                    id=id
                )
            except NoResultFound:
                raise NoRecordException(
                    model="user"
                )
            else:
                return await self.repo.update_user( 
                    user=user,
                    data=data
                )
            
    async def delete_user(self, *, id: int):
        async with self.session.begin():
            try:
                user = await self.repo.retrieve_user(
                    id=id
                )
            except NoResultFound:
                raise NoRecordException(
                    model="user"
                )
            else:
                return await self.repo.delete_user(
                    user=user
                )

