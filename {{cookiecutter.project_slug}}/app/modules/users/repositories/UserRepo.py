from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.users.models.UserModel import User
from app.pagination.limit_offset import paginate

async def get_users(db: AsyncSession, limit: int, offset: int):
    query = await db.query(User)
    total, items = paginate(query, limit, offset)
    return total, items

async def create_user(db: AsyncSession, data):
    user = User(**data.dict())
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user