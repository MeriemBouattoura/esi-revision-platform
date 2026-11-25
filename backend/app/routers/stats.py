"""Module preparation statistics."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_current_user, get_db
from app.models.academics import Module
from app.models.content import Course
from app.models.users import User
from app.services.stats_service import preparation_level

router = APIRouter(tags=["stats"])


@router.get("/modules/{module_id}/stats")
def module_stats(module_id: int, db: Session = Depends(get_db),
                 user: User = Depends(get_current_user)) -> dict:
    """Return preparation levels for each course in a module."""
    if db.get(Module, module_id) is None:
        raise HTTPException(status_code=404, detail="Module not found")
    courses = db.scalars(select(Course).where(Course.module_id == module_id).order_by(Course.id))
    return {"module_id": module_id, "courses": [
        {"course_id": course.id, "title": course.title,
         "preparation_level": preparation_level(db, user.id, course.id)}
        for course in courses
    ]}
