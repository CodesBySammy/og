"""Data processor — INTENTIONALLY VULNERABLE for XAI review testing."""

import hashlib
import threading


# ❌ God Class — does everything (10+ methods, 7+ attributes)
class DataProcessor:
    """Monolithic processor handling ETL, caching, validation, and reporting."""

    def __init__(self):
        self.raw_data = []
        self.clean_data = []
        self.cache = {}
        self.errors = []
        self.metrics = {}
        self.reports = []
        self.connections = []

    def extract(self, source):
        self.raw_data.append(source)

    def transform(self, record):
        self.clean_data.append(record)

    def load(self, dest):
        pass

    def validate(self, record):
        return bool(record)

    def build_report(self, data):
        self.reports.append(str(data))

    def cache_result(self, key, value):
        self.cache[key] = value

    def get_cached(self, key):
        return self.cache.get(key)

    def log_error(self, msg):
        self.errors.append(msg)

    def get_metrics(self):
        return self.metrics

    # ❌ Weak hashing (CWE-327)
    def hash_record(self, data):
        return hashlib.sha1(data.encode()).hexdigest()

    # ❌ Mutable default argument
    def merge_records(self, new, existing=[]):
        existing.extend(new)
        return existing

    # ❌ Mutable default argument (dict)
    def update_config(self, key, value, config={}):
        config[key] = value
        return config

    # ❌ Tight coupling — mixing I/O with logic
    def process_and_display(self, records):
        total = sum(r.get("amount", 0) for r in records)
        avg = total / len(records)
        print(f"Total: {total}, Average: {avg}")
        user_action = input("Continue? (y/n): ")
        return user_action == "y"


# ❌ Unbounded module-level list — memory leak
audit_trail = []

def log_audit(event):
    audit_trail.append(event)


# ❌ Global mutable state
total_processed = 0

def increment_count():
    global total_processed
    total_processed += 1


# ❌ Thread-unsafe shared counter
shared_counter = 0

def unsafe_increment():
    global shared_counter
    for _ in range(10000):
        shared_counter += 1


if __name__ == "__main__":
    dp = DataProcessor()
    dp.merge_records([1, 2, 3])
    dp.merge_records([4, 5, 6])  # Bug: gets [1,2,3,4,5,6] not [4,5,6]
    dp.hash_record("sensitive-data")
