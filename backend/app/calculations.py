"""
Core calculation functions for EPF/ETF retirement planning
"""
import numpy as np
from typing import Dict, List, Optional


def calculate_monthly_contributions(
    basic_salary: float,
    employee_epf_rate: int = 10
) -> Dict[str, float]:
    """
    Calculate monthly EPF/ETF contributions

    Args:
        basic_salary: Monthly basic salary in LKR
        employee_epf_rate: Employee EPF contribution rate (8 or 10)

    Returns:
        Dictionary with breakdown of contributions
    """
    employee_epf = basic_salary * (employee_epf_rate / 100)
    employer_epf = basic_salary * 0.12  # 12%
    employer_etf = basic_salary * 0.03  # 3%

    total_epf = employee_epf + employer_epf
    total_contribution = total_epf + employer_etf

    return {
        'employee_epf': round(employee_epf, 2),
        'employer_epf': round(employer_epf, 2),
        'employer_etf': round(employer_etf, 2),
        'total_epf': round(total_epf, 2),
        'total_monthly': round(total_contribution, 2),
        'yearly_contribution': round(total_epf * 12, 2)  # Only EPF accumulates (not ETF)
    }


def calculate_retirement_savings(
    current_age: int,
    retirement_age: int,
    basic_salary: float,
    employee_epf_rate: int = 10,
    annual_increment: float = 5.0,
    epf_interest_rate: float = 9.5,
    current_epf_balance: float = 0
) -> Dict:
    """
    Calculate retirement savings with compound interest

    Args:
        current_age: Current age
        retirement_age: Target retirement age
        basic_salary: Current monthly basic salary
        employee_epf_rate: Employee EPF rate (8 or 10)
        annual_increment: Expected annual salary increment percentage
        epf_interest_rate: Expected EPF interest rate
        current_epf_balance: Current EPF balance

    Returns:
        Dictionary with final balance and yearly breakdown
    """
    years_to_retirement = retirement_age - current_age
    if years_to_retirement <= 0:
        raise ValueError("Retirement age must be greater than current age")

    monthly_rate = epf_interest_rate / 100 / 12
    total_balance = current_epf_balance
    salary = basic_salary
    yearly_data = []

    for year in range(years_to_retirement):
        year_start_balance = total_balance

        # Calculate monthly contributions for this year
        employee_contribution = salary * (employee_epf_rate / 100)
        employer_contribution = salary * 0.12
        monthly_contribution = employee_contribution + employer_contribution

        # Calculate year-end balance with compound interest
        for month in range(12):
            total_balance = total_balance * (1 + monthly_rate) + monthly_contribution

        year_end_balance = total_balance
        year_interest = year_end_balance - year_start_balance - (monthly_contribution * 12)

        yearly_data.append({
            'year': year + 1,
            'age': current_age + year + 1,
            'salary': round(salary, 2),
            'monthly_contribution': round(monthly_contribution, 2),
            'yearly_contribution': round(monthly_contribution * 12, 2),
            'year_start_balance': round(year_start_balance, 2),
            'year_end_balance': round(year_end_balance, 2),
            'interest_earned': round(year_interest, 2)
        })

        # Apply salary increment for next year
        salary *= (1 + annual_increment / 100)

    return {
        'final_balance': round(total_balance, 2),
        'years_to_retirement': years_to_retirement,
        'yearly_breakdown': yearly_data,
        'total_contributions': round(sum(y['yearly_contribution'] for y in yearly_data), 2),
        'total_interest': round(total_balance - current_epf_balance - sum(y['yearly_contribution'] for y in yearly_data), 2)
    }


def calculate_purchasing_power(
    future_value: float,
    years: int,
    inflation_rate: float = 6.0
) -> Dict[str, float]:
    """
    Calculate real value adjusted for inflation

    Args:
        future_value: Nominal future value
        years: Number of years
        inflation_rate: Expected inflation rate

    Returns:
        Dictionary with real value and purchasing power loss
    """
    real_value = future_value / ((1 + inflation_rate / 100) ** years)
    purchasing_power_loss = ((future_value - real_value) / future_value) * 100

    return {
        'nominal_value': round(future_value, 2),
        'real_value': round(real_value, 2),
        'inflation_rate': inflation_rate,
        'years': years,
        'purchasing_power_loss_percentage': round(purchasing_power_loss, 2)
    }


def calculate_monthly_pension(
    epf_balance: float,
    interest_rate: float = 9.5,
    years: int = 20
) -> Dict[str, float]:
    """
    Calculate monthly pension if keeping money in EPF

    Args:
        epf_balance: Total EPF balance at retirement
        interest_rate: Expected EPF interest rate
        years: Number of years to withdraw

    Returns:
        Dictionary with monthly pension details
    """
    if epf_balance <= 0:
        return {
            'monthly_pension': 0,
            'total_withdrawals': 0,
            'total_interest': 0
        }

    monthly_rate = interest_rate / 100 / 12
    total_months = years * 12

    # PMT formula: calculate monthly withdrawal
    if monthly_rate == 0:
        monthly_pension = epf_balance / total_months
    else:
        monthly_pension = (epf_balance * monthly_rate) / (1 - (1 + monthly_rate) ** -total_months)

    total_withdrawals = monthly_pension * total_months
    total_interest = total_withdrawals - epf_balance

    return {
        'monthly_pension': round(monthly_pension, 2),
        'withdrawal_years': years,
        'total_withdrawals': round(total_withdrawals, 2),
        'initial_balance': round(epf_balance, 2),
        'total_interest_earned': round(total_interest, 2)
    }


def calculate_required_savings(
    target_amount: float,
    current_balance: float,
    monthly_contribution: float,
    interest_rate: float,
    years: int
) -> Dict[str, float]:
    """
    Calculate if target retirement amount is achievable

    Args:
        target_amount: Target retirement savings
        current_balance: Current EPF balance
        monthly_contribution: Current monthly EPF contribution
        interest_rate: Expected interest rate
        years: Years to retirement

    Returns:
        Dictionary with gap analysis and recommendations
    """
    monthly_rate = interest_rate / 100 / 12
    total_months = years * 12

    # Calculate projected balance with current contributions
    projected_balance = current_balance
    for _ in range(total_months):
        projected_balance = projected_balance * (1 + monthly_rate) + monthly_contribution

    gap = target_amount - projected_balance

    if gap > 0:
        # Calculate required additional monthly savings
        if monthly_rate == 0:
            required_additional = gap / total_months
        else:
            required_additional = (gap * monthly_rate) / ((1 + monthly_rate) ** total_months - 1)
    else:
        required_additional = 0

    return {
        'target_amount': round(target_amount, 2),
        'projected_balance': round(projected_balance, 2),
        'gap': round(gap, 2),
        'is_achievable': gap <= 0,
        'required_additional_monthly': round(required_additional, 2) if gap > 0 else 0,
        'current_monthly_contribution': round(monthly_contribution, 2)
    }


def calculate_lump_sum_tax(withdrawal_amount: float) -> Dict[str, float]:
    """
    Calculate tax on EPF lump sum withdrawal (Sri Lankan tax rules)

    As of 2024:
    - First LKR 2.5M: Tax-free
    - Above LKR 2.5M: Subject to income tax

    Args:
        withdrawal_amount: Amount to withdraw

    Returns:
        Dictionary with tax calculation
    """
    tax_free_threshold = 2500000  # LKR 2.5M

    if withdrawal_amount <= tax_free_threshold:
        taxable_amount = 0
        tax = 0
    else:
        taxable_amount = withdrawal_amount - tax_free_threshold
        # Simplified tax calculation (consult tax professional for exact rates)
        if taxable_amount <= 500000:
            tax = taxable_amount * 0.06
        elif taxable_amount <= 500000:
            tax = 500000 * 0.06 + (taxable_amount - 500000) * 0.12
        else:
            tax = 500000 * 0.06 + 500000 * 0.12 + (taxable_amount - 1000000) * 0.18

    net_amount = withdrawal_amount - tax

    return {
        'withdrawal_amount': round(withdrawal_amount, 2),
        'tax_free_amount': round(min(withdrawal_amount, tax_free_threshold), 2),
        'taxable_amount': round(taxable_amount, 2),
        'estimated_tax': round(tax, 2),
        'net_amount': round(net_amount, 2)
    }
