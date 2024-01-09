from datetime import datetime

from pydantic import BaseModel


class AdReadCreate(BaseModel):
    id: int
    title: str
    description: str
    price: float
    type: str
    created_at: datetime
    user_id: int

    class Config:
        orm_mode = True
