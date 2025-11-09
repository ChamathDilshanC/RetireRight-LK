/**
 * User types and interfaces
 */

export interface User {
  id: number;
  uid: string;
  email: string;
  name: string;
  profilePicture?: string;
  emailVerified: boolean;
  createdAt: string;
  lastLogin?: string;
}

export interface SalaryProfile {
  id: number;
  currentBasicSalary: number;
  age: number;
  yearsOfService: number;
  retirementAge: number;
  epfRate: number;
  expectedSalaryIncrement: number;
  currentEpfBalance: number;
  createdAt: string;
  updatedAt: string;
}

export interface CalculationHistory {
  id: number;
  calculationType: string;
  inputs: Record<string, any>;
  results: Record<string, any>;
  createdAt: string;
}

export interface MonthlyContributions {
  employee_epf: number;
  employer_epf: number;
  employer_etf: number;
  total_epf: number;
  total_monthly: number;
  yearly_contribution: number;
}

export interface YearlyBreakdown {
  year: number;
  age: number;
  salary: number;
  monthly_contribution: number;
  yearly_contribution: number;
  year_start_balance: number;
  year_end_balance: number;
  interest_earned: number;
}

export interface PurchasingPower {
  nominal_value: number;
  real_value: number;
  inflation_rate: number;
  years: number;
  purchasing_power_loss_percentage: number;
}

export interface MonthlyPension {
  monthly_pension: number;
  withdrawal_years: number;
  total_withdrawals: number;
  initial_balance: number;
  total_interest_earned: number;
}

export interface RetirementProjection {
  finalBalance: number;
  yearlyBreakdown: YearlyBreakdown[];
  purchasingPower: PurchasingPower;
  monthlyPensionOptions: {
    twentyYears: number;
    twentyFiveYears: number;
  };
}

export interface CalculatorInputs {
  currentAge: number;
  retirementAge: number;
  basicSalary: number;
  employeeEpfRate: number;
  annualIncrement: number;
  epfInterestRate: number;
  currentEpfBalance: number;
  inflationRate: number;
}

export interface Scenario {
  name: string;
  finalBalance: number;
  realValue: number;
  yearsToRetirement: number;
}
