from enum import Enum as PythonEnum

from sqlalchemy import (
    Column, Integer, String, DateTime,
    Enum, func, ForeignKey, Float, CheckConstraint
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
    reviews = relationship("Review", back_populates="ad")


class Comment(base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey(User.id))
    ad_id = Column(Integer, ForeignKey(Ad.id))
    ad = relationship("Ad", back_populates="comments")


class Review(base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    rating = Column(
        Integer, CheckConstraint("rating >= 1 and rating <= 5"),
        nullable=False
    )
    created_at = Column(DateTime(timezone=True), default=func.now())
    user_id = Column(Integer, ForeignKey(User.id))
    ad_id = Column(Integer, ForeignKey(Ad.id))

    ad = relationship("Ad", back_populates="reviews")
