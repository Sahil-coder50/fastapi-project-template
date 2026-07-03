from sqlalchemy import select, func

async def paginate(session, model, limit: int, offset: int):
    total_stmt = select(func.count()).select_from(model)
    total = await session.scalar(total_stmt)

    items_stmt = select(model).offset(offset).limit(limit)
    result = await session.execute(items_stmt)
    items = result.scalars().all()

    return total, items
