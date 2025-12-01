from datetime import date  # ★変更: 期限切れ判定に使用
from sqlalchemy.orm import Session
from models import Todo
from schemas import TodoCreate

def get_todos(db: Session):
    return db.query(Todo).all()

def get_todos_filtered(  # ★変更: フィルター付き一覧取得を追加
    db: Session,
    filter_value: str | None = None,
    category: str | None = None,
):
    query = db.query(Todo)

    if filter_value == "completed":  # ★変更
        query = query.filter(Todo.completed == True)
    elif filter_value == "active":  # ★変更
        query = query.filter(Todo.completed == False)
    elif filter_value == "expired":  # ★変更
        query = query.filter(Todo.completed == False, Todo.due < date.today())

    if category:  # ★変更: カテゴリで絞り込み
        query = query.filter(Todo.category == category)

    return query.order_by(Todo.due).all()  # ★変更: 期限順にソート

def get_distinct_categories(db: Session):  # ★変更: カテゴリ一覧を取得
    rows = db.query(Todo.category).distinct().all()
    return [row[0] for row in rows if row[0] is not None]

def get_todo(db: Session, todo_id: int):  # ★変更: 編集画面用に単体取得
    return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(db: Session, todo: TodoCreate):
    db_todo = Todo(
        title=todo.title,
        due=todo.due,
        category=todo.category,  # ★変更: カテゴリも保存
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def complete_todo(db: Session, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.completed = True
        db.commit()
        db.refresh(todo)
    return todo

def update_todo(  # ★変更: 編集用の更新処理を追加
    db: Session,
    todo_id: int,
    title: str,
    due: str,
    category: str | None,
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        return None

    todo.title = title
    todo.due = date.fromisoformat(due)
    todo.category = category
    db.commit()
    db.refresh(todo)
    return todo

def delete_todo(db: Session, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return todo
