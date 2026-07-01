# 🚛 Sarhad Express HR — Windows PC Setup

## Step 1 — Install Python
Download: https://python.org/downloads
⚠️ CHECK: "Add Python to PATH" during install!

## Step 2 — Open PowerShell in project folder
- Extract sarhad-hr-v2.zip
- Open folder
- Shift + Right Click → "Open PowerShell here"

## Step 3 — Run these commands ONE BY ONE:

```powershell
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate

# Install packages
pip install flask gspread google-auth google-auth-oauthlib

# Run the app
python run.py
```

## Step 4 — Open Browser
http://localhost:5000

## Login:
- Admin: SE000 / admin123
- Employee: SE001 / 1234
