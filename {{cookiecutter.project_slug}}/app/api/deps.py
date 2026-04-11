from app.core.database import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db_session(db: Session = Depends(get_db)):
    return db
