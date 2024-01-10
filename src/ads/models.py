from enum import Enum as PythonEnum

from sqlalchemy import (
    Column, Integer, String, DateTime,
    MetaData, Enum, func, ForeignKey, Float
)
from sqlalchemy.orm import declarative_base

from auth.models import User

metadata = MetaData()

Base = declarative_base()


class AdType(str, PythonEnum):
    sale = "sale"
    purchase = "purchase"
    service = "service"


class Ad(Base):
    __tablename__ = "ad"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    type = Column(Enum(AdType))
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey(User.id))
