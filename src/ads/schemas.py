from pydantic import BaseModel


class AdCreate(BaseModel):
    title: str
    description: str
    price: float
    type: str


class CommentCreate(BaseModel):
    text: str


class ReviewCreate(BaseModel):
    text: str
    rating: int
