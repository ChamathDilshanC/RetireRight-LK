"""
Firebase Authentication middleware and utilities
"""
from functools import wraps
from flask import request, jsonify
from firebase_admin import auth as firebase_auth
import logging

logger = logging.getLogger(__name__)


def verify_firebase_token(id_token):
    """
    Verify Firebase ID token and return decoded token

    Args:
        id_token: Firebase ID token from client

    Returns:
        dict: Decoded token containing user information

    Raises:
        Exception: If token verification fails
    """
    try:
        decoded_token = firebase_auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        raise Exception(f"Invalid authentication token: {str(e)}")


def require_auth(f):
    """
    Decorator to require Firebase authentication for routes

    Usage:
        @bp.route('/protected')
        @require_auth
        def protected_route(current_user):
            # current_user contains decoded token data
            return {'message': f"Hello {current_user['email']}"}
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return jsonify({
                'error': 'No authorization header',
                'message': 'Authorization header is required'
            }), 401

        # Extract token (format: "Bearer <token>")
        try:
            token = auth_header.split(' ')[1]
        except IndexError:
            return jsonify({
                'error': 'Invalid authorization header',
                'message': 'Authorization header must be in format: Bearer <token>'
            }), 401

        # Verify token
        try:
            decoded_token = verify_firebase_token(token)
            # Pass decoded token to route handler
            return f(decoded_token, *args, **kwargs)
        except Exception as e:
            return jsonify({
                'error': 'Authentication failed',
                'message': str(e)
            }), 401

    return decorated_function


def get_user_from_token(id_token):
    """
    Extract user information from Firebase token

    Args:
        id_token: Firebase ID token

    Returns:
        dict: User information including uid, email, name, etc.
    """
    try:
        decoded_token = verify_firebase_token(id_token)

        user_info = {
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email'),
            'email_verified': decoded_token.get('email_verified', False),
            'name': decoded_token.get('name'),
            'picture': decoded_token.get('picture'),
            'firebase': decoded_token
        }

        return user_info
    except Exception as e:
        logger.error(f"Failed to extract user info: {str(e)}")
        return None


def validate_firebase_user(uid):
    """
    Validate if a Firebase user exists

    Args:
        uid: Firebase user ID

    Returns:
        bool: True if user exists, False otherwise
    """
    try:
        firebase_auth.get_user(uid)
        return True
    except firebase_auth.UserNotFoundError:
        return False
    except Exception as e:
        logger.error(f"Error validating user: {str(e)}")
        return False
