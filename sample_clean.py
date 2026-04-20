"""
Sample Python file WITHOUT issues.
Use this to verify the XAI PR Reviewer passes clean, well-structured code.
"""

from __future__ import annotations

import hashlib
import hmac
import logging
import os
import secrets
import threading
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

# ✅ Secure configuration via environment variables
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///default.db")
API_KEY: str = os.getenv("API_KEY", "")

# ✅ Proper logging setup
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)


# ✅ Single Responsibility: User data model
@dataclass
class User:
    """Represents a registered user in the system."""

    MAX_AGE: int = 150  # Class constant for age validation

    user_id: str
    name: str
    email: str
    password_hash: str
    age: int

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("User name cannot be empty.")
        if "@" not in self.email:
            raise ValueError(f"Invalid email address: {self.email}")
        if not (0 < self.age < self.MAX_AGE):
            raise ValueError(f"Invalid age: {self.age}")


# ✅ Single Responsibility: Password hashing service
class PasswordService:
    """Handles secure password hashing and verification."""

    _ALGORITHM = "sha256"
    _ITERATIONS = 100_000
    _SALT_LENGTH = 32

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using PBKDF2 with a random salt."""
        salt = secrets.token_hex(PasswordService._SALT_LENGTH)
        key = hashlib.pbkdf2_hmac(
            PasswordService._ALGORITHM,
            password.encode("utf-8"),
            salt.encode("utf-8"),
            PasswordService._ITERATIONS,
        )
        return f"{salt}:{key.hex()}"

    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        """Verify a password against a stored hash."""
        try:
            salt, key_hex = stored_hash.split(":")
        except ValueError:
            return False

        new_key = hashlib.pbkdf2_hmac(
            PasswordService._ALGORITHM,
            password.encode("utf-8"),
            salt.encode("utf-8"),
            PasswordService._ITERATIONS,
        )
        return hmac.compare_digest(new_key.hex(), key_hex)


# ✅ Single Responsibility: User repository
class UserRepository:
    """Manages user storage and retrieval with thread safety."""

    def __init__(self) -> None:
        self._users: dict[str, User] = {}
        self._lock = threading.Lock()

    def add_user(self, user: User) -> None:
        """Add a user to the repository."""
        with self._lock:
            if user.user_id in self._users:
                raise ValueError(f"User with ID {user.user_id} already exists.")
            self._users[user.user_id] = user
            logger.info("User registered: %s", user.user_id)

    def get_user(self, user_id: str) -> User | None:
        """Retrieve a user by their ID."""
        with self._lock:
            return self._users.get(user_id)

    def user_exists(self, user_id: str) -> bool:
        """Check if a user exists."""
        with self._lock:
            return user_id in self._users


# ✅ Single Responsibility: Registration service
class RegistrationService:
    """Handles user registration logic."""

    def __init__(
        self,
        user_repo: UserRepository,
        password_service: PasswordService,
    ) -> None:
        self._user_repo = user_repo
        self._password_service = password_service

    def register(
        self,
        name: str,
        email: str,
        password: str,
        age: int,
    ) -> User:
        """Register a new user with validated input and secure password storage."""
        self._validate_password_strength(password)

        user_id = secrets.token_urlsafe(16)
        password_hash = self._password_service.hash_password(password)

        user = User(
            user_id=user_id,
            name=name,
            email=email,
            password_hash=password_hash,
            age=age,
        )
        self._user_repo.add_user(user)
        return user

    @staticmethod
    def _validate_password_strength(password: str) -> None:
        """Ensure the password meets minimum security requirements."""
        min_length = 8
        if len(password) < min_length:
            raise ValueError(
                f"Password must be at least {min_length} characters long."
            )
        if password.isalpha() or password.isdigit():
            raise ValueError(
                "Password must contain both letters and numbers."
            )


# ✅ Safe file operations with path validation
class FileService:
    """Handles file operations with security checks."""

    def __init__(self, base_directory: Path) -> None:
        self._base_dir = base_directory.resolve()

    def read_file(self, filename: str) -> str:
        """Read a file safely, preventing path traversal attacks."""
        safe_path = (self._base_dir / filename).resolve()

        # ✅ Path traversal prevention
        if not str(safe_path).startswith(str(self._base_dir)):
            raise PermissionError(
                f"Access denied: path traversal detected for '{filename}'."
            )

        if not safe_path.is_file():
            raise FileNotFoundError(f"File not found: {filename}")

        # ✅ Using context manager — no resource leak
        with open(safe_path, "r", encoding="utf-8") as f:
            return f.read()

    def write_file(self, filename: str, content: str) -> None:
        """Write content to a file atomically."""
        safe_path = (self._base_dir / filename).resolve()

        if not str(safe_path).startswith(str(self._base_dir)):
            raise PermissionError(
                f"Access denied: path traversal detected for '{filename}'."
            )

        # ✅ Atomic write to prevent partial writes
        temp_path = safe_path.with_suffix(".tmp")
        try:
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(content)
            temp_path.replace(safe_path)
        except Exception:
            if temp_path.exists():
                temp_path.unlink()
            raise


# ✅ Efficient algorithm — O(n) duplicate detection
def find_duplicates(items: list[Any]) -> list[Any]:
    """Find duplicate items in a list using O(n) counting."""
    counts = Counter(items)
    return [item for item, count in counts.items() if count > 1]


# ✅ Thread-safe counter
class AtomicCounter:
    """A thread-safe counter implementation."""

    def __init__(self, initial: int = 0) -> None:
        self._value = initial
        self._lock = threading.Lock()

    def increment(self, amount: int = 1) -> int:
        """Increment the counter and return the new value."""
        with self._lock:
            self._value += amount
            return self._value

    @property
    def value(self) -> int:
        """Get the current counter value."""
        with self._lock:
            return self._value


# ✅ Bounded event log with max size
@dataclass
class EventLog:
    """A bounded event log that prevents unbounded memory growth."""

    max_size: int = 10_000
    _events: list[str] = field(default_factory=list, repr=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def log(self, event: str) -> None:
        """Log an event, evicting the oldest if at capacity."""
        with self._lock:
            if len(self._events) >= self.max_size:
                self._events.pop(0)
            self._events.append(event)
            logger.debug("Event logged: %s", event)

    def recent(self, count: int = 10) -> list[str]:
        """Return the most recent events."""
        with self._lock:
            return list(self._events[-count:])


# ✅ Retry with exponential backoff and max attempts
def retry_with_backoff(
    func: Any,
    max_retries: int = 5,
    base_delay: float = 1.0,
) -> Any:
    """Retry a function with exponential backoff."""
    import time

    for attempt in range(1, max_retries + 1):
        try:
            return func()
        except Exception as exc:
            if attempt == max_retries:
                logger.error(
                    "All %d retry attempts failed. Last error: %s",
                    max_retries,
                    exc,
                )
                raise
            delay = base_delay * (2 ** (attempt - 1))
            logger.warning(
                "Attempt %d/%d failed (%s). Retrying in %.1fs...",
                attempt,
                max_retries,
                exc,
                delay,
            )
            time.sleep(delay)


def main() -> None:
    """Main entry point demonstrating clean code patterns."""
    # Setup services with dependency injection
    password_service = PasswordService()
    user_repo = UserRepository()
    registration_service = RegistrationService(user_repo, password_service)

    # Register a user
    demo_password = os.getenv("DEMO_PASSWORD", "")
    if not demo_password:
        demo_password = secrets.token_urlsafe(16)
    try:
        user = registration_service.register(
            name="Alice Johnson",
            email="alice@example.com",
            password=demo_password,
            age=30,
        )
        logger.info("User registered successfully: %s", user.user_id)
    except ValueError as e:
        logger.error("Registration failed: %s", e)

    # File operations
    file_service = FileService(Path("./uploads"))
    try:
        file_service.write_file("test.txt", "Hello, World!")
        content = file_service.read_file("test.txt")
        logger.info("File content: %s", content)
    except (PermissionError, FileNotFoundError) as e:
        logger.error("File operation failed: %s", e)

    # Efficient duplicate detection
    items = [1, 2, 3, 2, 4, 3, 5]
    dupes = find_duplicates(items)
    logger.info("Duplicates found: %s", dupes)

    # Thread-safe counter
    counter = AtomicCounter()
    counter.increment(10)
    logger.info("Counter value: %d", counter.value)

    # Bounded event log
    event_log = EventLog(max_size=100)
    event_log.log("Application started")
    event_log.log("User registered")
    logger.info("Recent events: %s", event_log.recent(5))


if __name__ == "__main__":
    main()
