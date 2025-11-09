/**
 * Calculator API service
 */
import api from '@/config/api';
import type {
  CalculatorInputs,
  MonthlyContributions,
  RetirementProjection,
  Scenario,
} from '@/types';

/**
 * Calculate monthly EPF/ETF contributions
 */
export const calculateContributions = async (
  basicSalary: number,
  employeeEpfRate: number = 10
): Promise<MonthlyContributions> => {
  try {
    const response = await api.post('/api/calculator/contributions', {
      basicSalary,
      employeeEpfRate,
    });
    return response.data.data;
  } catch (error: any) {
    console.error('Calculate contributions error:', error);
    throw new Error(
      error.response?.data?.message || 'Failed to calculate contributions'
    );
  }
};

/**
 * Calculate retirement projection
 */
export const calculateRetirementProjection = async (
  inputs: CalculatorInputs
): Promise<RetirementProjection> => {
  try {
    const response = await api.post(
      '/api/calculator/retirement-projection',
      inputs
    );
    return response.data.data;
  } catch (error: any) {
    console.error('Calculate retirement projection error:', error);
    throw new Error(
      error.response?.data?.message ||
        'Failed to calculate retirement projection'
    );
  }
};

/**
 * Compare multiple scenarios
 */
export const compareScenarios = async (
  scenarios: Array<{ name: string } & CalculatorInputs>
): Promise<Scenario[]> => {
  try {
    const response = await api.post('/api/calculator/scenarios/compare', {
      scenarios,
    });
    return response.data.data.scenarios;
  } catch (error: any) {
    console.error('Compare scenarios error:', error);
    throw new Error(
      error.response?.data?.message || 'Failed to compare scenarios'
    );
  }
};
