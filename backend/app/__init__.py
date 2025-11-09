"""
RetireRight LK - EPF/ETF Calculator Backend
Flask application factory
"""
from flask import Flask
from flask_cors import CORS
from app.config import Config
from app.models import db
import firebase_admin
from firebase_admin import credentials
import os


def create_app(config_class=Config):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize database
    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Enable CORS for frontend communication
    CORS(app, resources={
        r"/api/*": {
            "origins": app.config['FRONTEND_URL'],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Initialize Firebase Admin SDK
    try:
        # Check if Firebase is already initialized
        firebase_admin.get_app()
    except ValueError:
        # Try to use base64-encoded service account from environment variable (production)
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
                print("⚠️ Warning: Firebase service account not configured. Authentication will not work.")

    # Register blueprints
    from app.routes import auth, calculator, user
    app.register_blueprint(auth.bp)
    app.register_blueprint(calculator.bp)
    app.register_blueprint(user.bp)

    # Health check route
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'service': 'RetireRight LK API'}, 200

    return app
