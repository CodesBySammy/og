"""
Enterprise Payment Processing System — Sample with intentional issues.
Tests all 14 new detectors + existing SAST patterns.
"""

import os
import sys
import pickle
import subprocess
import hashlib
import threading

# ❌ Hardcoded credentials (CWE-798)
STRIPE_SECRET_KEY = "sk_live_51HG3jKLmnop1234567890abcdefghijklmnop"
DATABASE_PASSWORD = "Pr0duct10n_DB_Pass!"
JWT_SECRET_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.supersecretpayload"


# ❌ God Class — handles payments, users, inventory, reports, notifications, and logging
class PaymentPlatform:
    """Monolithic class managing the entire payment processing lifecycle."""

    def __init__(self):
        self.users = {}
        self.transactions = []
        self.inventory = {}
        self.reports = []
        self.notifications = []
        self.audit_log = []
        self.sessions = {}
        self.configs = {}
        self.webhooks = []

    # ❌ SQL Injection via string concatenation (CWE-89)
    def fetch_order(self, order_id):
        query = "SELECT * FROM orders WHERE id = '" + order_id + "'"
        return self._execute_raw(query)

    def _execute_raw(self, q):
        pass

    # ❌ Command injection with os.system (CWE-78)
    def generate_report(self, report_name):
        os.system("wkhtmltopdf report_" + report_name + ".html output.pdf")
        result = subprocess.call(f"echo {report_name}", shell=True)
        return result

    # ❌ Insecure deserialization (CWE-502)
    def load_session(self, session_bytes):
        return pickle.loads(session_bytes)

    # ❌ eval() on user input (CWE-94)
    def compute_discount(self, formula):
        return eval(formula)

    # ❌ Bare except + swallowing exception + logging sensitive data (CWE-532)
    def charge_customer(self, amount, card_number, cvv):
        try:
            print(f"Charging card={card_number}, cvv={cvv}, amount=${amount}")
            self.audit_log.append(f"Charged card: {card_number}")
            fee = amount * 0.029 + 0.30
            net = amount - fee
            return net / 0  # ❌ Division by zero
        except:
            pass

    # ❌ Mutable default argument
    def add_line_items(self, item, cart=[]):
        cart.append(item)
        return cart

    # ❌ Deep nesting — high cyclomatic complexity
    def validate_checkout(self, data):
        if data:
            if "items" in data:
                if len(data["items"]) > 0:
                    if "shipping" in data:
                        if "address" in data["shipping"]:
                            if len(data["shipping"]["address"]) > 5:
                                if "payment" in data:
                                    if "method" in data["payment"]:
                                        if data["payment"]["method"] in ("card", "paypal"):
                                            if "email" in data:
                                                if "@" in data["email"]:
                                                    return True
        return False

    # ❌ Resource leak — file handle never closed (CWE-404)
    def load_config(self, path):
        f = open(path, "r")
        data = f.read()
        return data

    # ❌ Path traversal — unsanitized filename in open() (CWE-22)
    def get_receipt(self, filename):
        return open("/var/receipts/" + filename, "r").read()

    # ❌ Unreachable/dead code after return
    def is_premium(self, user_id):
        return user_id in self.users
        if user_id is None:
            return False
        membership = self.users.get(user_id, {})
        return membership.get("tier") == "premium"

    # ❌ Weak cryptography — SHA1 (CWE-327)
    def hash_transaction(self, data):
        return hashlib.sha1(data.encode()).hexdigest()

    # ❌ Weak cryptography — MD5 (CWE-327)
    def hash_email(self, email):
        return hashlib.md5(email.encode()).hexdigest()

    # ❌ Tight coupling — mixing I/O with business logic
    def process_refund(self, txn_id, amount):
        user_input = input(f"Confirm refund of ${amount} for txn {txn_id}? (y/n): ")
        if user_input.lower() == "y":
            refund_amount = amount * 0.95
            print(f"Refunded ${refund_amount}")
            return refund_amount
        return 0

    # ❌ Infinite retry loop — no backoff, no max attempts
    def connect_payment_gateway(self):
        while True:
            try:
                self._establish_connection()
                break
            except:
                pass

    def _establish_connection(self):
        raise ConnectionError("Gateway timeout")


# ❌ Circular dependency — OrderService and PaymentService instantiate each other
class OrderService:
    def __init__(self):
        self.payment = PaymentService()

    def place_order(self, items):
        return self.payment.process(items)


class PaymentService:
    def __init__(self):
        self.orders = OrderService()

    def process(self, items):
        return sum(i.get("price", 0) for i in items)


# ❌ Global mutable state modified via `global` keyword
request_counter = 0

def track_request():
    global request_counter
    request_counter += 1


# ❌ Thread-unsafe counter — race condition
active_connections = 0

def on_connect():
    global active_connections
    for _ in range(10000):
        active_connections += 1


# ❌ Unbounded collection — memory leak
failed_transactions = []

def log_failure(txn):
    failed_transactions.append(txn)


# ❌ Wildcard import polluting namespace
from os.path import *


# ❌ No type hints, no docstrings, magic numbers everywhere
def calc_tax(p, s, r):
    return p * 0.0825 + s * 3.14 - r * 42 + 0.005 * p ** 1.5


# ❌ Unused variables
dead_config = {"retries": 3, "timeout": 30}
unused_flag = True


if __name__ == "__main__":
    platform = PaymentPlatform()
    platform.fetch_order("1001' OR '1'='1")
    platform.compute_discount("__import__('os').system('whoami')")
    platform.charge_customer(99.99, "4532-0123-4567-8901", "123")
    platform.hash_email("user@company.com")
    platform.hash_transaction("txn_abc123")
    print(calc_tax(100, 10, 5))
