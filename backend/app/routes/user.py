"""
User profile and calculation history routes
"""
from flask import Blueprint, request, jsonify
from app.auth import require_auth
from datetime import datetime
import logging
import json

# In-memory stores (non-persistent). Removing SQLAlchemy persistence as requested.
# Keyed by Firebase UID. These reset when the app restarts.
salary_profiles = {}  # uid -> profile dict
calculations_store = {}  # uid -> list of calculation dicts
_calc_id_counter = 1

logger = logging.getLogger(__name__)

bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/profile', methods=['GET'])
@require_auth
def get_profile(current_user):
    """Get user profile and salary information"""
    try:
        uid = current_user.get('uid')

        if not uid:
            return jsonify({'error': 'User not found'}), 404

        profile = salary_profiles.get(uid)

        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'id': None,
                    'email': current_user.get('email'),
                    'name': current_user.get('name'),
                    'profilePicture': current_user.get('picture')
                },
                'salaryProfile': profile
            }
        }), 200

    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'error': 'Failed to get profile', 'message': str(e)}), 500


@bp.route('/profile', methods=['PUT'])
@require_auth
def update_profile(current_user):
    """Update or create salary profile"""
    try:
        uid = current_user.get('uid')

        if not uid:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json() or {}

        # Build or update in-memory profile
        now = datetime.utcnow()
        profile = salary_profiles.get(uid, {
            'id': None,
            'currentBasicSalary': None,
            'age': None,
            'yearsOfService': None,
            'retirementAge': 60,
            'epfRate': 10,
            'expectedSalaryIncrement': 5.0,
            'currentEpfBalance': 0.0,
            'createdAt': now.isoformat(),
            'updatedAt': now.isoformat()
        })

        # Update fields
        if 'currentBasicSalary' in data:
            profile['currentBasicSalary'] = data['currentBasicSalary']
        if 'age' in data:
            profile['age'] = data['age']
        if 'yearsOfService' in data:
            profile['yearsOfService'] = data['yearsOfService']
        if 'retirementAge' in data:
            profile['retirementAge'] = data['retirementAge']
        if 'epfRate' in data:
            profile['epfRate'] = data['epfRate']
        if 'expectedSalaryIncrement' in data:
            profile['expectedSalaryIncrement'] = data['expectedSalaryIncrement']
        if 'currentEpfBalance' in data:
            profile['currentEpfBalance'] = data['currentEpfBalance']

        profile['updatedAt'] = datetime.utcnow().isoformat()
        salary_profiles[uid] = profile

        return jsonify({
            'success': True,
            'data': profile
        }), 200

    except Exception as e:
        logger.error(f"Update profile error: {str(e)}")
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500


@bp.route('/calculations', methods=['GET'])
@require_auth
def get_calculations(current_user):
    """Get user's calculation history"""
    try:
        uid = current_user.get('uid')

        if not uid:
            return jsonify({'error': 'User not found'}), 404

        items = calculations_store.get(uid, [])
        # sort by createdAt desc and limit 50
        sorted_items = sorted(items, key=lambda x: x.get('createdAt', ''), reverse=True)[:50]

        return jsonify({
            'success': True,
            'data': sorted_items
        }), 200

    except Exception as e:
        logger.error(f"Get calculations error: {str(e)}")
        return jsonify({'error': 'Failed to get calculations', 'message': str(e)}), 500


@bp.route('/calculations', methods=['POST'])
@require_auth
def save_calculation(current_user):
    """Save a calculation to history"""
    try:
        global _calc_id_counter
        uid = current_user.get('uid')

        if not uid:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json() or {}

        calc = {
            'id': _calc_id_counter,
            'userId': None,
            'calculationType': data.get('calculationType', 'retirement_projection'),
            'inputs': data.get('inputs', {}),
            'results': data.get('results', {}),
            'createdAt': datetime.utcnow().isoformat()
        }

        _calc_id_counter += 1

        calculations_store.setdefault(uid, []).append(calc)

        return jsonify({
            'success': True,
            'data': calc
        }), 201

    except Exception as e:
        logger.error(f"Save calculation error: {str(e)}")
        return jsonify({'error': 'Failed to save calculation', 'message': str(e)}), 500


@bp.route('/calculations/<int:calc_id>', methods=['DELETE'])
@require_auth
def delete_calculation(current_user, calc_id):
    """Delete a calculation from history"""
    try:
        uid = current_user.get('uid')

        if not uid:
            return jsonify({'error': 'User not found'}), 404

        items = calculations_store.get(uid, [])
        match = None
        for item in items:
            if int(item.get('id')) == int(calc_id):
                match = item
                break

        if not match:
            return jsonify({'error': 'Calculation not found'}), 404

        items.remove(match)

        return jsonify({
            'success': True,
            'message': 'Calculation deleted successfully'
        }), 200

    except Exception as e:
        logger.error(f"Delete calculation error: {str(e)}")
        return jsonify({'error': 'Failed to delete calculation', 'message': str(e)}), 500
