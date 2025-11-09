"""
Calculator routes for EPF/ETF calculations
"""
from flask import Blueprint, request, jsonify
from app.auth import require_auth
from app.calculations import (
    calculate_monthly_contributions,
    calculate_retirement_savings,
    calculate_purchasing_power,
    calculate_monthly_pension
)
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('calculator', __name__, url_prefix='/api/calculator')


@bp.route('/contributions', methods=['POST'])
def contributions():
    """
    Calculate monthly EPF/ETF contributions

    Request body:
        {
            "basicSalary": 75000,
            "employeeEpfRate": 10
        }

    Returns:
        Breakdown of monthly contributions
    """
    try:
        data = request.get_json()
        basic_salary = data.get('basicSalary')
        employee_rate = data.get('employeeEpfRate', 10)

        if not basic_salary:
            return jsonify({
                'error': 'Missing required field',
                'message': 'basicSalary is required'
            }), 400

        result = calculate_monthly_contributions(basic_salary, employee_rate)

        return jsonify({
            'success': True,
            'data': result
        }), 200

    except Exception as e:
        logger.error(f"Contributions calculation error: {str(e)}")
        return jsonify({
            'error': 'Calculation failed',
            'message': str(e)
        }), 500


@bp.route('/retirement-projection', methods=['POST'])
def retirement_projection():
    """
    Calculate retirement savings projection

    Request body:
        {
            "currentAge": 28,
            "retirementAge": 60,
            "basicSalary": 75000,
            "employeeEpfRate": 10,
            "annualIncrement": 5,
            "epfInterestRate": 9.5,
            "currentEpfBalance": 500000,
            "inflationRate": 6
        }

    Returns:
        Detailed retirement projection with yearly breakdown
    """
    try:
        data = request.get_json()

        # Required fields
        required_fields = ['currentAge', 'retirementAge', 'basicSalary']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': 'Missing required field',
                    'message': f'{field} is required'
                }), 400

        # Calculate retirement savings
        savings_result = calculate_retirement_savings(
            current_age=data['currentAge'],
            retirement_age=data['retirementAge'],
            basic_salary=data['basicSalary'],
            employee_epf_rate=data.get('employeeEpfRate', 10),
            annual_increment=data.get('annualIncrement', 5),
            epf_interest_rate=data.get('epfInterestRate', 9.5),
            current_epf_balance=data.get('currentEpfBalance', 0)
        )

        # Calculate purchasing power
        years_to_retirement = data['retirementAge'] - data['currentAge']
        purchasing_power = calculate_purchasing_power(
            savings_result['final_balance'],
            years_to_retirement,
            data.get('inflationRate', 6)
        )

        # Calculate monthly pension options
        monthly_pension_20y = calculate_monthly_pension(
            savings_result['final_balance'],
            data.get('epfInterestRate', 9.5),
            20
        )

        monthly_pension_25y = calculate_monthly_pension(
            savings_result['final_balance'],
            data.get('epfInterestRate', 9.5),
            25
        )

        return jsonify({
            'success': True,
            'data': {
                'finalBalance': savings_result['final_balance'],
                'yearlyBreakdown': savings_result['yearly_breakdown'],
                'purchasingPower': purchasing_power,
                'monthlyPensionOptions': {
                    'twentyYears': monthly_pension_20y,
                    'twentyFiveYears': monthly_pension_25y
                }
            }
        }), 200

    except Exception as e:
        logger.error(f"Retirement projection error: {str(e)}")
        return jsonify({
            'error': 'Calculation failed',
            'message': str(e)
        }), 500


@bp.route('/scenarios/compare', methods=['POST'])
def compare_scenarios():
    """
    Compare multiple retirement scenarios

    Request body:
        {
            "scenarios": [
                {
                    "name": "Retire at 55",
                    "currentAge": 28,
                    "retirementAge": 55,
                    "basicSalary": 75000,
                    ...
                },
                {
                    "name": "Retire at 60",
                    ...
                }
            ]
        }

    Returns:
        Comparison of all scenarios
    """
    try:
        data = request.get_json()
        scenarios = data.get('scenarios', [])

        if not scenarios:
            return jsonify({
                'error': 'Missing scenarios',
                'message': 'At least one scenario is required'
            }), 400

        results = []

        for scenario in scenarios:
            savings_result = calculate_retirement_savings(
                current_age=scenario['currentAge'],
                retirement_age=scenario['retirementAge'],
                basic_salary=scenario['basicSalary'],
                employee_epf_rate=scenario.get('employeeEpfRate', 10),
                annual_increment=scenario.get('annualIncrement', 5),
                epf_interest_rate=scenario.get('epfInterestRate', 9.5),
                current_epf_balance=scenario.get('currentEpfBalance', 0)
            )

            years_to_retirement = scenario['retirementAge'] - scenario['currentAge']
            purchasing_power = calculate_purchasing_power(
                savings_result['final_balance'],
                years_to_retirement,
                scenario.get('inflationRate', 6)
            )

            results.append({
                'name': scenario.get('name', f"Scenario {len(results) + 1}"),
                'finalBalance': savings_result['final_balance'],
                'realValue': purchasing_power['real_value'],
                'yearsToRetirement': years_to_retirement
            })

        return jsonify({
            'success': True,
            'data': {
                'scenarios': results
            }
        }), 200

    except Exception as e:
        logger.error(f"Scenario comparison error: {str(e)}")
        return jsonify({
            'error': 'Comparison failed',
            'message': str(e)
        }), 500
