# 🚀 SETUP INSTRUCTIONS - RetireRight LK

## ✅ What Has Been Created

Your RetireRight LK application is now set up with:

### Backend (Flask + Firebase Admin)

- ✅ Complete Flask REST API structure
- ✅ Firebase Authentication integration
- ✅ EPF/ETF calculation engine
- ✅ User profile management
- ✅ Calculation history tracking
- ✅ SQLAlchemy database models
- ✅ Protected API routes with JWT

### Frontend (React + TypeScript + Firebase)

- ✅ React 18 with TypeScript
- ✅ Firebase Google Sign-In
- ✅ Authentication store (Zustand)
- ✅ Protected routes
- ✅ Login page with Google OAuth
- ✅ Dashboard page
- ✅ API service layer
- ✅ TailwindCSS styling

---

## 📋 NEXT STEPS TO RUN THE APPLICATION

### Step 1: Backend Setup (5 minutes)

1. **Open a PowerShell terminal** in the backend folder:

   ```powershell
   cd "c:\Users\chamm\Desktop\RetireRight LK\backend"
   ```

2. **Create and activate virtual environment:**

   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**

   ```powershell
   copy .env.example .env
   ```

5. **Download Firebase Service Account:**

   - Go to: https://console.firebase.google.com/
   - Select project: `retireright-lk-41def`
   - Go to: **Project Settings** > **Service Accounts**
   - Click: **"Generate New Private Key"**
   - Save the JSON file as: `firebase-service-account.json` in the `backend` folder

6. **Run the backend:**

   ```powershell
   python run.py
   ```

   ✅ Backend should now be running at: http://localhost:5000

---

### Step 2: Frontend Setup (5 minutes)

1. **Open a NEW PowerShell terminal** in the frontend folder:

   ```powershell
   cd "c:\Users\chamm\Desktop\RetireRight LK\frontend"
   ```

2. **Install dependencies:**

   ```powershell
   npm install
   ```

3. **Create `.env` file:**

   ```powershell
   copy .env.example .env
   ```

4. **Run the frontend:**

   ```powershell
   npm run dev
   ```

   ✅ Frontend should now be running at: http://localhost:5173

---

### Step 3: Configure Firebase Console (2 minutes)

1. **Go to Firebase Console:**

   - URL: https://console.firebase.google.com/
   - Select project: `retireright-lk-41def`

2. **Enable Google Sign-In:**

   - Go to: **Authentication** > **Sign-in method**
   - Click: **Google**
   - Toggle: **Enable**
   - Add your email as Project support email
   - Click: **Save**

3. **Add authorized domains:**
   - Still in **Authentication** > **Settings** > **Authorized domains**
   - `localhost` should already be there
   - For production, add your domain later

---

### Step 4: Test the Application

1. **Open browser:**

   ```
   http://localhost:5173
   ```

2. **You should see:**

   - Login page with "Sign in with Google" button

3. **Click "Sign in with Google":**

   - Google OAuth popup should appear
   - Sign in with your Google account
   - You'll be redirected to the dashboard

4. **Dashboard should show:**
   - Your name and profile picture
   - Logout button
   - Placeholder sections for calculator features

---

## 🔧 Troubleshooting

### Backend Issues

**Error: "Firebase service account file not found"**

- Make sure `firebase-service-account.json` is in the `backend` folder
- Check the file name is exactly: `firebase-service-account.json`

**Error: "Module not found"**

- Make sure virtual environment is activated
- Run: `pip install -r requirements.txt` again

**Port 5000 already in use:**

- Change port in `backend/.env`: `PORT=5001`
- Update frontend `.env`: `VITE_API_URL=http://localhost:5001`

### Frontend Issues

**Error: "Cannot find module"**

- Run: `npm install` again
- Delete `node_modules` and run `npm install`

**Firebase authentication not working:**

- Check Firebase Console > Authentication is enabled
- Verify Google Sign-In is enabled
- Check browser console for error messages

**API calls failing:**

- Make sure backend is running on port 5000
- Check `frontend/.env` has correct `VITE_API_URL`

---

## 📁 Project Files Overview

### Backend Key Files

```
backend/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── config.py             # Configuration settings
│   ├── models.py             # Database models
│   ├── auth.py               # Firebase auth middleware
│   ├── calculations.py       # EPF/ETF calculation logic
│   └── routes/
│       ├── auth.py           # Authentication endpoints
│       ├── calculator.py     # Calculator endpoints
│       └── user.py           # User profile endpoints
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
└── firebase-service-account.json  # (YOU NEED TO ADD THIS)
```

### Frontend Key Files

```
frontend/
├── src/
│   ├── config/
│   │   ├── firebase.ts       # Firebase client configuration
│   │   └── api.ts            # Axios API setup
│   ├── services/
│   │   ├── auth.service.ts   # Authentication service
│   │   ├── calculator.service.ts  # Calculator API calls
│   │   └── user.service.ts   # User API calls
│   ├── store/
│   │   └── authStore.ts      # Authentication state management
│   ├── pages/
│   │   ├── LoginPage.tsx     # Login page with Google sign-in
│   │   └── DashboardPage.tsx # Main dashboard
│   ├── components/
│   │   └── ProtectedRoute.tsx  # Route protection
│   ├── types/
│   │   └── index.ts          # TypeScript types
│   ├── App.tsx               # Main app component
│   └── main.tsx              # Entry point
├── package.json              # Dependencies
├── tsconfig.json             # TypeScript config
├── vite.config.ts            # Vite config
├── tailwind.config.js        # TailwindCSS config
└── .env.example              # Environment variables template
```

---

## 🌟 What Works Now

✅ **Authentication:**

- Google Sign-In with Firebase
- User registration and login
- Session management
- Protected routes
- Logout functionality

✅ **Backend API:**

- `/api/auth/verify` - Verify Firebase tokens
- `/api/auth/me` - Get current user
- `/api/calculator/*` - Calculator endpoints
- `/api/user/*` - User profile endpoints

✅ **Frontend:**

- Login page with Google OAuth
- Dashboard with user info
- Route protection
- API integration setup
- State management

---

## 📈 Next Features to Implement

The authentication is complete! Next, you can implement:

1. **Calculator UI** - Input form for EPF/ETF calculations
2. **Results Display** - Show calculation results with charts
3. **Scenario Comparison** - Compare multiple retirement scenarios
4. **Calculation History** - Save and view past calculations
5. **Profile Management** - Edit salary profile
6. **PDF Export** - Download calculation reports
7. **Charts & Visualizations** - Interactive charts with Recharts

---

## 🚀 Deployment Checklist

When ready to deploy to Digital Ocean:

### Backend:

- [ ] Generate secure `SECRET_KEY` in production `.env`
- [ ] Set `FLASK_ENV=production`
- [ ] Update `FRONTEND_URL` to production URL
- [ ] Setup PostgreSQL (optional, SQLite works too)
- [ ] Configure Gunicorn service
- [ ] Setup Nginx reverse proxy
- [ ] Enable SSL with Let's Encrypt

### Frontend:

- [ ] Update `VITE_API_URL` to production API URL
- [ ] Build production bundle: `npm run build`
- [ ] Upload `dist/` folder to server
- [ ] Configure Nginx static hosting
- [ ] Add production domain to Firebase authorized domains

---

## 📞 Need Help?

If you encounter any issues:

1. Check the error message in the terminal
2. Look at browser console (F12) for frontend errors
3. Review the troubleshooting section above
4. Check Firebase Console for authentication issues
5. Verify all environment variables are set correctly

---

## ✅ Success!

If you can:

1. Run backend on http://localhost:5000 ✅
2. Run frontend on http://localhost:5173 ✅
3. Click "Sign in with Google" ✅
4. See your profile in the dashboard ✅

**Congratulations! Your authentication system is working!** 🎉

Now you can start building the calculator features!
