from datetime import date  # ★変更: 今日の日付取得に使用
from fastapi import FastAPI, Depends, Request, Form  # ★変更: Request, Form を追加
from fastapi.responses import HTMLResponse, RedirectResponse  # ★変更: HTML/リダイレクトレスポンス
from fastapi.templating import Jinja2Templates  # ★変更: テンプレート
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
import crud
from schemas import TodoCreate, TodoResponse

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")  # ★変更: テンプレートディレクトリを設定


# DBセッション依存性
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ======== APIエンドポイント（JSON用） =========

@app.get("/todos", response_model=list[TodoResponse])
def read_todos(db: Session = Depends(get_db)):
    return crud.get_todos(db)


@app.post("/todos", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    return crud.create_todo(db, todo)


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def complete(todo_id: int, db: Session = Depends(get_db)):
    return crud.complete_todo(db, todo_id)


@app.delete("/todos/{todo_id}")
def delete(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)
    return {"message": "Deleted"}


# ======== HTML画面用のエンドポイント =========

@app.get("/", response_class=HTMLResponse)  # ★変更: フィルター・カテゴリを考慮
def index(request: Request, db: Session = Depends(get_db)):
    filter_value = request.query_params.get("filter")  # ★変更: filter クエリ取得
    category = request.query_params.get("category")  # ★変更: category クエリ取得

    todos = crud.get_todos_filtered(db, filter_value, category)  # ★変更
    categories = crud.get_distinct_categories(db)  # ★変更
    today = date.today()  # ★変更

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "todos": todos,
            "filter": filter_value,
            "categories": categories,
            "selected_category": category,
            "today": today,
        },
    )


@app.post("/create")  # HTMLフォームからの新規作成
def create(
    title: str = Form(...),
    due: str = Form(...),
    category: str | None = Form(None),  # ★変更: カテゴリを受け取る
    db: Session = Depends(get_db),
):
    todo = TodoCreate(title=title, due=due, category=category)  # ★変更
    crud.create_todo(db, todo)
    return RedirectResponse("/", status_code=303)


@app.get("/complete/{todo_id}")  # HTMLから完了ボタン
def complete_html(todo_id: int, db: Session = Depends(get_db)):
    crud.complete_todo(db, todo_id)
    return RedirectResponse("/", status_code=303)


@app.get("/delete/{todo_id}")  # HTMLから削除ボタン
def delete_html(todo_id: int, db: Session = Depends(get_db)):
    crud.delete_todo(db, todo_id)
    return RedirectResponse("/", status_code=303)


@app.get("/edit/{todo_id}", response_class=HTMLResponse)  # ★変更: 編集画面表示
def edit_page(todo_id: int, request: Request, db: Session = Depends(get_db)):
    todo = crud.get_todo(db, todo_id)
    categories = crud.get_distinct_categories(db)
    return templates.TemplateResponse(
        "edit.html",
        {"request": request, "todo": todo, "categories": categories},
    )


@app.post("/edit/{todo_id}")  # ★変更: 編集内容の保存
def edit(
    todo_id: int,
    title: str = Form(...),
    due: str = Form(...),
    category: str | None = Form(None),
    db: Session = Depends(get_db),
):
    crud.update_todo(db, todo_id, title=title, due=due, category=category)
    return RedirectResponse("/", status_code=303)
