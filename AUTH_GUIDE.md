# Authentication System Guide

## Default Login Credentials
- **Username:** `iqbal`
- **Password:** `courtroom123`

## File Structure

### `users.csv` - Authorized Users
Edit this file to manage who can log in.

```csv
username,password_hash
iqbal,9f55ee4a703a6ecc16e0f75ee2fe3f1408f774b866145465d69320f416c23b57
```

**To add a new user:**
1. Decide on their username and password
2. Generate the hash:
   ```bash
   conda activate ml_env
   python -c "from auth import hash_password; print(hash_password('their_password'))"
   ```
3. Add the line to `users.csv`:
   ```csv
   newusername,their_password_hash
   ```

### `access_requests.csv` - Access Requests (Auto-Generated)
Unauthenticated users can request access by filling the form. Their requests are saved here automatically.

```csv
timestamp,email,message,status
2026-07-02 16:20:14,test@example.com,Testing the system,pending
```

**To approve a request:**
1. Review the email and message
2. Add the user to `users.csv` with a temporary password
3. (Optional) Update status in `access_requests.csv` to "approved"

## How It Works

1. **Unauthenticated users** see:
   - About section explaining the simulation
   - Login form
   - Access request form

2. **Authenticated users** see:
   - Simulation and Metrics tabs (normal app)
   - Logout button in sidebar
   - Username display in sidebar

3. **Session persistence:**
   - Login is remembered in browser (Streamlit session state)
   - Logout clears the session
   - Closing the browser window does NOT log you out (persistent)

## Security Notes

- Passwords are hashed with SHA-256 before storage
- No plaintext passwords are stored
- `.env` file with API keys is still separate and private
- For production, consider upgrading to a proper database

## Commands

### Test authentication
```bash
conda activate ml_env
python -c "from auth import authenticate; print(authenticate('iqbal', 'courtroom123'))"
```

### View access requests
```bash
cat access_requests.csv
```

### Generate a password hash
```bash
conda activate ml_env
python -c "from auth import hash_password; print(hash_password('your_password'))"
```

## UI Features

- **Fancy landing page:** Two-column layout with About section and login/access request forms
- **Session persistence:** User stays logged in across page refreshes
- **Logout button:** Sidebar logout button clears session
- **Access requests:** CSV auto-saves all requests for your review
- **Responsive design:** Works on desktop and mobile
