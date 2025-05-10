import axios from 'axios';
import { ChatMessage, ChatResponse, BreathingExercise } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/ai`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatWithBot = async (message: string, history?: ChatMessage[]) => {
  const response = await api.post<ChatResponse>('/chat', { message, history });
  return response.data;
};

export const analyzeSentiment = async (text: string) => {
  const response = await api.post('/sentiment', { text });
  return response.data;
};

export const getBreathingExercises = async () => {
  const response = await api.get<BreathingExercise[]>('/breathing-exercises');
  return response.data;
};

export default api; 