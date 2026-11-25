"""Initial ESI revision platform schema.

Revision ID: 0001_initial
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create all phase-one and reserved phase-two tables."""
    op.create_table("users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role", "users", ["role"])
    op.create_table("years",
        sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(30), nullable=False),
        sa.UniqueConstraint("name"))
    op.create_table("semesters",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("year_id", sa.Integer(), sa.ForeignKey("years.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(10), nullable=False), sa.UniqueConstraint("year_id", "name"))
    op.create_index("ix_semesters_year_id", "semesters", ["year_id"])
    op.create_table("modules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("semester_id", sa.Integer(), sa.ForeignKey("semesters.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(120), nullable=False), sa.UniqueConstraint("semester_id", "name"))
    op.create_index("ix_modules_semester_id", "modules", ["semester_id"])
    op.create_table("courses",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("module_id", sa.Integer(), sa.ForeignKey("modules.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(200), nullable=False), sa.Column("type", sa.String(10), nullable=False),
        sa.Column("file_url", sa.String(500), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    op.create_index("ix_courses_module_id", "courses", ["module_id"])
    op.create_index("ix_courses_type", "courses", ["type"])
    op.create_table("questions",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("text", sa.Text(), nullable=False), sa.Column("explanation", sa.Text(), nullable=False),
        sa.Column("difficulty", sa.String(10), nullable=False), sa.Column("status", sa.String(10), nullable=False),
        sa.Column("author_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    for column in ("course_id", "difficulty", "status", "author_id"):
        op.create_index(f"ix_questions_{column}", "questions", [column])
    op.create_table("choices",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("text", sa.Text(), nullable=False), sa.Column("is_correct", sa.Boolean(), nullable=False))
    op.create_index("ix_choices_question_id", "choices", ["question_id"])
    op.create_table("quiz_attempts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False), sa.Column("total_questions", sa.Integer(), nullable=False),
        sa.Column("duration_seconds", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    for column in ("user_id", "course_id", "created_at"):
        op.create_index(f"ix_quiz_attempts_{column}", "quiz_attempts", [column])
    op.create_table("attempt_answers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("attempt_id", sa.Integer(), sa.ForeignKey("quiz_attempts.id", ondelete="CASCADE"), nullable=False),
        sa.Column("question_id", sa.Integer(), sa.ForeignKey("questions.id", ondelete="CASCADE"), nullable=False),
        sa.Column("choice_id", sa.Integer(), sa.ForeignKey("choices.id", ondelete="SET NULL"), nullable=True),
        sa.Column("is_correct", sa.Boolean(), nullable=False))
    for column in ("attempt_id", "question_id"):
        op.create_index(f"ix_attempt_answers_{column}", "attempt_answers", [column])
    op.create_index("ix_attempt_answers_choice_id", "attempt_answers", ["choice_id"])
    op.create_table("todos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("module_id", sa.Integer(), sa.ForeignKey("modules.id", ondelete="SET NULL"), nullable=True),
        sa.Column("title", sa.String(240), nullable=False), sa.Column("done", sa.Boolean(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    for column in ("user_id", "module_id"):
        op.create_index(f"ix_todos_{column}", "todos", [column])
    op.create_table("friendships",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("requester_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("receiver_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(10), nullable=False))
    for column in ("requester_id", "receiver_id", "status"):
        op.create_index(f"ix_friendships_{column}", "friendships", [column])
    op.create_table("messages",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("sender_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("receiver_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))
    for column in ("sender_id", "receiver_id"):
        op.create_index(f"ix_messages_{column}", "messages", [column])


def downgrade() -> None:
    """Remove schema in dependency-safe order."""
    for table in ("messages", "friendships", "todos", "attempt_answers", "quiz_attempts",
                  "choices", "questions", "courses", "modules", "semesters", "years", "users"):
        op.drop_table(table)
