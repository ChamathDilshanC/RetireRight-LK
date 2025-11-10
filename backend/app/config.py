"""
Configuration settings for the Flask application
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'

    # Firebase Configuration
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID', 'retireright-lk-41def')

    # Frontend URL for CORS
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')

    # Database Configuration (SQLite for MVP)
    # No persistent relational database is used. The app relies on Firebase for
    # authentication and keeps profiles/history in-memory (non-persistent).

    # EPF Configuration (Sri Lanka)
    EPF_EMPLOYEE_RATE_OPTIONS = [8, 10]  # Percentage options
    EPF_EMPLOYER_RATE = 12  # Percentage
    ETF_EMPLOYER_RATE = 3   # Percentage

    # Default assumptions
    DEFAULT_EPF_INTEREST_RATE = 9.5  # Annual percentage
    DEFAULT_INFLATION_RATE = 6.0     # Annual percentage
    DEFAULT_SALARY_INCREMENT = 5.0    # Annual percentage
    DEFAULT_RETIREMENT_AGE = 60

    # Retirement age options
    RETIREMENT_AGE_OPTIONS = [55, 60, 65]


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    # Override with production values
    SECRET_KEY = os.environ.get('SECRET_KEY')
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://your-domain.com')


class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    # No DB settings for testing by default


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
