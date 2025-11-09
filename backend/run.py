"""
Run the Flask application
"""
import os
from app import create_app
from app.config import config

# Get environment from environment variable, default to development
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(config.get(env, config['default']))

if __name__ == '__main__':
    # Run the app
    port = int(os.environ.get('PORT', 5000))
    debug = env == 'development'

    print(f"Starting RetireRight LK API on port {port}")
    print(f"Environment: {env}")
    print(f"Debug mode: {debug}")

    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
