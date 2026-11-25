"""Core authentication, quiz, statistics, and ownership tests."""

from sqlalchemy import select

from app.core.security import hash_password
from app.models.academics import Module, Semester, Year
from app.models.activity import QuizAttempt
from app.models.content import Choice, Course, Question
from app.models.users import User


def setup_course(db):
    """Create a user, course and approved sample question."""
    user = User(name="Student", email="student@example.com", password_hash=hash_password("password123"), role="student")
    admin = User(name="Admin", email="admin@example.com", password_hash=hash_password("password123"), role="admin")
    db.add_all([user, admin])
    db.flush()
    year = Year(name="1CP")
    db.add(year)
    db.flush()
    semester = Semester(year_id=year.id, name="S1")
    db.add(semester)
    db.flush()
    module = Module(semester_id=semester.id, name="Algorithms")
    db.add(module)
    db.flush()
    course = Course(module_id=module.id, title="Intro", type="cours", file_url="sample.pdf")
    db.add(course)
    db.flush()
    question = Question(course_id=course.id, text="Two plus two?", explanation="Basic arithmetic.",
                        difficulty="easy", status="approved", author_id=admin.id,
                        choices=[Choice(text="Four", is_correct=True), Choice(text="Five", is_correct=False)])
    db.add(question)
    db.commit()
    ids = user.id, admin.id, course.id, question.id, question.choices[0].id
    return ids


def token(client, email="student@example.com", password="password123"):
    """Authenticate a test user."""
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


def test_register_login_and_role_protection(client, db_session):
    """Register/login works and students cannot access admin routes."""
    registered = client.post("/api/v1/auth/register", json={
        "name": "New Student", "email": "new@example.com", "password": "password123",
    })
    assert registered.status_code == 201
    assert registered.json()["role"] == "student"
    assert client.post("/api/v1/auth/login", json={
        "email": "new@example.com", "password": "password123",
    }).status_code == 200
    setup_course(db_session)
    response = client.get("/api/v1/questions/pending", headers={"Authorization": f"Bearer {token(client)}"})
    assert response.status_code == 403


def test_quiz_generation_does_not_leak_answers(client, db_session):
    """Generated quiz questions do not include answer correctness."""
    _, _, course_id, _, _ = setup_course(db_session)
    response = client.post("/api/v1/quizzes/generate",
        headers={"Authorization": f"Bearer {token(client)}"},
        json={"course_id": course_id, "number_of_questions": 5})
    assert response.status_code == 200
    body = response.json()
    assert len(body["questions"]) == 1
    assert all("is_correct" not in choice for choice in body["questions"][0]["choices"])


def test_quiz_submission_grades_and_returns_correction(client, db_session):
    """Answers are graded server-side and persisted."""
    _, _, course_id, question_id, correct_choice_id = setup_course(db_session)
    response = client.post("/api/v1/quizzes/submit",
        headers={"Authorization": f"Bearer {token(client)}"},
        json={"course_id": course_id, "duration_seconds": 42,
              "answers": [{"question_id": question_id, "choice_id": correct_choice_id}]})
    assert response.status_code == 200
    assert response.json()["score"] == 1
    assert response.json()["correction"][0]["is_correct"] is True
    assert response.json()["correction"][0]["explanation"] == "Basic arithmetic."


def test_stats_computation_uses_recent_weighted_attempts(client, db_session):
    """Preparation level handles no history and applies recency weighting."""
    from app.services.stats_service import preparation_level
    _, _, course_id, _, _ = setup_course(db_session)
    user_id = db_session.scalar(select(User.id).where(User.email == "student@example.com"))
    assert preparation_level(db_session, user_id, course_id) == 0
    db_session.add_all([
        QuizAttempt(user_id=user_id, course_id=course_id, score=0, total_questions=1, duration_seconds=10),
        QuizAttempt(user_id=user_id, course_id=course_id, score=1, total_questions=1, duration_seconds=10),
    ])
    db_session.commit()
    assert preparation_level(db_session, user_id, course_id) == 67


def test_todo_ownership(client, db_session):
    """Users cannot read, change, or delete another user's task."""
    setup_course(db_session)
    owner = db_session.scalar(select(User).where(User.email == "student@example.com"))
    other = User(name="Other", email="other@example.com", password_hash=hash_password("password123"), role="student")
    db_session.add(other)
    db_session.flush()
    from app.models.activity import Todo
    todo = Todo(user_id=owner.id, title="Revise")
    db_session.add(todo)
    db_session.commit()
    todo_id = todo.id
    headers = {"Authorization": f"Bearer {token(client, 'other@example.com')}"}
    assert client.patch(f"/api/v1/todos/{todo_id}", headers=headers, json={"done": True}).status_code == 404
    assert client.delete(f"/api/v1/todos/{todo_id}", headers=headers).status_code == 404
