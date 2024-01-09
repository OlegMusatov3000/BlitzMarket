from enum import Enum as PythonEnum

from sqlalchemy import (
    Table, Column, Integer, String, DateTime,
    MetaData, Enum, func, ForeignKey, Float
)

from auth.models import user

metadata = MetaData()


class AdType(str, PythonEnum):
    sale = "sale"
    purchase = "purchase"
    service = "service"


ad = Table(
    "ad",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("title", String, index=True),
    Column("description", String),
    Column("price", Float),
    Column("type", Enum(AdType)),
    Column("created_at", DateTime(timezone=True), default=func.now()),
    Column("user_id", Integer, ForeignKey(user.c.id))
)
