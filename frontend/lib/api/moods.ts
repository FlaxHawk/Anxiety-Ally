import axios from 'axios';
import { Mood, MoodAggregation } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/moods`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getMoods = async () => {
  const response = await api.get('/');
  return response.data;
};

export const createMood = async (mood: Partial<Mood>) => {
  const response = await api.post('/', mood);
  return response.data;
};

export const updateMood = async (moodId: string, mood: Partial<Mood>) => {
  const response = await api.put(`/${moodId}`, mood);
  return response.data;
};

export const deleteMood = async (moodId: string) => {
  const response = await api.delete(`/${moodId}`);
  return response.data;
};

export const aggregateMoods = async (period: string, startDate?: string, endDate?: string) => {
  let url = `/aggregate/${period}`;
  const params = [];
  if (startDate) params.push(`start_date=${startDate}`);
  if (endDate) params.push(`end_date=${endDate}`);
  if (params.length) url += `?${params.join('&')}`;
  const response = await api.get(url);
  return response.data;
};

export default api; 