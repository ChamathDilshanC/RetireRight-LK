# RetireRight LK - Backend

Backend API for the EPF/ETF Retirement Calculator for Sri Lanka.

## Tech Stack

- **Framework**: Flask 3.0
- **Authentication**: Firebase Admin SDK
- **Database**: SQLAlchemy (SQLite for dev, PostgreSQL for production)
- **API**: RESTful API with JWT authentication

## Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update values:

```bash
cp .env.example .env
```

Update the following in `.env`:

- `SECRET_KEY`: Generate a secure random key
- `FRONTEND_URL`: Your frontend URL (default: http://localhost:5173)

### 4. Firebase Setup

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Navigate to Project Settings > Service Accounts
3. Click "Generate New Private Key"
4. Save the JSON file as `firebase-service-account.json` in the `backend` folder

### 5. Run the Application

```bash
# Development
python run.py

# Production (with Gunicorn)
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

The API will be available at: `http://localhost:5000`

## API Endpoints

### Authentication

- `POST /api/auth/verify` - Verify Firebase token and create/update user
- `GET /api/auth/me` - Get current user info (requires auth)
- `POST /api/auth/logout` - Logout user
- `DELETE /api/auth/delete` - Delete user account

### Calculator

- `POST /api/calculator/contributions` - Calculate monthly EPF/ETF contributions
- `POST /api/calculator/retirement-projection` - Calculate retirement savings projection
- `POST /api/calculator/scenarios/compare` - Compare multiple scenarios

### User Profile

- `GET /api/user/profile` - Get user profile (requires auth)
- `PUT /api/user/profile` - Update salary profile (requires auth)
- `GET /api/user/calculations` - Get calculation history (requires auth)
- `POST /api/user/calculations` - Save calculation (requires auth)
- `DELETE /api/user/calculations/:id` - Delete calculation (requires auth)

### Health Check

- `GET /health` - API health check

## Project Structure

```
backend/
├── app/
│   ├── __init__.py          # App factory
│   ├── config.py            # Configuration
│   ├── models.py            # Database models
│   ├── auth.py              # Firebase auth middleware
│   ├── calculations.py      # EPF/ETF calculations
│   └── routes/
│       ├── auth.py          # Auth routes
│       ├── calculator.py    # Calculator routes
│       └── user.py          # User routes
├── data/                    # SQLite database (auto-created)
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

## Database Schema

### Users

- `id`, `firebase_uid`, `email`, `name`, `profile_picture`, `email_verified`, `created_at`, `last_login`

### Salary Profiles

- `id`, `user_id`, `current_basic_salary`, `age`, `years_of_service`, `retirement_age`, `epf_rate`, `expected_salary_increment`, `current_epf_balance`, `created_at`, `updated_at`

### Calculation History

- `id`, `user_id`, `calculation_type`, `inputs` (JSON), `results` (JSON), `created_at`

### EPF Rate History

- `id`, `year`, `interest_rate`, `inflation_rate`, `created_at`

## Deployment (Digital Ocean)

### 1. Create Droplet

- Ubuntu 22.04 LTS
- Minimum 1GB RAM
- Add your SSH key

### 2. Install Dependencies

```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

### 3. Clone Repository

```bash
git clone https://github.com/ChamathDilshanC/RetireRight-LK.git
cd RetireRight-LK/backend
```

### 4. Setup Application

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 5. Configure Environment

```bash
cp .env.example .env
nano .env  # Update with production values
```

### 6. Add Firebase Service Account

Upload `firebase-service-account.json` to the backend folder.

### 7. Setup Gunicorn Service

Create `/etc/systemd/system/retireright.service`:

```ini
[Unit]
Description=RetireRight LK API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/RetireRight-LK/backend
Environment="PATH=/path/to/RetireRight-LK/backend/venv/bin"
ExecStart=/path/to/RetireRight-LK/backend/venv/bin/gunicorn -w 4 -b 127.0.0.1:5000 "app:create_app()"

[Install]
WantedBy=multi-user.target
```

Start the service:

```bash
sudo systemctl start retireright
sudo systemctl enable retireright
```

### 8. Configure Nginx

Create `/etc/nginx/sites-available/retireright`:

```nginx
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable and restart:

```bash
sudo ln -s /etc/nginx/sites-available/retireright /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 9. SSL Certificate (Optional)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.your-domain.com
```

## Testing

```bash
# Run tests
pytest

# With coverage
pytest --cov=app
```

## License

MIT License - See LICENSE file for details
