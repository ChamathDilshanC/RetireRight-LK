/**
 * Authentication store using Zustand
 */
import {
  getCurrentUser,
  onAuthStateChange,
  signInWithGoogle,
  signOut,
} from '@/services/auth.service';
import type { User } from '@/types';
import { create } from 'zustand';

interface AuthState {
  user: User | null;
  loading: boolean;
  error: string | null;
  isInitializing: boolean;

  // Actions
  login: () => Promise<void>;
  logout: () => Promise<void>;
  initialize: () => () => void;
  setUser: (user: User | null) => void;
  setError: (error: string | null) => void;
}

export const useAuthStore = create<AuthState>(set => ({
  user: null,
  loading: true,
  error: null,
  isInitializing: false,

  login: async () => {
    set({ loading: true, error: null });
    try {
      const user = await signInWithGoogle();
      set({ user, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  logout: async () => {
    try {
      set({ loading: true });
      await signOut();
      set({ user: null, loading: false });
    } catch (error: any) {
      set({ error: error.message, loading: false });
      throw error;
    }
  },

  initialize: () => {
    // Listen to Firebase auth state changes
    const unsubscribe = onAuthStateChange(async firebaseUser => {
      if (firebaseUser) {
        try {
          const token = await firebaseUser.getIdToken();
          localStorage.setItem('firebaseToken', token);

          // Get user from backend
          const user = await getCurrentUser();
          if (user) {
            set({ user, loading: false });
          } else {
            // Backend not available, use Firebase user data
            const fallbackUser: User = {
              id: 0,
              uid: firebaseUser.uid,
              email: firebaseUser.email || '',
              name: firebaseUser.displayName || '',
              profilePicture: firebaseUser.photoURL || '',
              emailVerified: firebaseUser.emailVerified,
              createdAt: new Date().toISOString(),
            };
            set({ user: fallbackUser, loading: false });
          }
        } catch (error) {
          console.error('Error getting user:', error);
          // Fallback to Firebase user
          const fallbackUser: User = {
            id: 0,
            uid: firebaseUser.uid,
            email: firebaseUser.email || '',
            name: firebaseUser.displayName || '',
            profilePicture: firebaseUser.photoURL || '',
            emailVerified: firebaseUser.emailVerified,
            createdAt: new Date().toISOString(),
          };
          set({ user: fallbackUser, loading: false });
        }
      } else {
        set({ user: null, loading: false });
        localStorage.removeItem('firebaseToken');
      }
    });

    return unsubscribe;
  },
  setUser: user => set({ user }),

  setError: error => set({ error }),
}));
