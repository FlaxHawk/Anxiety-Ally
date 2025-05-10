import axios from 'axios';
import { User } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Initialize Axios
const api = axios.create({
  baseURL: `${API_URL}`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Set auth token for any future requests
export const setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

// Login user
export const loginUser = async (email: string, password: string) => {
  const formData = new URLSearchParams();
  formData.append('username', email); // OAuth2 uses username field
  formData.append('password', password);

  const response = await api.post('/auth/token', formData.toString(), {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });

  return response.data;
};

// Register user
export const registerUser = async (email: string, password: string, fullName: string) => {
  const response = await api.post('/auth/register', {
    email,
    password,
    full_name: fullName,
  });

  return response.data;
};

// Get user profile
export const getUserProfile = async (): Promise<User> => {
  const response = await api.get('/auth/me');
  return response.data;
};

export default api; 