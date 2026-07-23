from app.mixins import BaseModelMixin
from sqlalchemy import *
from sqlalchemy.orm import *
from app.db.base_class import Base

class User(BaseModelMixin):
    __tablename__ = "users"

    id: Mapped[int] =  mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password:Mapped[str] = mapped_column(String)
