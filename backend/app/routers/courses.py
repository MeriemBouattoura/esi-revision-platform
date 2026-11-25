"""Course document routes."""

from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.deps import get_db, require_admin
from app.models.academics import Module
from app.models.content import Course
from app.models.users import User

router = APIRouter(tags=["courses"])


def course_data(course: Course) -> dict:
    """Serialize a course document."""
    return {"id": course.id, "module_id": course.module_id, "title": course.title,
            "type": course.type, "file_url": course.file_url, "created_at": course.created_at}


@router.get("/modules/{module_id}/courses")
def list_courses(module_id: int, type: str | None = None, db: Session = Depends(get_db)) -> list[dict]:
    """List module documents, optionally by type."""
    if db.get(Module, module_id) is None:
        raise HTTPException(status_code=404, detail="Module not found")
    if type not in (None, "cours", "td"):
        raise HTTPException(status_code=422, detail="type must be cours or td")
    query = select(Course).where(Course.module_id == module_id)
    if type:
        query = query.where(Course.type == type)
    return [course_data(course) for course in db.scalars(query.order_by(Course.id))]


@router.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)) -> dict:
    """Return document metadata and a PDF URL."""
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_data(course)


@router.get("/uploads/{filename}")
def read_upload(filename: str) -> FileResponse:
    """Serve a stored PDF document."""
    path = (Path(settings.upload_dir) / filename).resolve()
    if path.parent != Path(settings.upload_dir).resolve() or not path.is_file():
        raise HTTPException(status_code=404, detail="Document not found")
    return FileResponse(path, media_type="application/pdf")


@router.post("/courses", status_code=201)
async def create_course(
    module_id: int = Form(...), title: str = Form(...), type: str = Form(...),
    file: UploadFile = File(...), db: Session = Depends(get_db), _: User = Depends(require_admin),
) -> dict:
    """Upload a course PDF as an administrator."""
    if type not in ("cours", "td"):
        raise HTTPException(status_code=422, detail="type must be cours or td")
    if file.content_type != "application/pdf" or not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=422, detail="Only PDF files are accepted")
    if db.get(Module, module_id) is None:
        raise HTTPException(status_code=404, detail="Module not found")
    content = await file.read(20 * 1024 * 1024 + 1)
    if len(content) > 20 * 1024 * 1024 or not content.startswith(b"%PDF-"):
        raise HTTPException(status_code=422, detail="Invalid PDF or file exceeds 20 MB")
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid4().hex}.pdf"
    (upload_dir / filename).write_bytes(content)
    course = Course(module_id=module_id, title=title.strip(), type=type, file_url=f"/api/v1/uploads/{filename}")
    db.add(course)
    db.commit()
    db.refresh(course)
    return course_data(course)


@router.delete("/courses/{course_id}", status_code=204)
def delete_course(course_id: int, db: Session = Depends(get_db), _: User = Depends(require_admin)) -> None:
    """Delete a course and its uploaded file."""
    course = db.get(Course, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    if course.file_url.startswith("/api/v1/uploads/"):
        path = (Path(settings.upload_dir) / Path(course.file_url).name).resolve()
        if path.parent == Path(settings.upload_dir).resolve() and path.is_file():
            path.unlink()
    db.delete(course)
    db.commit()
