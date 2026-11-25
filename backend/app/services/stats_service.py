"""Preparation-level calculations."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.activity import QuizAttempt


def preparation_level(db: Session, user_id: int, course_id: int) -> int:
    """Compute a 0-100 score from at most five attempts, newest weighted most."""
    attempts = db.scalars(
        select(QuizAttempt)
        .where(QuizAttempt.user_id == user_id, QuizAttempt.course_id == course_id)
        .order_by(QuizAttempt.created_at.desc(), QuizAttempt.id.desc())
        .limit(5)
    ).all()
    if not attempts:
        return 0
    weights = list(range(len(attempts), 0, -1))
    weighted_percent = sum(
        (attempt.score / attempt.total_questions * 100) * weight
        for attempt, weight in zip(attempts, weights)
        if attempt.total_questions
    )
    total_weight = sum(weight for attempt, weight in zip(attempts, weights) if attempt.total_questions)
    return round(weighted_percent / total_weight) if total_weight else 0
