"""Import all ORM models so metadata and migrations discover them."""

from app.models.academics import Module, Semester, Year
from app.models.activity import AttemptAnswer, QuizAttempt, Todo
from app.models.content import Choice, Course, Question
from app.models.social import Friendship, Message
from app.models.users import User

__all__ = [
    "AttemptAnswer", "Choice", "Course", "Friendship", "Message", "Module",
    "Question", "QuizAttempt", "Semester", "Todo", "User", "Year",
]
