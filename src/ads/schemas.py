from pydantic import BaseModel


class AdCreate(BaseModel):
    id: int
    title: str
    description: str
    price: float
    type: str


class CommentCreate(BaseModel):
    text: str


class ComplaintCreate(BaseModel):
    text: str
