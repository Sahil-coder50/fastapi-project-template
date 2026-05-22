from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.users.schemas.UserSchema import UserCreate, UserOut
from app.modules.users.services.UserService import register_user, list_users

from app.dependencies.db import get_db
from app.pagination.base import PaginatedResponse
from app.dependencies.pagination import pagination_params

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserOut)
async def create(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await register_user(db, data)

@router.get("/", response_model=PaginatedResponse[UserOut])
async def get_all_users(
    db: AsyncSession = Depends(get_db),
    pagination: dict = Depends(pagination_params)
):
    total, users = await list_users(
        db,
        pagination["limit"],
        pagination["offset"]
    )

    return {
        "total": total,
        "limit": pagination["limit"],
        "offset": pagination["offset"],
        "data": users
    }