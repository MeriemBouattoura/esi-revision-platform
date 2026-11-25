"""Quiz grading and safe question serialization."""

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.content import Choice, Question
from app.models.activity import AttemptAnswer, QuizAttempt
from app.schemas.api import AnswerIn, CorrectionItem, QuestionOut


def question_for_quiz(question: Question) -> QuestionOut:
    """Serialize a question without exposing its answer key."""
    return QuestionOut(
        id=question.id,
        text=question.text,
        difficulty=question.difficulty,
        choices=[{"id": choice.id, "text": choice.text} for choice in question.choices],
    )


def grade_quiz(
    db: Session, user_id: int, course_id: int, duration_seconds: int, answers: list[AnswerIn]
) -> tuple[QuizAttempt, list[CorrectionItem]]:
    """Validate answers, grade them on the server, and persist the attempt."""
    question_ids = [answer.question_id for answer in answers]
    if len(set(question_ids)) != len(question_ids):
        raise HTTPException(status_code=422, detail="Each question may be answered only once")
    questions = db.scalars(
        select(Question)
        .where(Question.id.in_(question_ids), Question.course_id == course_id, Question.status == "approved")
        .options(selectinload(Question.choices))
    ).all()
    question_map = {question.id: question for question in questions}
    if len(question_map) != len(question_ids):
        raise HTTPException(status_code=422, detail="Answers must reference approved questions in this course")

    correction: list[CorrectionItem] = []
    answer_rows: list[AttemptAnswer] = []
    score = 0
    for answer in answers:
        question = question_map[answer.question_id]
        correct = next((choice for choice in question.choices if choice.is_correct), None)
        if correct is None:
            raise HTTPException(status_code=500, detail="Question has no correct answer configured")
        selected = next((choice for choice in question.choices if choice.id == answer.choice_id), None)
        if answer.choice_id is not None and selected is None:
            raise HTTPException(status_code=422, detail="Selected choice does not belong to its question")
        is_correct = selected is not None and selected.id == correct.id
        score += int(is_correct)
        answer_rows.append(AttemptAnswer(
            question_id=question.id, choice_id=selected.id if selected else None, is_correct=is_correct
        ))
        correction.append(CorrectionItem(
            question_id=question.id,
            question=question.text,
            selected_choice_id=answer.choice_id,
            correct_choice_id=correct.id,
            is_correct=is_correct,
            explanation=question.explanation,
        ))
    attempt = QuizAttempt(
        user_id=user_id, course_id=course_id, score=score,
        total_questions=len(answers), duration_seconds=duration_seconds, answers=answer_rows,
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    return attempt, correction
