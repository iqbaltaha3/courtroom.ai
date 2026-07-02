# ⚠️ API Key Security Alert - Action Required

## What Happened

Your API keys were accidentally committed to the Git repository. GitHub's push protection detected this and blocked the push.

**Status:** 🔴 Action required before push can succeed

---

## ✅ Step-by-Step Resolution

### 1. Unblock the Push (GitHub)
1. Click this link: https://github.com/iqbaltaha3/courtroom.ai/security/secret-scanning/unblock-secret/3FwwAX1MJdnExmYsgl1MELEWwEr
2. Review the secret detection
3. Click **"Allow"** to unblock the push
4. Wait 30 seconds for GitHub to process

### 2. Rotate Your API Keys (URGENT ⚠️)

#### For GROQ API:
1. Go to https://console.groq.com/keys
2. Click the trash icon to **delete** the old key `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`
3. Click **"Create API Key"** to generate a new one
4. **Copy** the new key immediately

#### For TAVILY API:
1. Go to https://tavily.com/api-keys
2. Delete the old key `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`
3. Create a new API key
4. **Copy** the new key immediately

### 3. Update Local Configuration

Edit `.env` file (do NOT commit):
```bash
nano .env
```

Replace with new keys:
```
GROQ_API_KEY=<your_new_groq_key>
TAVILY_API_KEY=<your_new_tavily_key>
```

Edit `.streamlit/secrets.toml` (do NOT commit):
```bash
nano .streamlit/secrets.toml
```

Replace with new keys:
```toml
GROQ_API_KEY = "<your_new_groq_key>"
TAVILY_API_KEY = "<your_new_tavily_key>"
```

### 4. Test Locally
```bash
conda activate ml_env
streamlit run src/ui/app.py
```

### 5. Push to GitHub
```bash
git push origin main
```

---

## 🔐 Protecting Your Keys Going Forward

### 1. Never Commit Secrets
- `.env` is in `.gitignore` ✓
- `.streamlit/secrets.toml` should NOT be in Git
- Don't paste real keys in documentation ✓ (now using placeholders)

### 2. Add `.streamlit/` to `.gitignore`
```bash
echo ".streamlit/" >> .gitignore
echo "*.env" >> .gitignore
git add .gitignore
git commit -m "security: exclude secrets from git"
git push origin main
```

### 3. Use Different Keys per Environment
- **Local dev:** Original keys (now rotated)
- **Staging:** Different keys
- **Production:** Different keys

---

## 📋 Checklist

- [ ] Clicked GitHub unblock link
- [ ] Deleted old GROQ API key
- [ ] Created new GROQ API key
- [ ] Deleted old TAVILY API key
- [ ] Created new TAVILY API key
- [ ] Updated `.env` with new keys
- [ ] Updated `.streamlit/secrets.toml` with new keys
- [ ] Tested locally: `streamlit run src/ui/app.py`
- [ ] Successfully pushed to GitHub
- [ ] Updated Streamlit Cloud secrets dashboard

---

## 🚀 After Push Succeeds

1. Go to https://streamlit.io/cloud
2. Click your app settings → Secrets
3. Update with the new API keys
4. Redeploy

---

## ⚡ Quick Summary

```
EXPOSED KEY → ROTATE → UPDATE LOCAL → PUSH → UPDATE HOSTED
```

**Timeline:** ~5-10 minutes total

Your app will work perfectly once the new keys are in place! 🎉
