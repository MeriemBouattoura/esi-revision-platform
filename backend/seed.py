"""Insert a small curriculum, demo users, and sample quiz questions."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import hash_password
from app.models.academics import Module, Semester, Year
from app.models.content import Choice, Course, Question
from app.models.users import User

YEARS = ["1CP", "2CP", "1CS", "2CS", "3CS"]
SAMPLE = [
    ("What does CPU stand for?", "The CPU executes program instructions.", "easy",
     [("Central Processing Unit", True), ("Computer Program Utility", False), ("Core Process User", False), ("Central Program Unit", False)]),
    ("Which structure follows FIFO order?", "A queue processes its earliest item first.", "easy",
     [("Queue", True), ("Stack", False), ("Tree", False), ("Heap", False)]),
    ("What is the worst-case lookup complexity of binary search?", "Each step halves the remaining search interval.", "medium",
     [("O(log n)", True), ("O(n)", False), ("O(1)", False), ("O(n log n)", False)]),
    ("Which normal form eliminates transitive dependencies?", "Third normal form addresses transitive dependencies.", "medium",
     [("3NF", True), ("1NF", False), ("2NF", False), ("BCNF only", False)]),
    ("What is the value of 2^5?", "Two raised to the fifth power is 32.", "easy",
     [("32", True), ("16", False), ("25", False), ("64", False)]),
    ("Which traversal visits a binary search tree in sorted order?", "In-order traversal visits left, root, then right.", "medium",
     [("In-order", True), ("Pre-order", False), ("Post-order", False), ("Level-order", False)]),
    ("What does HTTP status 404 indicate?", "The requested resource could not be found.", "easy",
     [("Not Found", True), ("Unauthorized", False), ("Server Error", False), ("Created", False)]),
    ("Which SQL clause filters grouped rows?", "HAVING filters aggregate groups.", "medium",
     [("HAVING", True), ("WHERE", False), ("ORDER BY", False), ("LIMIT", False)]),
    ("What is a deadlock?", "A deadlock involves processes waiting in a cycle for resources.", "hard",
     [("A cyclic wait for resources", True), ("A process crash", False), ("Memory fragmentation", False), ("A cache miss", False)]),
    ("Which algorithm finds shortest paths with nonnegative edge weights?", "Dijkstra's algorithm assumes nonnegative edge weights.", "hard",
     [("Dijkstra", True), ("Depth-first search", False), ("Kruskal", False), ("Topological sort", False)]),
]


def seed(db: Session) -> None:
    """Create demo data idempotently."""
    for email, name, role in (
        ("admin@esi.dz", "ESI Admin", "admin"),
        ("student@esi.dz", "Demo Student", "student"),
    ):
        if db.scalar(select(User).where(User.email == email)) is None:
            db.add(User(name=name, email=email, password_hash=hash_password("ESIrevision2026!"), role=role))
    for name in YEARS:
        year = db.scalar(select(Year).where(Year.name == name))
        if year is None:
            year = Year(name=name)
            db.add(year)
            db.flush()
        for sem_name in ("S1", "S2"):
            semester = db.scalar(select(Semester).where(Semester.year_id == year.id, Semester.name == sem_name))
            if semester is None:
                semester = Semester(year_id=year.id, name=sem_name)
                db.add(semester)
                db.flush()
            if not semester.modules:
                module_names = ["Algorithmique", "Architecture des ordinateurs"] if sem_name == "S1" else ["Structures de données", "Bases de données"]
                for module_name in module_names:
                    module = Module(semester_id=semester.id, name=module_name)
                    db.add(module)
                    db.flush()
                    course = Course(module_id=module.id, title=f"{module_name} - Introduction", type="cours",
                                    file_url="https://example.com/sample.pdf")
                    db.add(course)
                    db.flush()
                    if name == "1CP" and sem_name == "S1" and module_name == "Algorithmique":
                        for text, explanation, difficulty, choices in SAMPLE:
                            db.add(Question(
                                course_id=course.id, text=text, explanation=explanation, difficulty=difficulty,
                                status="approved", author_id=None,
                                choices=[Choice(text=choice, is_correct=correct) for choice, correct in choices],
                            ))
    db.commit()


if __name__ == "__main__":
    with SessionLocal() as session:
        seed(session)
