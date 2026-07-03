from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.modules.users.schemas.UserSchema import UserCreate, UserOut
from app.modules.users.services.UserService import *

from app.core.response import ApiResponse, ApiPaginateResponse
from app.dependencies.db import get_async_db
from app.pagination.base import PaginatedResponse
from app.dependencies.pagination import pagination_params, PaginationParams

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=ApiPaginateResponse[UserOut])
async def list_users(
        request: Request,
        pagination: Annotated[PaginationParams, Query()],
        session: AsyncSession = Depends(get_async_db),
):
    meta, data = await list_paginate_user_service(
        session=session,
        limit=pagination.limit,
        offset=pagination.offset
    )
    
    return ApiPaginateResponse.success(
        message="All User Record Retrieval Successful.",
        data=data,
        meta=meta
    )

@router.get("/{user_id}", response_model=ApiResponse[UserOut])
async def retrieve_user(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_db),
):
    data = await retrieve_user_service(
        session=session,
        id=user_id
    )

    return ApiResponse.success(
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

    return ApiResponse.success(
        message="User Created Successfully.",
        data=data
    )

@router.patch("/{user_id}", response_model=ApiResponse[UserOut])
async def update_user(
    request: Request,
    user_id: int,
    session: AsyncSession = Depends(get_async_db),
):
    data = await retrieve_user_service(
        session=session,
        id=user_id
    )

    return ApiResponse(
        message="User Updated Successfully.",
        data=data
    )
