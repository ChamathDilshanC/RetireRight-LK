/**
 * User profile and calculation history service
 */
import api from '@/config/api';
import type { CalculationHistory, SalaryProfile } from '@/types';

/**
 * Get user profile
 */
export const getUserProfile = async () => {
  try {
    const response = await api.get('/api/user/profile');
    return response.data.data;
  } catch (error: any) {
    console.error('Get user profile error:', error);
    throw new Error(error.response?.data?.message || 'Failed to get profile');
  }
};

/**
 * Update salary profile
 */
export const updateSalaryProfile = async (
  profile: Partial<SalaryProfile>
): Promise<SalaryProfile> => {
  try {
    const response = await api.put('/api/user/profile', profile);
    return response.data.data;
  } catch (error: any) {
    console.error('Update salary profile error:', error);
    throw new Error(
      error.response?.data?.message || 'Failed to update profile'
    );
  }
};

/**
 * Get calculation history
 */
export const getCalculationHistory = async (): Promise<
  CalculationHistory[]
> => {
  try {
    const response = await api.get('/api/user/calculations');
    return response.data.data;
  } catch (error: any) {
    console.error('Get calculation history error:', error);
    throw new Error(
      error.response?.data?.message || 'Failed to get calculation history'
    );
  }
};

/**
 * Save calculation
 */
export const saveCalculation = async (
  calculationType: string,
  inputs: Record<string, any>,
  results: Record<string, any>
): Promise<CalculationHistory> => {
  try {
    const response = await api.post('/api/user/calculations', {
      calculationType,
      inputs,
      results,
    });
    return response.data.data;
  } catch (error: any) {
    console.error('Save calculation error:', error);
    throw new Error(
      error.response?.data?.message || 'Failed to save calculation'
    );
  }
};

/**
 * Delete calculation
 */
export const deleteCalculation = async (id: number): Promise<void> => {
  try {
    await api.delete(`/api/user/calculations/${id}`);
  } catch (error: any) {
    console.error('Delete calculation error:', error);
    throw new Error(
      error.response?.data?.message || 'Failed to delete calculation'
    );
  }
};
