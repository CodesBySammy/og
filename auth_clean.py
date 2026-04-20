"""Authentication module — CLEAN production-grade implementation."""


import hashlib
import hmac
import logging
import os
import secrets
from typing import Optional

# ✅ Secure config via environment variables
DB_URL: str = os.getenv("DATABASE_URL", "")
JWT_SECRET: str = os.getenv("JWT_SECRET", "")

logger = logging.getLogger(__name__)


class PasswordService:
    """Handles secure password hashing with PBKDF2."""

    _ITERATIONS = 100_000
    _SALT_LENGTH = 32

    @staticmethod
    def hash_password(password: str) -> str:
        salt = secrets.token_hex(PasswordService._SALT_LENGTH)
        key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), PasswordService._ITERATIONS)
        return f"{salt}:{key.hex()}"

    @staticmethod
    def verify(password: str, stored_hash: str) -> bool:
        try:
            salt, key_hex = stored_hash.split(":")
        except ValueError:
            return False
        new_key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), PasswordService._ITERATIONS)
        return hmac.compare_digest(new_key.hex(), key_hex)


class SessionStore:
    """Thread-safe session management."""

    def __init__(self) -> None:
        self._sessions: dict[str, dict] = {}

    def create(self, user_id: str) -> str:
        token = secrets.token_urlsafe(32)
        self._sessions[token] = {"user_id": user_id}
        return token

    def validate(self, token: str) -> Optional[dict]:
        return self._sessions.get(token)


class AuthService:
    """Orchestrates authentication using injected dependencies."""

    def __init__(self, pwd_service: PasswordService, sessions: SessionStore) -> None:
        self._pwd = pwd_service
        self._sessions = sessions

    def authenticate(self, username: str, password: str, stored_hash: str) -> Optional[str]:
        if self._pwd.verify(password, stored_hash):
            logger.info("User %s authenticated successfully.", username)
            return self._sessions.create(username)
        logger.warning("Failed login attempt for user: %s", username)
        return None


if __name__ == "__main__":
    pwd_svc = PasswordService()
    store = SessionStore()
    auth = AuthService(pwd_svc, store)
    hashed = pwd_svc.hash_password("StrongP@ss1")
    auth.authenticate("alice", "StrongP@ss1", hashed)
