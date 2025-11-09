# 🚀 Quick Reference - RetireRight LK

## Starting the Application

### Backend

```powershell
cd backend
venv\Scripts\activate
python run.py
```

**URL:** http://localhost:5000

### Frontend

```powershell
cd frontend
npm run dev
```

**URL:** http://localhost:5173

---

## Important Files to Add

### Backend

1. **firebase-service-account.json**

   - Download from Firebase Console
   - Place in: `backend/firebase-service-account.json`

2. **.env**
   - Copy from: `backend/.env.example`
   - Update SECRET_KEY if needed

### Frontend

1. **.env**
   - Copy from: `frontend/.env.example`
   - Default values should work for local development

---

## Firebase Setup Required

1. **Enable Google Sign-In:**

   - Firebase Console > Authentication > Sign-in method
   - Enable Google provider

2. **Download Service Account:**

   - Project Settings > Service Accounts
   - Generate New Private Key

3. **Authorized Domains:**
   - Authentication > Settings > Authorized domains
   - `localhost` should be pre-approved

---

## API Endpoints

### Base URL: http://localhost:5000

#### Authentication

- `POST /api/auth/verify` - Verify Firebase token & create user
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/logout` - Logout user
- `DELETE /api/auth/delete` - Delete account

#### Calculator

- `POST /api/calculator/contributions`

  ```json
  {
    "basicSalary": 75000,
    "employeeEpfRate": 10
  }
  ```

- `POST /api/calculator/retirement-projection`

  ```json
  {
    "currentAge": 28,
    "retirementAge": 60,
    "basicSalary": 75000,
    "employeeEpfRate": 10,
    "annualIncrement": 5,
    "epfInterestRate": 9.5,
    "currentEpfBalance": 500000,
    "inflationRate": 6
  }
  ```

- `POST /api/calculator/scenarios/compare`
  ```json
  {
    "scenarios": [
      {
        "name": "Retire at 55",
        "currentAge": 28,
        "retirementAge": 55,
        "basicSalary": 75000,
        ...
      }
    ]
  }
  ```

#### User Profile

- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update salary profile
- `GET /api/user/calculations` - Get calculation history
- `POST /api/user/calculations` - Save calculation
- `DELETE /api/user/calculations/:id` - Delete calculation

---

## Common Commands

### Backend

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python run.py

# Run with Gunicorn (production)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

### Frontend

```powershell
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type check
npm run type-check

# Lint code
npm run lint
```

---

## EPF/ETF Calculation Details

### Contribution Rates (Sri Lanka)

- Employee EPF: **8% or 10%** of basic salary
- Employer EPF: **12%** of basic salary
- Employer ETF: **3%** of basic salary

### Default Assumptions

- EPF Interest Rate: **9.5%** per annum
- Inflation Rate: **6%** per annum
- Salary Increment: **5%** per annum
- Retirement Age: **60 years**

### Calculation Formula

**Monthly Contribution:**

```
Employee EPF = Basic Salary × (8% or 10%)
Employer EPF = Basic Salary × 12%
Employer ETF = Basic Salary × 3%
Total EPF = Employee EPF + Employer EPF
```

**Future Value with Compound Interest:**

```
FV = P × [((1 + r)^n - 1) / r]

Where:
P = Monthly contribution
r = Monthly interest rate (9.5% ÷ 12)
n = Number of months to retirement
```

**Inflation-Adjusted Value:**

```
Real Value = Nominal Value / (1 + inflation_rate)^years
```

---

## Project Structure

```
RetireRight LK/
├── backend/                  # Flask API
│   ├── app/
│   │   ├── __init__.py      # App factory
│   │   ├── config.py        # Configuration
│   │   ├── models.py        # Database models
│   │   ├── auth.py          # Firebase middleware
│   │   ├── calculations.py  # EPF calculations
│   │   └── routes/          # API endpoints
│   ├── run.py               # Entry point
│   └── requirements.txt     # Dependencies
│
└── frontend/                # React + TypeScript
    ├── src/
    │   ├── config/          # Firebase & API config
    │   ├── services/        # API services
    │   ├── store/           # State management
    │   ├── pages/           # Page components
    │   ├── components/      # Reusable components
    │   └── types/           # TypeScript types
    ├── package.json         # Dependencies
    └── vite.config.ts       # Vite config
```

---

## Tech Stack

**Backend:**

- Flask 3.0
- Firebase Admin SDK
- SQLAlchemy
- NumPy
- Gunicorn

**Frontend:**

- React 18
- TypeScript
- Vite
- TailwindCSS
- Zustand
- Axios
- Recharts
- Lucide React

---

## Firebase Configuration

**Project Details:**

- Project ID: `retireright-lk-41def`
- Auth Domain: `retireright-lk-41def.firebaseapp.com`
- API Key: `AIzaSyASPnWP5H_MYqS55U_iOkR4eWb0rEbpyzI`

**Location:** `frontend/src/config/firebase.ts`

---

## Environment Variables

### Backend (.env)

```env
SECRET_KEY=your-secret-key
FLASK_ENV=development
FIREBASE_PROJECT_ID=retireright-lk-41def
FRONTEND_URL=http://localhost:5173
```

### Frontend (.env)

```env
VITE_API_URL=http://localhost:5000
```

---

## Deployment Checklist

### Digital Ocean Backend

- [ ] Setup Droplet (Ubuntu 22.04)
- [ ] Install Python, pip, venv, nginx
- [ ] Clone repository
- [ ] Setup virtual environment
- [ ] Install dependencies
- [ ] Configure .env (production values)
- [ ] Add firebase-service-account.json
- [ ] Setup Gunicorn service
- [ ] Configure Nginx reverse proxy
- [ ] Enable SSL (Let's Encrypt)

### Digital Ocean Frontend

- [ ] Build production: `npm run build`
- [ ] Upload `dist/` folder
- [ ] Configure Nginx static hosting
- [ ] Update API URL in .env
- [ ] Enable SSL
- [ ] Add domain to Firebase authorized domains

---

## Troubleshooting

**Backend won't start:**

- Check virtual environment is activated
- Verify all dependencies installed
- Check firebase-service-account.json exists
- Look for port conflicts (change PORT in .env)

**Frontend won't start:**

- Delete node_modules, run `npm install`
- Check .env file exists
- Verify backend is running

**Google Sign-In fails:**

- Enable Google provider in Firebase Console
- Check authorized domains in Firebase
- Verify firebaseConfig in firebase.ts
- Check browser console for errors

**API calls fail:**

- Verify backend is running
- Check VITE_API_URL in frontend .env
- Check CORS settings in backend
- Look for errors in browser console

---

## Contact

**Developer:** Chamath Dilshan
**GitHub:** [@ChamathDilshanC](https://github.com/ChamathDilshanC)
**Repository:** [RetireRight-LK](https://github.com/ChamathDilshanC/RetireRight-LK)

---

**Made with ❤️ for Sri Lankan workers**
