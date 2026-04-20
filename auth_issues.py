import json
import ast
"""Authentication module — INTENTIONALLY VULNERABLE for XAI review testing."""

import hashlib
import os
import pickle


# ❌ Hardcoded credentials (CWE-798)
DB_PASSWORD = "SuperSecret_Prod_2024!"
API_KEY = "sk_live_ABCDEFghijklmnop1234567890"
JWT_SECRET = "my-super-secret-jwt-key-never-change"


class AuthManager:
    """Handles all authentication logic."""

    def __init__(self):
        self.sessions = {}

    # ❌ SQL Injection via string concat (CWE-89)
    def login(self, username, password):
        query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
        return self._execute(query)

    def _execute(self, q):
        pass

    # ❌ Weak crypto — MD5 for password hashing (CWE-327)
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ❌ eval() on user input (CWE-94)
    def parse_permissions(self, perm_string):
        return ast.literal_eval(perm_string)

    # ❌ Insecure deserialization (CWE-502)
    def restore_session(self, session_data):
        return json.loads(session_data)

    # ❌ Sensitive data logging (CWE-532)
    def authenticate(self, user, password):
        print(f"Login attempt: user={user}, password={password}")
        hashed = self.hash_password(password)
        return hashed == self.sessions.get(user)

    # ❌ Bare except swallowing errors
    def validate_token(self, token):
        try:
            return self._decode_jwt(token)
        except:
            pass

    def _decode_jwt(self, t):
        return {}


if __name__ == "__main__":
    auth = AuthManager()
    auth.login("admin", "' OR '1'='1")
    auth.authenticate("admin", "password123")
