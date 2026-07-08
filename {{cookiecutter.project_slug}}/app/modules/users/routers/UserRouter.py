from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.modules.users.schemas.UserSchema import UserCreate, UserOut
from app.modules.users.services.UserService import *

from app.core.response import ApiResponse
from app.dependencies.db import get_async_db

from fast_paginate import Paginate, ApiPaginateResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=ApiPaginateResponse[list[UserOut]])
async def list_users(
        request: Request,
        pagination: Annotated[Paginate, Depends()],
        session: AsyncSession = Depends(get_async_db),
):
    total, data = await list_paginate_user_service(
        session=session,
        limit=pagination.limit,
        offset=pagination.offset
    )
    
    return pagination.get_paginated_response(
        total=total,
        data=data,
        request=request
    )


@router.get("/{user_id}/", response_model=ApiResponse[UserOut], response_model_exclude_none=True)
async def retrieve_user(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_db),
):
    data = await retrieve_user_service(
        session=session,
        id=user_id
    )

    return ApiResponse.success_response(
        message="User Retrieval Successful.",
        data=data
    )


@router.post("/", response_model=ApiResponse[UserOut])
async def create_user(
    request: Request,
    data: UserCreate,
    session: AsyncSession = Depends(get_async_db),
):
    data = await create_user_service(
        session=session,
        data=data.model_dump()
    )

    return ApiResponse.success_response(
        message="User Created Successfully.",
        data=data
    )


@router.patch("/{user_id}/", response_model=ApiResponse[UserOut])
async def update_user(
    request: Request,
    user_id: int,
    data: UserCreate,
    session: AsyncSession = Depends(get_async_db),
):
    data = await update_user_service(
        session=session,
        id=user_id,
        data=data.model_dump(exclude_unset=True)
    )

    return ApiResponse.success_response(
        message="User Updated Successfully.",
        data=data
    )


@router.delete("/{user_id}/", response_model=ApiResponse, response_model_exclude_none=True)
async def delete_user(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_db),
):
    user = await delete_user_service(
        session=session,
        id=user_id
    )

    return ApiResponse.success_response(
        message=f"User {user.email} Deleted Successfully",
        data=None
    )