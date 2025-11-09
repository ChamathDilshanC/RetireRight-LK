# RetireRight LK - Frontend

Frontend application for the EPF/ETF Retirement Calculator for Sri Lanka.

## Tech Stack

- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: Zustand
- **Authentication**: Firebase Authentication (Google Sign-In)
- **HTTP Client**: Axios
- **Charts**: Recharts
- **Icons**: Lucide React
- **Notifications**: React Hot Toast
- **Routing**: React Router DOM

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

Update the API URL in `.env`:

```
VITE_API_URL=http://localhost:5000
```

### 3. Firebase Configuration

The Firebase configuration is already set up in `src/config/firebase.ts` with your credentials:

- Project ID: `retireright-lk-41def`
- Auth Domain: `retireright-lk-41def.firebaseapp.com`

### 4. Run Development Server

```bash
npm run dev
```

The application will be available at: `http://localhost:5173`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Project Structure

```
frontend/
├── src/
│   ├── components/         # Reusable components
│   │   └── ProtectedRoute.tsx
│   ├── config/            # Configuration files
│   │   ├── firebase.ts    # Firebase setup
│   │   └── api.ts         # Axios setup
│   ├── pages/             # Page components
│   │   ├── LoginPage.tsx
│   │   └── DashboardPage.tsx
│   ├── services/          # API services
│   │   ├── auth.service.ts
│   │   ├── calculator.service.ts
│   │   └── user.service.ts
│   ├── store/             # State management
│   │   └── authStore.ts
│   ├── types/             # TypeScript types
│   │   └── index.ts
│   ├── App.tsx            # Main app component
│   ├── main.tsx           # Entry point
│   └── index.css          # Global styles
├── public/                # Static assets
├── index.html            # HTML template
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
├── vite.config.ts        # Vite config
├── tailwind.config.js    # Tailwind config
└── README.md             # This file
```

## Features

### Authentication

- ✅ Google Sign-In with Firebase
- ✅ Protected routes
- ✅ Automatic token refresh
- ✅ User session management
- ✅ Backend token verification

### Planned Features

- [ ] EPF/ETF contribution calculator
- [ ] Retirement projection calculator
- [ ] Scenario comparison
- [ ] Interactive charts and visualizations
- [ ] Calculation history
- [ ] User profile management
- [ ] PDF report generation
- [ ] Mobile responsive design

## API Integration

The frontend communicates with the backend API through the following services:

### Auth Service (`src/services/auth.service.ts`)

- `signInWithGoogle()` - Google OAuth sign-in
- `signOut()` - User logout
- `getCurrentUser()` - Get current user data
- `deleteAccount()` - Delete user account

### Calculator Service (`src/services/calculator.service.ts`)

- `calculateContributions()` - Calculate monthly contributions
- `calculateRetirementProjection()` - Project retirement savings
- `compareScenarios()` - Compare multiple scenarios

### User Service (`src/services/user.service.ts`)

- `getUserProfile()` - Get user profile
- `updateSalaryProfile()` - Update salary information
- `getCalculationHistory()` - Get saved calculations
- `saveCalculation()` - Save calculation to history
- `deleteCalculation()` - Delete calculation

## State Management

Using Zustand for state management:

### Auth Store

- User authentication state
- Login/logout actions
- Firebase auth listener
- Token management

## Deployment

### Build for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` folder.

### Deploy to Digital Ocean

#### Option 1: Static Hosting (App Platform)

1. Connect your GitHub repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Set environment variable: `VITE_API_URL=https://api.your-domain.com`

#### Option 2: Droplet with Nginx

1. Build the application:

```bash
npm run build
```

2. Upload `dist/` folder to your droplet

3. Configure Nginx:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    root /var/www/retireright/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

4. Enable HTTPS with Let's Encrypt:

```bash
sudo certbot --nginx -d your-domain.com
```

## Environment Variables

- `VITE_API_URL` - Backend API URL

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

MIT License - See LICENSE file for details
