'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import axios from 'axios';
import { useRouter } from 'next/navigation';
import { AuthState, User } from '@/types';
import { loginUser, registerUser, getUserProfile } from '@/lib/api/auth';

// Token utilities
const getStoredToken = (): string | null => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('token');
  }
  return null;
};

const setStoredToken = (token: string): void => {
  if (typeof window !== 'undefined') {
    localStorage.setItem('token', token);
  }
};

const removeStoredToken = (): void => {
  if (typeof window !== 'undefined') {
    localStorage.removeItem('token');
  }
};

// Create context
interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, fullName: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// Provider component
export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    token: null,
    loading: true,
    error: null,
  });
  
  const router = useRouter();

  // Check for token and load user on mount
  useEffect(() => {
    const initializeAuth = async () => {
      const token = getStoredToken();
      
      if (token) {
        try {
          // Set token in global axios headers
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
          
          // Fetch user profile
          const userData = await getUserProfile();
          
          setAuthState({
            user: userData,
            token,
            loading: false,
            error: null,
          });
        } catch (error) {
          console.error('Error loading user:', error);
          removeStoredToken();
          setAuthState({
            user: null,
            token: null,
            loading: false,
            error: 'Session expired. Please login again.',
          });
        }
      } else {
        setAuthState({
          user: null,
          token: null,
          loading: false,
          error: null,
        });
      }
    };

    initializeAuth();
  }, []);

  // Login function
  const login = async (email: string, password: string) => {
    setAuthState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      const { access_token } = await loginUser(email, password);
      
      // Set token
      setStoredToken(access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      // Get user data
      const userData = await getUserProfile();
      
      setAuthState({
        user: userData,
        token: access_token,
        loading: false,
        error: null,
      });
      
      // Redirect to dashboard
      router.push('/dashboard');
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Login failed. Please try again.';
      setAuthState(prev => ({
        ...prev,
        user: null,
        token: null,
        loading: false,
        error: errorMessage,
      }));
    }
  };

  // Register function
  const register = async (email: string, password: string, fullName: string) => {
    setAuthState(prev => ({ ...prev, loading: true, error: null }));
    
    try {
      await registerUser(email, password, fullName);
      
      // Automatically login after successful registration
      await login(email, password);
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Registration failed. Please try again.';
      setAuthState(prev => ({
        ...prev,
        user: null,
        token: null,
        loading: false,
        error: errorMessage,
      }));
    }
  };

  // Logout function
  const logout = () => {
    removeStoredToken();
    delete axios.defaults.headers.common['Authorization'];
    
    setAuthState({
      user: null,
      token: null,
      loading: false,
      error: null,
    });
    
    router.push('/');
  };

  // Context values
  const contextValue: AuthContextType = {
    ...authState,
    login,
    register,
    logout,
  };

  return (
    <AuthContext.Provider value={contextValue}>
      {children}
    </AuthContext.Provider>
  );
};

// Hook for using auth context
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  
  return context;
}; 