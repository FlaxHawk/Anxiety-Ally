import axios from 'axios';
import { JournalEntry, JournalAnalysis } from '@/types';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: `${API_URL}/journals`,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const getJournals = async () => {
  const response = await api.get('/');
  return response.data;
};

export const createJournal = async (entry: Partial<JournalEntry>) => {
  const response = await api.post('/', entry);
  return response.data;
};

export const updateJournal = async (entryId: string, entry: Partial<JournalEntry>) => {
  const response = await api.put(`/${entryId}`, entry);
  return response.data;
};

export const deleteJournal = async (entryId: string) => {
  const response = await api.delete(`/${entryId}`);
  return response.data;
};

export const analyzeJournal = async (entryId: string) => {
  const response = await api.get(`/${entryId}/analysis`);
  return response.data as JournalAnalysis;
};

export default api; 