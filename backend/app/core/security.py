"""Password hashing and JWT helpers."""

from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

ALGORITHM = "HS256"
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Return a bcrypt hash of a password."""
    return password_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Check a password against its bcrypt hash."""
    return password_context.verify(password, password_hash)


def create_access_token(subject: str) -> str:
    """Create a signed access token for a user ID."""
    expires = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    return jwt.encode({"sub": subject, "exp": expires}, settings.jwt_secret, algorithm=ALGORITHM)
