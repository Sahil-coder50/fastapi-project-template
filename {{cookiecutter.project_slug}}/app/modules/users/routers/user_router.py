from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession

from typing import Annotated

from app.modules.users.schemas.user_schema import UserCreate, UserOut
from app.modules.users.services.user_service import UserService

from app.core.response import ApiResponse

from ..dependency import get_user_service

from fast_paginate import Paginate, ApiPaginateResponse

router = APIRouter(prefix="/users", tags=["Users"])



@router.get("", response_model=ApiPaginateResponse[list[UserOut]])
async def list_users(
        request: Request,
        pagination: Annotated[Paginate, Depends()],
        service: UserService = Depends(get_user_service),
):
    total, data = await service.list_paginate_user(
        limit=pagination.limit,
        offset=pagination.offset,
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
    service: UserService = Depends(get_user_service),
):
    data = await service.retrieve_user(
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
    service: UserService = Depends(get_user_service),
):
    data = await service.create_user(
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
    service: UserService = Depends(get_user_service),
):
    data = await service.update_user(
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
    service: UserService = Depends(get_user_service),
):
    user = await service.delete_user(
        id=user_id
    )

    return ApiResponse.success_response(
        message=f"User {user.email} Deleted Successfully",
        data=None
    )