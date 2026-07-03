from fastapi import Query
from pydantic import BaseModel, Field

def pagination_params(
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0)
):
    return {"limit": limit, "offset": offset}

class PaginationParams(BaseModel):
    offset: int = Field(alias="page", default=1, ge=1)
    limit: int = Field(alias="size", default=10, ge=1, le=100)
