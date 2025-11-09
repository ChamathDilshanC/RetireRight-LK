"""
Database models for the application
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    """User model for storing user information"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255))
    profile_picture = db.Column(db.String(512))
    email_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

    # Relationships
    salary_profile = db.relationship('SalaryProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    calculations = db.relationship('CalculationHistory', backref='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'


class SalaryProfile(db.Model):
    """Salary profile model for storing user's financial information"""
    __tablename__ = 'salary_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    current_basic_salary = db.Column(db.Float, nullable=False)
    age = db.Column(db.Integer)
    years_of_service = db.Column(db.Integer)
    retirement_age = db.Column(db.Integer, default=60)
    epf_rate = db.Column(db.Integer, default=10)  # 8 or 10
    expected_salary_increment = db.Column(db.Float, default=5.0)
    current_epf_balance = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'currentBasicSalary': self.current_basic_salary,
            'age': self.age,
            'yearsOfService': self.years_of_service,
            'retirementAge': self.retirement_age,
            'epfRate': self.epf_rate,
            'expectedSalaryIncrement': self.expected_salary_increment,
            'currentEpfBalance': self.current_epf_balance,
            'createdAt': self.created_at.isoformat(),
            'updatedAt': self.updated_at.isoformat()
        }

    def __repr__(self):
        return f'<SalaryProfile user_id={self.user_id}>'


class CalculationHistory(db.Model):
    """Calculation history model for storing user's past calculations"""
    __tablename__ = 'calculation_history'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    calculation_type = db.Column(db.String(50), nullable=False)  # e.g., 'retirement_projection'
    inputs = db.Column(db.Text, nullable=False)  # JSON string of inputs
    results = db.Column(db.Text, nullable=False)  # JSON string of results
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'calculationType': self.calculation_type,
            'inputs': json.loads(self.inputs) if isinstance(self.inputs, str) else self.inputs,
            'results': json.loads(self.results) if isinstance(self.results, str) else self.results,
            'createdAt': self.created_at.isoformat()
        }

    def __repr__(self):
        return f'<CalculationHistory id={self.id} type={self.calculation_type}>'


class EPFRateHistory(db.Model):
    """Historical EPF interest rates from Central Bank"""
    __tablename__ = 'epf_rate_history'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True, nullable=False)
    interest_rate = db.Column(db.Float, nullable=False)
    inflation_rate = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'year': self.year,
            'interestRate': self.interest_rate,
            'inflationRate': self.inflation_rate
        }

    def __repr__(self):
        return f'<EPFRateHistory year={self.year} rate={self.interest_rate}%>'
