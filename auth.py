"""Authentication and access control module."""

import hashlib
import csv
import os
from datetime import datetime
from pathlib import Path

USERS_FILE = "users.csv"
ACCESS_REQUESTS_FILE = "access_requests.csv"


def hash_password(password: str) -> str:
    """Hash a password using SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against its hash."""
    return hash_password(password) == hashed


def ensure_users_file():
    """Create users.csv if it doesn't exist (with default user)."""
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password_hash'])
            # Default user: username='iqbal', password='courtroom123'
            writer.writerow(['iqbal', hash_password('courtroom123')])


def ensure_access_requests_file():
    """Create access_requests.csv if it doesn't exist."""
    if not os.path.exists(ACCESS_REQUESTS_FILE):
        with open(ACCESS_REQUESTS_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['timestamp', 'email', 'message', 'status'])


def load_users() -> dict:
    """Load all users from CSV into a dict {username: password_hash}."""
    ensure_users_file()
    users = {}
    try:
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and 'username' in row and 'password_hash' in row:
                    users[row['username']] = row['password_hash']
    except Exception as e:
        print(f"Error loading users: {e}")
    return users


def authenticate(username: str, password: str) -> bool:
    """Authenticate a user. Returns True if credentials are valid."""
    users = load_users()
    if username not in users:
        return False
    return verify_password(password, users[username])


def submit_access_request(email: str, message: str) -> bool:
    """Submit an access request. Returns True if successful."""
    ensure_access_requests_file()
    try:
        with open(ACCESS_REQUESTS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, email, message, 'pending'])
        return True
    except Exception as e:
        print(f"Error submitting access request: {e}")
        return False


def get_access_requests() -> list:
    """Get all access requests (for manual review)."""
    ensure_access_requests_file()
    requests = []
    try:
        with open(ACCESS_REQUESTS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    requests.append(row)
    except Exception as e:
        print(f"Error reading access requests: {e}")
    return requests
