"""
Authentication routes for Firebase integration
"""
from flask import Blueprint, request, jsonify
from app.auth import verify_firebase_token, get_user_from_token, require_auth
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@bp.route('/verify', methods=['POST'])
def verify_token():
    """
    Verify Firebase token and create/update user in database

    Request body:
        {
            "idToken": "firebase-id-token"
        }

    Returns:
        User information and verification status
    """
    try:
        data = request.get_json()
        id_token = data.get('idToken')

        if not id_token:
            return jsonify({
                'error': 'Missing token',
                'message': 'idToken is required'
            }), 400

        # Verify token and get user info
        user_info = get_user_from_token(id_token)

        if not user_info:
            return jsonify({
                'error': 'Invalid token',
                'message': 'Failed to verify token'
            }), 401

        # No persistent DB: return the verified user info directly.
        # Clients should treat this as non-persistent profile data.
        now = datetime.utcnow()
        return jsonify({
            'success': True,
            'user': {
                'id': None,
                'uid': user_info['uid'],
                'email': user_info.get('email'),
                'name': user_info.get('name'),
                'profilePicture': user_info.get('picture'),
                'emailVerified': user_info.get('email_verified', False),
                'createdAt': now.isoformat(),
                'lastLogin': now.isoformat()
            }
        }), 200

    except Exception as e:
        logger.error(f"Token verification error: {str(e)}")
        return jsonify({
            'error': 'Verification failed',
            'message': str(e)
        }), 500


@bp.route('/me', methods=['GET'])
@require_auth
def get_current_user(current_user):
    """
    Get current authenticated user information

    Requires Authorization header with Firebase token

    Returns:
        Current user information
    """
    try:
        # No DB: return info from the decoded Firebase token
        return jsonify({
            'user': {
                'id': None,
                'uid': current_user.get('uid'),
                'email': current_user.get('email'),
                'name': current_user.get('name'),
                'profilePicture': current_user.get('picture'),
                'emailVerified': current_user.get('email_verified', False),
                'createdAt': None,
                'lastLogin': None
            }
        }), 200

    except Exception as e:
        logger.error(f"Get current user error: {str(e)}")
        return jsonify({
            'error': 'Failed to get user',
            'message': str(e)
        }), 500


@bp.route('/logout', methods=['POST'])
@require_auth
def logout(current_user):
    """
    Logout endpoint (mainly for logging purposes)
    Actual token invalidation happens on client side

    Returns:
        Success message
    """
    try:
        logger.info(f"User logged out: {current_user.get('email')}")
        return jsonify({
            'success': True,
            'message': 'Logged out successfully'
        }), 200
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return jsonify({
            'error': 'Logout failed',
            'message': str(e)
        }), 500


@bp.route('/delete', methods=['DELETE'])
@require_auth
def delete_account(current_user):
    """
    Delete user account

    Requires Authorization header with Firebase token

    Returns:
        Success message
    """
    try:
        # No DB: nothing to delete locally. If you want to delete the Firebase account,
        # that must be done via Firebase Admin SDK (not performed here).
        logger.info(f"Requested account delete for UID: {current_user.get('uid')}")
        return jsonify({
            'success': True,
            'message': 'Account deletion is not backed by a local DB. If needed, delete in Firebase.'
        }), 200

    except Exception as e:
        logger.error(f"Delete account error: {str(e)}")
        return jsonify({
            'error': 'Failed to delete account',
            'message': str(e)
        }), 500
