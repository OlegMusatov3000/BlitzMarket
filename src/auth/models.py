from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import (
    Column, Integer, String, TIMESTAMP,
    ForeignKey, Boolean
)
from sqlalchemy.orm import declarative_base

base = declarative_base()


class Role(base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)


class User(SQLAlchemyBaseUserTable[int], base):

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    role_id = Column(Integer, ForeignKey(Role.id))
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
