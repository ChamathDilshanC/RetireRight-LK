# RetireRight LK - EPF/ETF Retirement Calculator

A comprehensive retirement planning calculator specifically designed for Sri Lankan workers. Calculate Employee Provident Fund (EPF) and Employee Trust Fund (ETF) contributions, project retirement savings with inflation adjustment, and plan your financial future.

## 🚀 Features

- **Firebase Google Authentication** - Secure login with your Google account
- **EPF/ETF Calculator** - Accurate calculation of monthly contributions
- **Retirement Projections** - Project your savings with compound interest
- **Inflation Adjustment** - See real purchasing power at retirement
- **Scenario Comparison** - Compare different retirement strategies
- **Calculation History** - Save and track your calculations
- **User Profiles** - Store and manage your salary information

## 📁 Project Structure

```
RetireRight-LK/
├── backend/              # Flask API server
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── models.py
│   │   ├── auth.py
│   │   ├── calculations.py
│   │   └── routes/
│   ├── requirements.txt
│   ├── run.py
│   └── README.md
├── frontend/             # React + TypeScript app
│   ├── src/
│   │   ├── components/
│   │   ├── config/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── store/
│   │   └── types/
│   ├── package.json
│   └── README.md
└── README.md            # This file
```

## 🛠️ Tech Stack

### Backend

- **Framework**: Flask 3.0
- **Authentication**: Firebase Admin SDK
- **Database**: No persistent DB (in-memory stores used). Firebase is used for auth.
- **Calculations**: NumPy

### Frontend

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: Zustand
- **Authentication**: Firebase Auth (Google)
- **HTTP Client**: Axios
- **Charts**: Recharts

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+
- Firebase account
- Git

### Backend Setup

1. **Navigate to backend:**

   ```powershell
   cd backend
   ```

2. **Create virtual environment:**

   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Configure environment:**

   ```powershell
   copy .env.example .env
   ```

5. **Add Firebase service account:**

   - Download from Firebase Console > Project Settings > Service Accounts
   - Save as `firebase-service-account.json` in backend folder

6. **Run server:**
   ```powershell
   python run.py
   ```

### Frontend Setup

1. **Navigate to frontend:**

   ```powershell
   cd frontend
   ```

2. **Install dependencies:**

   ```powershell
   npm install
   ```

3. **Configure environment:**

   ```powershell
   copy .env.example .env
   ```

4. **Run development server:**
   ```powershell
   npm run dev
   ```

## 📊 API Endpoints

### Authentication

- `POST /api/auth/verify` - Verify Firebase token
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout
- `DELETE /api/auth/delete` - Delete account

### Calculator

- `POST /api/calculator/contributions` - Calculate monthly contributions
- `POST /api/calculator/retirement-projection` - Project retirement savings
- `POST /api/calculator/scenarios/compare` - Compare scenarios

### User

- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update profile
- `GET /api/user/calculations` - Get calculation history
- `POST /api/user/calculations` - Save calculation
- `DELETE /api/user/calculations/:id` - Delete calculation

## 👨‍💻 Developer

**Chamath Dilshan**

- GitHub: [@ChamathDilshanC](https://github.com/ChamathDilshanC)
- Repository: [RetireRight-LK](https://github.com/ChamathDilshanC/RetireRight-LK)

---

**Made with ❤️ for Sri Lankan workers**
