#!/usr/bin/env python3
"""
Simple User Manager - Add new users to users.csv
Usage: python add_user.py
"""

import csv
from auth import hash_password
import os

USERS_FILE = "users.csv"

def add_user():
    """Interactive user creation."""
    print("\n" + "="*50)
    print("⚙️  ADD NEW USER")
    print("="*50)
    
    # Get username
    username = input("\n📝 Enter username (e.g., john_doe): ").strip()
    
    if not username:
        print("❌ Username cannot be empty!")
        return
    
    # Check if user exists
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row and 'username' in row:
                    users[row['username']] = row['password_hash']
    
    if username in users:
        print(f"❌ User '{username}' already exists!")
        return
    
    # Get password
    password = input("🔐 Enter password (e.g., MySecure123): ").strip()
    
    if not password:
        print("❌ Password cannot be empty!")
        return
    
    if len(password) < 6:
        print("❌ Password must be at least 6 characters!")
        return
    
    # Confirm password
    confirm = input("🔐 Confirm password: ").strip()
    
    if password != confirm:
        print("❌ Passwords don't match!")
        return
    
    # Hash the password
    password_hash = hash_password(password)
    
    # Add to CSV
    try:
        if not os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['username', 'password_hash'])
        
        with open(USERS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([username, password_hash])
        
        print(f"\n✅ User '{username}' added successfully!")
        print(f"   Password: {password}")
        print(f"   They can now log in with these credentials!\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def view_users():
    """Show all users."""
    print("\n" + "="*50)
    print("👥 CURRENT USERS")
    print("="*50)
    
    if not os.path.exists(USERS_FILE):
        print("No users file found.")
        return
    
    try:
        with open(USERS_FILE, 'r') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                if row and 'username' in row:
                    count += 1
                    print(f"{count}. {row['username']}")
            
            if count == 0:
                print("No users found.")
            else:
                print(f"\nTotal: {count} user(s)\n")
    
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main menu."""
    while True:
        print("\n" + "="*50)
        print("👤 USER MANAGER")
        print("="*50)
        print("1. Add new user")
        print("2. View all users")
        print("3. Exit")
        print("="*50)
        
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            add_user()
        elif choice == "2":
            view_users()
        elif choice == "3":
            print("\n👋 Goodbye!\n")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()
