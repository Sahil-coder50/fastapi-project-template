from .BaseModel import BaseModel
from .ModelCommonImport import *

class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] =  mapped_column(Integer, primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password:Mapped[str] = mapped_column(String)
