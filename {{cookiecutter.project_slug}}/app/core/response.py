from typing import Generic, TypeVar, Any
from pydantic import BaseModel, ConfigDict

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    status: str
    error: Any | None = None
    message: str | None = None
    data: T | None = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def success_response(cls, data: list[Any], message: str):
        return cls(
            status="success",
            message=message,
            data=data
        )
    @classmethod
    def error_response(cls, error: Any, message: str):
        return cls(
            status="error",
            message=message,
            error=error
        )

class ApiPaginateResponse(BaseModel, Generic[T]):
    status: str
    message: str | None = None
    data: T | None = None
    meta: dict[str, Any] | None = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def success_response(cls, data: list[Any], message: str, meta: dict[str, Any]| None = None):
        return cls(
            status="success",
            message=message,
            data=data,
            meta=meta
        )
