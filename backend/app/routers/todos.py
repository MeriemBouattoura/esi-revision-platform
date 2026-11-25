"""Personal to-do list endpoints."""

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models.academics import Module
from app.models.activity import Todo
from app.models.users import User
from app.schemas.api import TodoCreate, TodoOut, TodoUpdate

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("", response_model=list[TodoOut])
def list_todos(module_id: int | None = None, scope: str | None = Query(default=None, pattern="^(global|module)$"),
               db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[Todo]:
    """List only the current user's tasks, with optional scope filters."""
    query = select(Todo).where(Todo.user_id == user.id)
    if scope == "global" or (module_id is None and scope is None):
        query = query.where(Todo.module_id.is_(None))
    elif scope == "module":
        if module_id is None:
            raise HTTPException(status_code=422, detail="module_id is required for module scope")
        query = query.where(Todo.module_id == module_id)
    elif module_id is not None:
        query = query.where(Todo.module_id == module_id)
    return list(db.scalars(query.order_by(Todo.due_date, Todo.id)).all())


@router.post("", response_model=TodoOut, status_code=201)
def create_todo(payload: TodoCreate, db: Session = Depends(get_db),
                user: User = Depends(get_current_user)) -> Todo:
    """Create a global or module-specific task."""
    if payload.module_id is not None and db.get(Module, payload.module_id) is None:
        raise HTTPException(status_code=404, detail="Module not found")
    todo = Todo(user_id=user.id, module_id=payload.module_id, title=payload.title.strip(), due_date=payload.due_date)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.patch("/{todo_id}", response_model=TodoOut)
def update_todo(todo_id: int, payload: TodoUpdate, db: Session = Depends(get_db),
                user: User = Depends(get_current_user)) -> Todo:
    """Update a task owned by the current user."""
    todo = db.get(Todo, todo_id)
    if todo is None or todo.user_id != user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(todo, field, value)
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}", status_code=204)
def delete_todo(todo_id: int, db: Session = Depends(get_db),
                user: User = Depends(get_current_user)) -> Response:
    """Delete a task owned by the current user."""
    todo = db.get(Todo, todo_id)
    if todo is None or todo.user_id != user.id:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return Response(status_code=204)
