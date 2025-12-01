from pydantic import BaseModel
from datetime import date

class TodoBase(BaseModel):
    title: str
    due: date
    category: str | None = None  # ★変更: カテゴリを任意項目として追加

class TodoCreate(TodoBase):
    pass

class TodoResponse(TodoBase):
    id: int
    completed: bool

    class Config:
        orm_mode = True
