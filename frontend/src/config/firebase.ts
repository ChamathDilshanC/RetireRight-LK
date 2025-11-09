/**
 * Firebase configuration and initialization
 */
import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: 'AIzaSyASPnWP5H_MYqS55U_iOkR4eWb0rEbpyzI',
  authDomain: 'retireright-lk-41def.firebaseapp.com',
  projectId: 'retireright-lk-41def',
  storageBucket: 'retireright-lk-41def.firebasestorage.app',
  messagingSenderId: '787400804995',
  appId: '1:787400804995:web:9629e598e7ed51a17229b6',
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication
export const auth = getAuth(app);

// Google Auth Provider
export const googleProvider = new GoogleAuthProvider();
googleProvider.setCustomParameters({
  prompt: 'select_account',
});

export default app;
