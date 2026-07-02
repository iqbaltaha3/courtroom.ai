# 🚀 Deployment Secrets Configuration Guide

## Overview

MyPeshkar works seamlessly in both **local** and **hosted** environments. The app automatically detects and uses secrets from the appropriate source.

---

## 🏠 Local Development (Already Configured)

### File: `.streamlit/secrets.toml`
- **Auto-loaded** by Streamlit when you run `streamlit run`
- Contains: `GROQ_API_KEY`, `TAVILY_API_KEY`, `ENVIRONMENT`, `DEBUG`
- ✅ Already created and configured

### File: `.env`
- **Fallback** for non-Streamlit environments
- Used by `load_dotenv()` in Python
- ✅ Already has your API keys

**To run locally:**
```bash
conda activate ml_env
streamlit run src/ui/app.py
```

---

## ☁️ Hosted Deployment (Streamlit Cloud)

### Step 1: Connect Your GitHub Repository
1. Go to https://streamlit.io/cloud
2. Click "New app"
3. Select your GitHub repo (`courtroom` or `PROJECTS/AI_PROJECTS/courtroom`)
4. Set main file: `src/ui/app.py`
5. Click "Deploy"

### Step 2: Set Secrets in Streamlit Cloud Dashboard

After deployment, go to your app's settings:

1. **Click** the three-dot menu (⋯) → **Settings**
2. Scroll to **Secrets** section
3. Paste the following (TOML format) with YOUR actual keys:

```toml
# Get your actual keys from:
# - GROQ: https://console.groq.com/keys
# - TAVILY: https://tavily.com/api-keys

GROQ_API_KEY = "your_groq_api_key_here"
TAVILY_API_KEY = "your_tavily_api_key_here"
ENVIRONMENT = "production"
DEBUG = false
```

4. **Save** and wait for app to rebuild (1-2 minutes)

---

## 🔧 Other Hosting Platforms

### Heroku
Set config variables via Heroku CLI:
```bash
heroku config:set GROQ_API_KEY="your_key"
heroku config:set TAVILY_API_KEY="your_key"
```

### Render / Railway / Fly.io
Set environment variables in the deployment dashboard with the same key names:
- `GROQ_API_KEY`
- `TAVILY_API_KEY`
- `ENVIRONMENT=production`

### Azure / AWS / GCP
Use their secrets management:
- Azure Key Vault
- AWS Secrets Manager
- GCP Secret Manager

Then update the app to read from those services.

---

## ✅ How It Works (Behind the Scenes)

The app uses a smart fallback system:

```python
try:
    import streamlit as st
    API_KEY = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
except:
    API_KEY = os.getenv("GROQ_API_KEY")
```

**Priority order:**
1. **Streamlit secrets** (hosted: `.streamlit/secrets.toml`, cloud dashboard)
2. **Environment variables** (local: `.env`, hosted: platform settings)
3. **Fallback** (empty string if not found)

---

## 🔐 Security Best Practices

✅ **DO:**
- Store real API keys in `.env` locally (already in `.gitignore`)
- Use platform secrets manager for hosted deployments
- Rotate keys regularly
- Use read-only API keys where possible

❌ **DON'T:**
- Commit `.env` to Git (it's in `.gitignore`)
- Share your `.env` file
- Use the same keys across dev/staging/production
- Paste real API keys in documentation files (use placeholders instead)

---

## 🐛 Troubleshooting

### Error: `ModuleNotFoundError: No module named 'groq'`
**Solution:** The hosted platform needs to install dependencies.
- Check that `requirements.txt` is in the root directory
- Streamlit Cloud will auto-install from `requirements.txt`
- For other platforms, ensure dependencies are installed

### Error: `ValueError: Invalid API key`
**Solution:** The API key is not being read correctly.
1. **For Streamlit Cloud:** Go to app settings → Secrets and paste the TOML above
2. **For other platforms:** Set environment variables directly (not in `.env`)
3. **Verify locally first:** Run `streamlit run src/ui/app.py` to test

### App works locally but fails when hosted
**Solution:** Missing secrets in hosted environment.
1. Verify secrets are set in the platform dashboard
2. Check that key names match exactly: `GROQ_API_KEY`, `TAVILY_API_KEY`
3. Redeploy after adding secrets
4. Check app logs for error messages

---

## 📝 Deployment Checklist

- [ ] GitHub repository is public or accessible
- [ ] `.env` is in `.gitignore` (don't commit it!)
- [ ] `requirements.txt` is up-to-date
- [ ] Secrets set in hosting platform dashboard
- [ ] `ENVIRONMENT` set to `production` for live deployments
- [ ] Test the app works with hosted secrets
- [ ] Monitor logs for any import errors

---

## 📞 Quick Reference

| Environment | Secrets Location | How to Set |
|-------------|-----------------|-----------|
| **Local Dev** | `.streamlit/secrets.toml` + `.env` | Already configured ✓ |
| **Streamlit Cloud** | Dashboard → Settings → Secrets | Copy TOML above |
| **Heroku** | Heroku CLI or dashboard | `heroku config:set KEY=value` |
| **Docker** | Environment variables | `docker run -e KEY=value` |
| **Virtual Machine** | `.env` or system env vars | `export KEY=value` |

---

## 🚀 Next Steps

1. **Local:** Everything is already set up. Just run the app.
2. **Deploy:** Push to GitHub and connect to Streamlit Cloud
3. **Configure:** Add secrets in the hosting platform dashboard
4. **Monitor:** Check logs and metrics to ensure app is running

Your MyPeshkar courtroom AI is ready for the world! 🎯
