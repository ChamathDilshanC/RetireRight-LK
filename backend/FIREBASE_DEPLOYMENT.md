# 🔐 Firebase Service Account - DigitalOcean Deployment

## ⚠️ Current Issue
The file `firebase-service-account.json` is in `.gitignore`, so it won't be deployed to DigitalOcean.

---

## ✅ OPTION 1: Use Environment Variable (Recommended for Production)

### Step 1: Convert JSON to Base64
```bash
# On Windows PowerShell:
cd backend
$content = Get-Content firebase-service-account.json -Raw
[Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($content)) | Set-Clipboard
# Now the base64 is in your clipboard
```

OR

```bash
# On Linux/Mac:
base64 firebase-service-account.json | tr -d '\n' | pbcopy
```

### Step 2: Add to DigitalOcean Environment Variables
In **App Platform → Settings → Environment Variables**, add:
```
FIREBASE_SERVICE_ACCOUNT_BASE64=<paste-the-base64-here>
```

### Step 3: Modify app/__init__.py

Replace the Firebase initialization section with this:

```python
# Initialize Firebase Admin SDK
try:
    # Check if Firebase is already initialized
    firebase_admin.get_app()
except ValueError:
    # Try to use base64-encoded service account from env
    service_account_base64 = os.environ.get('FIREBASE_SERVICE_ACCOUNT_BASE64')
    
    if service_account_base64:
        # Decode base64 and parse JSON
        import base64
        import json
        service_account_json = base64.b64decode(service_account_base64)
        service_account_dict = json.loads(service_account_json)
        cred = credentials.Certificate(service_account_dict)
        firebase_admin.initialize_app(cred)
        print("✅ Firebase initialized from environment variable")
    else:
        # Fall back to file (for local development)
        cred_path = os.path.join(os.path.dirname(__file__), '..', 'firebase-service-account.json')
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
            print("✅ Firebase initialized from file")
        else:
            print("⚠️ Warning: Firebase service account not configured")
```

---

## ✅ OPTION 2: Make Repository Private (Simple)

### Steps:
1. Make your GitHub repo private
2. Remove `firebase-service-account.json` from `.gitignore`
3. Commit the file:
```bash
git add backend/firebase-service-account.json
git commit -m "Add Firebase service account for deployment"
git push
```

### Why this works:
- Private repos are secure
- No need for environment variables
- Simpler deployment

⚠️ **NEVER do this with a public repository!**

---

## ✅ OPTION 3: DigitalOcean App Platform Secrets (Enterprise)

If you're on DigitalOcean's paid plan:
1. Go to **App Platform → Settings → Secrets**
2. Upload `firebase-service-account.json` as a secret
3. Mount it as a file in your app

---

## 🎯 RECOMMENDATION

For your use case (private project, DigitalOcean):

**Use OPTION 1 (Environment Variable)**
- Most secure
- Works with .gitignore
- Production-ready

---

## 📝 Summary

Currently, your `.gitignore` excludes the Firebase file, so:
1. Either use **Option 1** (base64 in env var)
2. Or use **Option 2** (private repo + commit file)

Without this, your backend will start but Firebase authentication won't work.
