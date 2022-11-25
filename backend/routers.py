from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .database import get_db
from .database_strategies import CommitData, DeleteData, UpdataData
from .schemas import TodoCreate, TodoResponse
from .models import Todo

router = APIRouter(prefix="/todo", tags=["Todo"])


@router.get("/", response_model=list[TodoResponse])
def get_todos(
    db: Session = Depends(get_db),
):
    return db.query(Todo).order_by(Todo.level_of_importance).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    new_todo = Todo(**todo.dict())
    with CommitData(db, new_todo):
        return new_todo


@router.get("/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.todo_id == todo_id).first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id <{todo_id}> was not found",
        )
    return todo


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
):
    query = db.query(Todo).filter(Todo.todo_id == todo_id)
    delete = DeleteData(db, query, todo_id, router.tags[0])
    return delete.run()


@router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, updated_todo: TodoCreate, db: Session = Depends(get_db)):
    query = db.query(Todo).filter(Todo.todo_id == todo_id)
    update = UpdataData(db, query, updated_todo.dict(), todo_id, router.tags[0])
    return update.run()
