"""Question creation and moderation routes."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.deps import get_current_user, get_db, require_admin
from app.models.content import Choice, Course, Question
from app.models.users import User
from app.schemas.api import QuestionAdminOut, QuestionCreate, QuestionStatus

router = APIRouter(tags=["questions"])


def check_correct_choice(choices: list) -> None:
    """Ensure every authored question has exactly one correct choice."""
    if sum(choice.is_correct for choice in choices) != 1:
        raise HTTPException(status_code=422, detail="A question must have exactly one correct choice")


@router.post("/questions", response_model=QuestionAdminOut, status_code=201)
def create_question(payload: QuestionCreate, db: Session = Depends(get_db),
                    user: User = Depends(get_current_user)) -> Question:
    """Create a suggestion (student) or approved question (admin)."""
    if db.get(Course, payload.course_id) is None:
        raise HTTPException(status_code=404, detail="Course not found")
    check_correct_choice(payload.choices)
    question = Question(
        course_id=payload.course_id, text=payload.text.strip(), explanation=payload.explanation.strip(),
        difficulty=payload.difficulty, status="approved" if user.role == "admin" else "pending",
        author_id=user.id, choices=[Choice(text=choice.text.strip(), is_correct=choice.is_correct)
                                    for choice in payload.choices],
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.get("/questions/pending", response_model=list[QuestionAdminOut])
def pending_questions(db: Session = Depends(get_db), _: User = Depends(require_admin)) -> list[Question]:
    """List questions awaiting moderation."""
    return list(db.scalars(
        select(Question).where(Question.status == "pending").options(selectinload(Question.choices))
    ).all())


@router.patch("/questions/{question_id}/status", response_model=QuestionAdminOut)
def update_question_status(question_id: int, payload: QuestionStatus, db: Session = Depends(get_db),
                           _: User = Depends(require_admin)) -> Question:
    """Approve or reject a pending question."""
    question = db.scalar(
        select(Question).where(Question.id == question_id).options(selectinload(Question.choices))
    )
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    if question.status != "pending":
        raise HTTPException(status_code=409, detail="Only pending questions can be reviewed")
    question.status = payload.status
    db.commit()
    db.refresh(question)
    return question


@router.get("/courses/{course_id}/questions", response_model=list[QuestionAdminOut])
def course_questions(course_id: int, db: Session = Depends(get_db),
                     _: User = Depends(require_admin)) -> list[Question]:
    """List all questions for a course for administrators."""
    if db.get(Course, course_id) is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return list(db.scalars(
        select(Question).where(Question.course_id == course_id).options(selectinload(Question.choices))
    ).all())
