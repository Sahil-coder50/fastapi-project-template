from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, declared_attr, relationship

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.modules.users.models import User

class AuditMixin:
    
    created_by_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id")
    )

    @declared_attr
    def created_by(cls) -> Mapped["User"]:
        return relationship(
            "User",
            foreign_keys=[cls.created_by_id]
        )
    
    updated_by_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id")
    )

    @declared_attr
    def updated_by(cls) -> Mapped["User"]:
        return relationship(
            "User",
            foreign_keys=[cls.updated_by_id]
        )
    