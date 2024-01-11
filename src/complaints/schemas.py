from pydantic import BaseModel


class ComplaintCreate(BaseModel):
    text: str
