"""Read-only curriculum navigation."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models.academics import Module, Semester, Year

router = APIRouter(tags=["academics"])


@router.get("/years")
def list_years(db: Session = Depends(get_db)) -> list[dict]:
    """List study years."""
    return [{"id": row.id, "name": row.name} for row in db.scalars(select(Year).order_by(Year.id))]


@router.get("/years/{year_id}/semesters")
def list_semesters(year_id: int, db: Session = Depends(get_db)) -> list[dict]:
    """List semesters for a year."""
    if db.get(Year, year_id) is None:
        raise HTTPException(status_code=404, detail="Year not found")
    rows = db.scalars(select(Semester).where(Semester.year_id == year_id).order_by(Semester.id))
    return [{"id": row.id, "year_id": row.year_id, "name": row.name} for row in rows]


@router.get("/semesters/{semester_id}/modules")
def list_modules(semester_id: int, db: Session = Depends(get_db)) -> list[dict]:
    """List modules for a semester."""
    if db.get(Semester, semester_id) is None:
        raise HTTPException(status_code=404, detail="Semester not found")
    rows = db.scalars(select(Module).where(Module.semester_id == semester_id).order_by(Module.id))
    return [{"id": row.id, "semester_id": row.semester_id, "name": row.name} for row in rows]


@router.get("/modules/{module_id}")
def get_module(module_id: int, db: Session = Depends(get_db)) -> dict:
    """Return a module with its semester and year."""
    row = db.get(Module, module_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return {"id": row.id, "semester_id": row.semester_id, "name": row.name,
            "semester": row.semester.name, "year": row.semester.year.name}
