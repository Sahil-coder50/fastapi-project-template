from .BaseModel import BaseModel
from sqlalchemy import *
from sqlalchemy.orm import *
from app.db.base_class import Base

class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] =  mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password:Mapped[str] = mapped_column(String)
