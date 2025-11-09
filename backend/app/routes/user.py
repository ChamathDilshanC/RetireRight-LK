"""
User profile and calculation history routes
"""
from flask import Blueprint, request, jsonify
from app.auth import require_auth
from app.models import User, SalaryProfile, CalculationHistory, db
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)

bp = Blueprint('user', __name__, url_prefix='/api/user')


@bp.route('/profile', methods=['GET'])
@require_auth
def get_profile(current_user):
    """Get user profile and salary information"""
    try:
        user = User.query.filter_by(firebase_uid=current_user['uid']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        salary_profile = SalaryProfile.query.filter_by(user_id=user.id).first()

        return jsonify({
            'success': True,
            'data': {
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                    'profilePicture': user.profile_picture
                },
                'salaryProfile': salary_profile.to_dict() if salary_profile else None
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
        user = User.query.filter_by(firebase_uid=current_user['uid']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()
        salary_profile = SalaryProfile.query.filter_by(user_id=user.id).first()

        if not salary_profile:
            salary_profile = SalaryProfile(user_id=user.id)
            db.session.add(salary_profile)

        # Update fields
        if 'currentBasicSalary' in data:
            salary_profile.current_basic_salary = data['currentBasicSalary']
        if 'age' in data:
            salary_profile.age = data['age']
        if 'yearsOfService' in data:
            salary_profile.years_of_service = data['yearsOfService']
        if 'retirementAge' in data:
            salary_profile.retirement_age = data['retirementAge']
        if 'epfRate' in data:
            salary_profile.epf_rate = data['epfRate']
        if 'expectedSalaryIncrement' in data:
            salary_profile.expected_salary_increment = data['expectedSalaryIncrement']
        if 'currentEpfBalance' in data:
            salary_profile.current_epf_balance = data['currentEpfBalance']

        db.session.commit()

        return jsonify({
            'success': True,
            'data': salary_profile.to_dict()
        }), 200

    except Exception as e:
        logger.error(f"Update profile error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500


@bp.route('/calculations', methods=['GET'])
@require_auth
def get_calculations(current_user):
    """Get user's calculation history"""
    try:
        user = User.query.filter_by(firebase_uid=current_user['uid']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        calculations = CalculationHistory.query.filter_by(user_id=user.id)\
            .order_by(CalculationHistory.created_at.desc())\
            .limit(50)\
            .all()

        return jsonify({
            'success': True,
            'data': [calc.to_dict() for calc in calculations]
        }), 200

    except Exception as e:
        logger.error(f"Get calculations error: {str(e)}")
        return jsonify({'error': 'Failed to get calculations', 'message': str(e)}), 500


@bp.route('/calculations', methods=['POST'])
@require_auth
def save_calculation(current_user):
    """Save a calculation to history"""
    try:
        user = User.query.filter_by(firebase_uid=current_user['uid']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.get_json()

        calculation = CalculationHistory(
            user_id=user.id,
            calculation_type=data.get('calculationType', 'retirement_projection'),
            inputs=json.dumps(data.get('inputs', {})),
            results=json.dumps(data.get('results', {}))
        )

        db.session.add(calculation)
        db.session.commit()

        return jsonify({
            'success': True,
            'data': calculation.to_dict()
        }), 201

    except Exception as e:
        logger.error(f"Save calculation error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to save calculation', 'message': str(e)}), 500


@bp.route('/calculations/<int:calc_id>', methods=['DELETE'])
@require_auth
def delete_calculation(current_user, calc_id):
    """Delete a calculation from history"""
    try:
        user = User.query.filter_by(firebase_uid=current_user['uid']).first()

        if not user:
            return jsonify({'error': 'User not found'}), 404

        calculation = CalculationHistory.query.filter_by(
            id=calc_id,
            user_id=user.id
        ).first()

        if not calculation:
            return jsonify({'error': 'Calculation not found'}), 404

        db.session.delete(calculation)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Calculation deleted successfully'
        }), 200

    except Exception as e:
        logger.error(f"Delete calculation error: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete calculation', 'message': str(e)}), 500
