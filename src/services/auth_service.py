"""Authentication Service - user login and access management."""
import hashlib
import csv
import os
from datetime import datetime

# File paths for user and access request data
USERS_FILE = "users.csv"
ACCESS_REQUESTS_FILE = "access_requests.csv"


def hash_password(password: str) -> str:
    """Hash password using SHA-256 for secure storage.
    
    Args:
        password: Plain text password
    
    Returns:
        SHA-256 hash of the password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """Verify a plain text password against its hash.
    
    Args:
        password: Plain text password to verify
        hashed: Stored SHA-256 hash
    
    Returns:
        True if password matches hash, False otherwise
    """
    return hash_password(password) == hashed


def ensure_users_file():
    """Create users.csv if it doesn't exist with default admin user.
    
    Default credentials:
    - Username: iqbal
    - Password: courtroom123
    """
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["username", "password_hash"])
            writer.writerow(["iqbal", hash_password("courtroom123")])


def ensure_access_requests_file():
    """Create access_requests.csv if it doesn't exist."""
    if not os.path.exists(ACCESS_REQUESTS_FILE):
        with open(ACCESS_REQUESTS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "email", "message", "status"])


def load_users() -> dict:
    """Load all users from CSV into dictionary.
    
    Returns:
        Dictionary mapping {username: password_hash}
    """
    ensure_users_file()
    users = {}
    try:
        with open(USERS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and "username" in row and "password_hash" in row:
                    users[row["username"]] = row["password_hash"]
    except Exception as e:
        print(f"Error loading users: {e}")
    return users


def authenticate(username: str, password: str) -> bool:
    """Authenticate user with username and password.
    
    Args:
        username: User's username
        password: User's plain text password
    
    Returns:
        True if authentication successful, False otherwise
    """
    users = load_users()
    if username not in users:
        return False
    return verify_password(password, users[username])


def submit_access_request(email: str, message: str) -> bool:
    """Submit access request from unauthenticated user.
    
    Args:
        email: User's email address
        message: Request message
    
    Returns:
        True if request submitted successfully, False otherwise
    """
    ensure_access_requests_file()
    try:
        with open(ACCESS_REQUESTS_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow([timestamp, email, message, "pending"])
        return True
    except Exception as e:
        print(f"Error submitting access request: {e}")
        return False


def get_access_requests() -> list:
    """Retrieve all pending access requests (for admin review).
    
    Returns:
        List of dictionaries containing access request data
    """
    ensure_access_requests_file()
    requests = []
    try:
        with open(ACCESS_REQUESTS_FILE, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row:
                    requests.append(row)
    except Exception as e:
        print(f"Error reading access requests: {e}")
    return requests
