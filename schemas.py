from pydantic import BaseModel
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    content: str | None = None


class NoteResponse(BaseModel):
    id: int
    title: str
    content: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
