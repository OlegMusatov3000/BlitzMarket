from sqlalchemy import (
    Column, Integer, String, DateTime,
    func, ForeignKey
)
from sqlalchemy.orm import declarative_base

from ads.models import Ad
from auth.models import User

base = declarative_base()


class Complaint(base):
    __tablename__ = "complaint"

    id = Column(Integer, primary_key=True, index=True)
    for_ad = Column(Integer, ForeignKey(Ad.id))
    author = Column(Integer, ForeignKey(User.id))
    text = Column(String)
    created_at = Column(DateTime(timezone=True), default=func.now())
