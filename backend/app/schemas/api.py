"""Request and response models for the REST API."""

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field

Role = Literal["student", "admin"]
Difficulty = Literal["easy", "medium", "hard"]


class ORMModel(BaseModel):
    """Schema configured for SQLAlchemy object serialization."""

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """New account request."""

    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserOut(ORMModel):
    """Safe public user fields."""

    id: int
    name: str
    email: EmailStr
    role: Role
    created_at: datetime


class LoginRequest(BaseModel):
    """Password-based login request."""

    email: EmailStr
    password: str


class TokenOut(BaseModel):
    """Bearer access token response."""

    access_token: str
    token_type: str = "bearer"


class ChoiceOut(ORMModel):
    """A choice without correctness data."""

    id: int
    text: str


class QuestionOut(ORMModel):
    """A question suitable for a quiz."""

    id: int
    text: str
    difficulty: Difficulty
    choices: list[ChoiceOut]


class ChoiceCreate(BaseModel):
    """A choice supplied with a question."""

    text: str = Field(min_length=1, max_length=1000)
    is_correct: bool


class QuestionCreate(BaseModel):
    """A student suggestion or admin-authored question."""

    course_id: int
    text: str = Field(min_length=5, max_length=5000)
    explanation: str = Field(default="", max_length=5000)
    difficulty: Difficulty
    choices: list[ChoiceCreate] = Field(min_length=2, max_length=8)


class QuestionAdminOut(ORMModel):
    """Question details for administrative review."""

    id: int
    course_id: int
    text: str
    explanation: str
    difficulty: Difficulty
    status: str
    author_id: int | None
    choices: list[ChoiceOut]


class QuestionStatus(BaseModel):
    """Moderation status update."""

    status: Literal["approved", "rejected"]


class QuizGenerate(BaseModel):
    """Quiz generation options."""

    course_id: int
    number_of_questions: int = Field(ge=1, le=50)
    difficulty: Difficulty | None = None


class AnswerIn(BaseModel):
    """A selected answer in a submitted quiz."""

    question_id: int
    choice_id: int | None = None


class QuizSubmit(BaseModel):
    """A completed quiz submission."""

    course_id: int
    duration_seconds: int = Field(ge=0, le=86400)
    answers: list[AnswerIn] = Field(min_length=1, max_length=50)


class CorrectionItem(BaseModel):
    """Graded question with its answer and explanation."""

    question_id: int
    question: str
    selected_choice_id: int | None
    correct_choice_id: int
    is_correct: bool
    explanation: str


class QuizResult(BaseModel):
    """Submitted quiz score and correction."""

    attempt_id: int
    score: int
    total_questions: int
    correction: list[CorrectionItem]


class TodoCreate(BaseModel):
    """Create a personal task."""

    title: str = Field(min_length=1, max_length=240)
    module_id: int | None = None
    due_date: date | None = None


class TodoUpdate(BaseModel):
    """Update allowed task fields."""

    title: str | None = Field(default=None, min_length=1, max_length=240)
    done: bool | None = None
    due_date: date | None = None


class TodoOut(ORMModel):
    """Personal task response."""

    id: int
    user_id: int
    module_id: int | None
    title: str
    done: bool
    due_date: date | None
    created_at: datetime
