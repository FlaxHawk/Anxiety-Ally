import type { Metadata } from 'next';
import { Inter, Poppins } from 'next/font/google';
import './globals.css';
import { AuthProvider } from '@/lib/context/auth-context';
import { QueryClientProvider } from '@/lib/providers/query-client-provider';

const inter = Inter({ 
  subsets: ['latin'],
  variable: '--font-inter',
  display: 'swap',
});

const poppins = Poppins({
  weight: ['400', '500', '600', '700'],
  subsets: ['latin'],
  variable: '--font-poppins',
  display: 'swap',
});

export const metadata: Metadata = {
  title: 'Anxiety Ally | Your Mental Health Companion',
  description: 'Track moods, journal thoughts, and practice guided exercises for managing anxiety and improving mental well-being.',
  keywords: 'anxiety, mental health, mood tracking, journaling, breathing exercises, therapy',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.variable} ${poppins.variable} font-sans antialiased`}>
        <QueryClientProvider>
          <AuthProvider>
            {children}
          </AuthProvider>
        </QueryClientProvider>
      </body>
    </html>
  );
} 