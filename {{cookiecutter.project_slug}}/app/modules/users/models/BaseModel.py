from .ModelCommonImport import *
from app.mixins import TimeStampMixin, AuditMixin, SoftDeleteMixin

class BaseModel(Base, AuditMixin, TimeStampMixin, SoftDeleteMixin):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    