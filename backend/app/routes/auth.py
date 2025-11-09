"""
Authentication routes for Firebase integration
"""
from flask import Blueprint, request, jsonify
from app.auth import verify_firebase_token, get_user_from_token, require_auth
from app.models import User, db
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

        # Check if user exists in database
        user = User.query.filter_by(firebase_uid=user_info['uid']).first()

        if not user:
            # Create new user
            user = User(
                firebase_uid=user_info['uid'],
                email=user_info['email'],
                name=user_info['name'],
                profile_picture=user_info.get('picture'),
                email_verified=user_info['email_verified']
            )
            db.session.add(user)
            db.session.commit()
            logger.info(f"Created new user: {user.email}")
        else:
            # Update existing user info
            user.last_login = datetime.utcnow()
            user.name = user_info['name']
            user.profile_picture = user_info.get('picture')
            user.email_verified = user_info['email_verified']
            db.session.commit()
            logger.info(f"User logged in: {user.email}")

        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'uid': user.firebase_uid,
                'email': user.email,
                'name': user.name,
                'profilePicture': user.profile_picture,
                'emailVerified': user.email_verified,
                'createdAt': user.created_at.isoformat(),
                'lastLogin': user.last_login.isoformat() if user.last_login else None
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
        user = User.query.filter_by(firebase_uid=current_user['uid']).first()

        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'User does not exist in database'
            }), 404

        return jsonify({
            'user': {
                'id': user.id,
                'uid': user.firebase_uid,
                'email': user.email,
                'name': user.name,
                'profilePicture': user.profile_picture,
                'emailVerified': user.email_verified,
                'createdAt': user.created_at.isoformat(),
                'lastLogin': user.last_login.isoformat() if user.last_login else None
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
        user = User.query.filter_by(firebase_uid=current_user['uid']).first()

        if not user:
            return jsonify({
                'error': 'User not found',
                'message': 'User does not exist in database'
            }), 404

        # Delete user from database
        db.session.delete(user)
        db.session.commit()

        logger.info(f"User account deleted: {user.email}")

        return jsonify({
            'success': True,
            'message': 'Account deleted successfully'
        }), 200

    except Exception as e:
        logger.error(f"Delete account error: {str(e)}")
        return jsonify({
            'error': 'Failed to delete account',
            'message': str(e)
        }), 500
