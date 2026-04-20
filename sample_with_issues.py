"""
Sample Python file WITH intentional issues.
Use this to test that the XAI PR Reviewer catches problems.
"""

import os
import sys
import pickle
import subprocess
import eval  # ❌ Non-existent module import

# ❌ Hardcoded credentials (Security Vulnerability)
DB_PASSWORD = "admin123"
API_KEY = "sk-proj-abc123xyz789secretkey"
SECRET_TOKEN = "ghp_1234567890abcdefghijklmnopqrstuvwxyz"
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE/wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


# ❌ God Class Anti-Pattern (does everything)
class ApplicationManager:
    """Handles database, auth, email, logging, caching, and business logic all in one class."""

    def __init__(self):
        self.users = {}
        self.cache = {}
        self.logs = []
        self.db_connection = None
        self.email_queue = []
        self.config = {}
        self.sessions = {}
        self.metrics = {}
        self.temp_files = []

    # ❌ SQL Injection vulnerability
    def get_user(self, username):
        query = "SELECT * FROM users WHERE username = '" + username + "'"
        return self.execute_query(query)

    # ❌ Command Injection vulnerability
    def run_system_command(self, user_input):
        os.system("echo " + user_input)
        result = subprocess.call(user_input, shell=True)  # shell=True is dangerous
        return result

    # ❌ Insecure deserialization
    def load_data(self, data_bytes):
        return pickle.loads(data_bytes)  # Arbitrary code execution risk

    # ❌ Eval usage (Remote Code Execution)
    def calculate(self, expression):
        return eval(expression)  # Never eval user input

    # ❌ Bare except clause + swallowing exceptions
    def process_payment(self, amount, card_number):
        try:
            # ❌ Logging sensitive data
            print(f"Processing payment: card={card_number}, amount={amount}")
            self.logs.append(f"Card: {card_number}")
            result = amount / 0  # ❌ Division by zero bug
        except:  # ❌ Bare except - catches everything including SystemExit
            pass  # ❌ Silently swallowing the exception

    # ❌ Mutable default argument
    def add_items(self, item, item_list=[]):
        item_list.append(item)
        return item_list

    # ❌ No input validation, deeply nested logic (high cyclomatic complexity)
    def register_user(self, data):
        if data:
            if "name" in data:
                if len(data["name"]) > 0:
                    if "email" in data:
                        if "@" in data["email"]:
                            if "password" in data:
                                if len(data["password"]) > 0:
                                    if len(data["password"]) < 100:
                                        if "age" in data:
                                            if data["age"] > 0:
                                                if data["age"] < 150:
                                                    self.users[data["name"]] = data
                                                    return True
        return False

    # ❌ Resource leak - file handle never closed
    def read_config(self, path):
        f = open(path, "r")
        content = f.read()
        # Missing f.close() — resource leak
        return content

    # ❌ Path traversal vulnerability
    def get_file(self, filename):
        base_dir = "/app/uploads/"
        return open(base_dir + filename, "r").read()  # ../../etc/passwd attack

    # ❌ Race condition (TOCTOU)
    def safe_write(self, filepath, content):
        if os.path.exists(filepath):
            # Another process could modify/delete between check and write
            with open(filepath, "w") as f:
                f.write(content)

    # ❌ Dead code / unreachable code
    def validate_token(self, token):
        return True
        # Everything below is unreachable
        if token is None:
            return False
        if len(token) < 10:
            return False
        return token.startswith("valid_")

    # ❌ Inefficient algorithm - O(n²) when O(n) is possible
    def find_duplicates(self, items):
        duplicates = []
        for i in range(len(items)):
            for j in range(i + 1, len(items)):
                if items[i] == items[j]:
                    if items[i] not in duplicates:
                        duplicates.append(items[i])
        return duplicates

    # ❌ Global state mutation
    def update_config(self, key, value):
        import builtins
        setattr(builtins, key, value)  # Polluting global namespace

    # ❌ Weak cryptography
    def hash_password(self, password):
        import hashlib
        return hashlib.md5(password.encode()).hexdigest()  # MD5 is broken

    # ❌ Infinite loop potential
    def retry_connection(self):
        while True:
            try:
                self.db_connection = self.connect()
                break
            except:
                pass  # No backoff, no max retries, infinite loop on failure

    def connect(self):
        raise ConnectionError("DB unavailable")


# ❌ Circular dependency simulation
class ServiceA:
    def __init__(self):
        self.b = ServiceB()

class ServiceB:
    def __init__(self):
        self.a = ServiceA()  # ❌ Infinite recursion on instantiation


# ❌ No type hints, no docstrings, magic numbers
def calc(x, y, z):
    return x * 3.14159 + y / 2.71828 - z * 42 + 0.007 * x ** 2


# ❌ Wildcard import (pollutes namespace)
from os.path import *


# ❌ Global mutable state
GLOBAL_REGISTRY = {}
_internal_cache = []


def register(name, obj):
    GLOBAL_REGISTRY[name] = obj
    _internal_cache.append(obj)


# ❌ Thread safety issue
import threading

counter = 0

def increment():
    global counter
    for _ in range(1000000):
        counter += 1  # Not thread-safe, race condition


# ❌ Memory leak - growing list without bounds
event_log = []

def log_event(event):
    event_log.append(event)  # Never cleaned up, unbounded growth


# ❌ Unused variables and imports
unused_variable = "I'm never used"
another_unused = [1, 2, 3, 4, 5]


if __name__ == "__main__":
    app = ApplicationManager()

    # These will all cause issues at runtime
    app.get_user("admin' OR '1'='1")
    app.calculate("__import__('os').system('rm -rf /')")
    app.process_payment(100, "4111-1111-1111-1111")
    app.hash_password("mysecretpassword")
    print(calc(10, 20, 30))
