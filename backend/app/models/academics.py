"""Academic year, semester, and module models."""

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class Year(Base):
    """A study year in the ESI curriculum."""

    __tablename__ = "years"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    semesters: Mapped[list["Semester"]] = relationship(back_populates="year", cascade="all, delete-orphan")


class Semester(Base):
    """A semester belonging to a study year."""

    __tablename__ = "semesters"
    __table_args__ = (UniqueConstraint("year_id", "name"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    year_id: Mapped[int] = mapped_column(ForeignKey("years.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(10), nullable=False)
    year: Mapped[Year] = relationship(back_populates="semesters")
    modules: Mapped[list["Module"]] = relationship(back_populates="semester", cascade="all, delete-orphan")


class Module(Base):
    """A module in a semester."""

    __tablename__ = "modules"
    __table_args__ = (UniqueConstraint("semester_id", "name"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    semester_id: Mapped[int] = mapped_column(ForeignKey("semesters.id", ondelete="CASCADE"), index=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    semester: Mapped[Semester] = relationship(back_populates="modules")
    courses: Mapped[list["Course"]] = relationship(back_populates="module", cascade="all, delete-orphan")
