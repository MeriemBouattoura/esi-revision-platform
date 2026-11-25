"""Quiz generation, grading, and history endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.deps import get_current_user, get_db
from app.models.activity import QuizAttempt
from app.models.content import Course, Question
from app.models.users import User
from app.schemas.api import QuizGenerate, QuizResult, QuizSubmit
from app.services.quiz_service import grade_quiz, question_for_quiz

router = APIRouter(prefix="/quizzes", tags=["quizzes"])


@router.post("/generate")
def generate_quiz(payload: QuizGenerate, db: Session = Depends(get_db),
                  _: User = Depends(get_current_user)) -> dict:
    """Select random approved questions without their answer keys."""
    if db.get(Course, payload.course_id) is None:
        raise HTTPException(status_code=404, detail="Course not found")
    query = select(Question).where(
        Question.course_id == payload.course_id, Question.status == "approved"
    ).options(selectinload(Question.choices)).order_by(Question.id)
    if payload.difficulty:
        query = query.where(Question.difficulty == payload.difficulty)
    questions = list(db.scalars(query).all())
    import random
    random.SystemRandom().shuffle(questions)
    selected = questions[:payload.number_of_questions]
    if not selected:
        raise HTTPException(status_code=422, detail="No approved questions match this course and difficulty")
    return {"course_id": payload.course_id, "questions": [question_for_quiz(q) for q in selected]}


@router.post("/submit", response_model=QuizResult)
def submit_quiz(payload: QuizSubmit, db: Session = Depends(get_db),
                user: User = Depends(get_current_user)) -> QuizResult:
    """Grade and store a quiz submission."""
    attempt, correction = grade_quiz(
        db, user.id, payload.course_id, payload.duration_seconds, payload.answers
    )
    return QuizResult(attempt_id=attempt.id, score=attempt.score,
                      total_questions=attempt.total_questions, correction=correction)


@router.get("/history")
def quiz_history(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> list[dict]:
    """Return the current user's quiz history."""
    attempts = db.scalars(
        select(QuizAttempt).where(QuizAttempt.user_id == user.id)
        .order_by(QuizAttempt.created_at.desc(), QuizAttempt.id.desc())
    ).all()
    return [{"id": row.id, "course_id": row.course_id, "score": row.score,
             "total_questions": row.total_questions, "duration_seconds": row.duration_seconds,
             "created_at": row.created_at} for row in attempts]
