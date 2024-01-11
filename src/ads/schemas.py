from pydantic import BaseModel


class AdCreate(BaseModel):
    title: str
    description: str
    price: float
    type: str


class CommentCreate(BaseModel):
    text: str
