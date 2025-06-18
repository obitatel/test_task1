from pydantic import BaseModel
from datetime import datetime

class Category(BaseModel):
    id: str
    name: str

class Task(BaseModel):
    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    due_date: datetime | None
    categories: list[Category] = []