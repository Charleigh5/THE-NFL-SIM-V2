# Firebase Setup Guide

## Step 1: Create Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add Project"
3. Name it: `nfl-sim-engine` (or your preference)
4. Disable Google Analytics (not needed for this project)
5. Click "Create Project"

## Step 2: Download Service Account Key

1. In Firebase Console, click the ⚙️ (Settings) → **Project Settings**
2. Go to the **Service Accounts** tab
3. Click **Generate New Private Key**
4. Save the JSON file as: `serviceAccountKey.json`
5. **IMPORTANT:** Move this file to: `backend/serviceAccountKey.json`

## Step 3: Set Environment Variable

### Windows (PowerShell)

```powershell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\cweir\Documents\GitHub\THE NFL SIM\backend\serviceAccountKey.json"
```

### Add to `.env` file (Recommended)

Create/edit `backend/.env`:

```
GOOGLE_APPLICATION_CREDENTIALS=./serviceAccountKey.json
```

## Step 4: Secure the Key

Add to `backend/.gitignore`:

```
serviceAccountKey.json
*.json
!package.json
```

## Step 5: Initialize in Your App

In `backend/app/main.py`, add:

```python
from app.core.auth import initialize_firebase

@app.on_event("startup")
async def startup_event():
    initialize_firebase()
```

## Testing Authentication

Once set up, you can test with:

```python
from app.core.auth import verify_token

# Example token from frontend
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6..."
user_data = verify_token(token)
print(user_data['uid'])  # User ID
```

## Next Steps

1. Set up Firebase Authentication in the React frontend
2. Implement protected API routes using `get_current_user` dependency
3. Connect Firestore for cloud saves
