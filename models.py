from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    due = Column(Date)
    completed = Column(Boolean, default=False)
    category = Column(String, index=True, nullable=True)  # ★変更: カテゴリ用の列を追加
