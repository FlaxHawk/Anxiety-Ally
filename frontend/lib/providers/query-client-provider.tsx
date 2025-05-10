'use client';

import React from 'react';
import { QueryClient, QueryClientProvider as ReactQueryClientProvider } from 'react-query';

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
    },
  },
});

export function QueryClientProvider({ children }: { children: React.ReactNode }) {
  return (
    <ReactQueryClientProvider client={queryClient}>
      {children}
    </ReactQueryClientProvider>
  );
} 