"""Course, question, and answer-choice models."""

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Course(Base):
    """A course document or TD document for a module."""

    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    module_id: Mapped[int] = mapped_column(ForeignKey("modules.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    type: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    file_url: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    module: Mapped["Module"] = relationship(back_populates="courses")
    questions: Mapped[list["Question"]] = relationship(back_populates="course", cascade="all, delete-orphan")


class Question(Base):
    """A multiple-choice question and moderation state."""

    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id", ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False, default="")
    difficulty: Mapped[str] = mapped_column(String(10), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(10), nullable=False, default="pending", index=True)
    author_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    course: Mapped[Course] = relationship(back_populates="questions")
    author: Mapped["User | None"] = relationship(back_populates="questions")
    choices: Mapped[list["Choice"]] = relationship(back_populates="question", cascade="all, delete-orphan")


class Choice(Base):
    """A selectable answer for a question."""

    __tablename__ = "choices"
    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id", ondelete="CASCADE"), index=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_correct: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    question: Mapped[Question] = relationship(back_populates="choices")
