# HOW TO MANAGE USERS

## Simple Way: Use the User Manager Script

Instead of manually editing `users.csv`, use this simple script:

```bash
conda activate ml_env
python add_user.py
```

This will show you a menu:
```
==================================================
👤 USER MANAGER
==================================================
1. Add new user
2. View all users
3. Exit
==================================================
```

**To add a user:**
1. Choose option `1`
2. Enter username (e.g., `john_doe`)
3. Enter password (e.g., `MyPassword123`)
4. Confirm password
5. Done! ✅

**To view all users:**
1. Choose option `2`
2. See all current users

---

## Manual Way: Edit users.csv Directly

If you prefer, you can edit `users.csv` directly:

```csv
username,password_hash
iqbal,9f55ee4a703a6ecc16e0f75ee2fe3f1408f774b866145465d69320f416c23b57
john_doe,a1b2c3d4e5f6... (another hash)
```

To get a password hash for a new user:
1. Open a terminal
2. Run: `conda activate ml_env && python add_user.py`
3. Use the script (much easier than manual hashing!)

---

## Your Current User

```
Username: iqbal
Password: courtroom123
```

The long code `9f55ee4a703a6ecc16e0f75ee2fe3f1408f774b866145465d69320f416c23b57` is 
the encrypted version of your password. You never type this — only the script uses it 
to verify if someone's login is correct.

---

## Example: Adding a Colleague

Let's say you want to add your colleague Sarah with username `sarah` and password `Sarah2024!`

**Using the script (recommended):**
```bash
conda activate ml_env
python add_user.py
# Choose option 1
# Username: sarah
# Password: Sarah2024!
# Confirm: Sarah2024!
# ✅ Done!
```

Now Sarah can log in with:
- Username: `sarah`
- Password: `Sarah2024!`

That's it! Much simpler than dealing with hashes. 🎉
