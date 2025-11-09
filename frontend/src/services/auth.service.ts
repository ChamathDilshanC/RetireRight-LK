/**
 * Authentication service - Firebase integration
 */
import api from '@/config/api';
import { auth, googleProvider } from '@/config/firebase';
import type { User } from '@/types';
import {
  signOut as firebaseSignOut,
  User as FirebaseUser,
  onAuthStateChanged,
  signInWithPopup,
  UserCredential,
} from 'firebase/auth';

/**
 * Sign in with Google
 */
export const signInWithGoogle = async (): Promise<User> => {
  try {
    const result: UserCredential = await signInWithPopup(auth, googleProvider);
    const user = result.user;

    // Get Firebase ID token
    const idToken = await user.getIdToken();

    // Store token in localStorage
    localStorage.setItem('firebaseToken', idToken);

    try {
      // Verify token with backend and create/update user
      const response = await api.post('/api/auth/verify', { idToken });
      return response.data.user;
    } catch (backendError) {
      console.warn(
        'Backend verification failed, using Firebase user data:',
        backendError
      );
      // Return user data from Firebase if backend fails
      return {
        id: 0,
        uid: user.uid,
        email: user.email || '',
        name: user.displayName || '',
        profilePicture: user.photoURL || '',
        emailVerified: user.emailVerified,
        createdAt: new Date().toISOString(),
      };
    }
  } catch (error: any) {
    console.error('Google sign-in error:', error);
    throw new Error(error.message || 'Failed to sign in with Google');
  }
};

/**
 * Sign out
 */
export const signOut = async (): Promise<void> => {
  try {
    // Notify backend
    await api.post('/api/auth/logout');
  } catch (error) {
    console.error('Backend logout error:', error);
  } finally {
    // Sign out from Firebase
    await firebaseSignOut(auth);

    // Clear token
    localStorage.removeItem('firebaseToken');
  }
};

/**
 * Get current user from backend
 */
export const getCurrentUser = async (): Promise<User | null> => {
  try {
    const response = await api.get('/api/auth/me');
    return response.data.user;
  } catch (error) {
    console.error('Get current user error:', error);
    return null;
  }
};

/**
 * Refresh Firebase token
 */
export const refreshToken = async (): Promise<string | null> => {
  try {
    const user = auth.currentUser;
    if (user) {
      const token = await user.getIdToken(true);
      localStorage.setItem('firebaseToken', token);
      return token;
    }
    return null;
  } catch (error) {
    console.error('Token refresh error:', error);
    return null;
  }
};

/**
 * Delete account
 */
export const deleteAccount = async (): Promise<void> => {
  try {
    // Delete from backend
    await api.delete('/api/auth/delete');

    // Delete Firebase user
    const user = auth.currentUser;
    if (user) {
      await user.delete();
    }

    // Clear token
    localStorage.removeItem('firebaseToken');
  } catch (error: any) {
    console.error('Delete account error:', error);
    throw new Error(error.message || 'Failed to delete account');
  }
};

/**
 * Listen to auth state changes
 */
export const onAuthStateChange = (
  callback: (user: FirebaseUser | null) => void
) => {
  return onAuthStateChanged(auth, callback);
};
