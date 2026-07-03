from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from datetime import datetime

class TimeStampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now()
    )
