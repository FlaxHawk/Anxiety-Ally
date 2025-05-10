// User related types
export interface User {
  id: string;
  email: string;
  full_name: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  loading: boolean;
  error: string | null;
}

// Journal related types
export interface JournalEntry {
  id: string;
  title: string;
  content: string;
  mood_id?: string;
  user_id: string;
  created_at: string;
  updated_at?: string;
  sentiment_score?: number;
  tags: string[];
  image_urls: string[];
}

export interface JournalAnalysis {
  entry_id: string;
  sentiment_score: number;
  sentiment_label: string;
  keywords: string[];
  suggestions?: string[];
}

// Mood related types
export interface Mood {
  id: string;
  score: number;
  notes?: string;
  user_id: string;
  timestamp: string;
  created_at: string;
}

export interface MoodAggregation {
  period: 'day' | 'week' | 'month';
  data: {
    period: string;
    average_score: number;
    count: number;
  }[];
  average_score: number;
}

// AI Chat related types
export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatResponse {
  response: string;
  suggestions: string[];
}

// Breathing exercise related types
export interface BreathingExercise {
  name: string;
  description: string;
  inhale_duration: number;
  hold_duration: number;
  exhale_duration: number;
  cycles: number;
} 