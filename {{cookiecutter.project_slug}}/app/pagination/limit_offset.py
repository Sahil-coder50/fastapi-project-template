from sqlalchemy.orm import Query
from app.pagination.base import PaginatedResponse

def paginate(query: Query, limit: int, offset: int):
    total = query.count()
    items = query.offset(offset).limit(limit).all()

    return total, items
