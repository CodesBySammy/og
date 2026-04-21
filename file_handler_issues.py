"""File handler — INTENTIONALLY VULNERABLE for XAI review testing."""

import os
import subprocess


class FileManager:
    """Manages file operations."""

    # ❌ Path traversal — unsanitized user input in open() (CWE-22)
    def read_file(self, user_path):
        return open("/var/data/" + user_path, "r").read()

    # ❌ Resource leak — file handle never closed (CWE-404)
    def load_config(self, path):
        f = open(path, "r")
        data = f.read()
        return data

    # ❌ OS Command Injection (CWE-78)
    def compress_file(self, filename):
        os.system("tar -czf archive.tar.gz " + filename)

    # ❌ Command injection with shell=True (CWE-78)
    def get_file_info(self, filepath):
        result = subprocess.run(f"file {filepath}", shell=True, capture_output=True)
        return result.stdout

    # ❌ Bare except masking errors
    def delete_file(self, path):
        try:
            os.remove(path)
        except:
            pass

    # ❌ Unreachable code after return
    def file_exists(self, path):
        return os.path.exists(path)
        if path is None:
            return False
        return os.path.isfile(path)

    # ❌ Mutable default argument
    def batch_read(self, paths, results=[]):
        for p in paths:
            results.append(self.load_config(p))
        return results


# ❌ Wildcard import
from os.path import *


if __name__ == "__main__":
    fm = FileManager()
    fm.read_file("../../etc/passwd")
    fm.compress_file("; rm -rf /")
