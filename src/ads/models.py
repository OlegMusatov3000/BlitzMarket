from enum import Enum as PythonEnum

from sqlalchemy import (
    Column, Integer, String, DateTime,
    Enum, func, ForeignKey, Float
)
from sqlalchemy.orm import relationship, declarative_base

from auth.models import User

base = declarative_base()


class AdType(str, PythonEnum):
    sale = "sale"
    purchase = "purchase"
    service = "service"


class Ad(base):
    __tablename__ = "ad"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    type = Column(Enum(AdType))
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey(User.id))
    comments = relationship("Comment", back_populates="ad")


class Comment(base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey(User.id))
    ad_id = Column(Integer, ForeignKey(Ad.id))
    ad = relationship("Ad", back_populates="comments")


class Complaint(base):
    __tablename__ = "complaint"

    id = Column(Integer, primary_key=True, index=True)
    for_ad = Column(Integer, ForeignKey(Ad.id))
    author = Column(Integer, ForeignKey(User.id))
    text = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
