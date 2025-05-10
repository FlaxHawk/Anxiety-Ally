'use client';

import React from 'react';
import Link from 'next/link';
import { motion } from 'framer-motion';
import { useAuth } from '@/lib/context/auth-context';

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen flex flex-col">
      {/* Header/Navigation */}
      <nav className="bg-white dark:bg-gray-900 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16">
            <div className="flex">
              <div className="flex-shrink-0 flex items-center">
                <h1 className="text-xl font-bold text-primary-600">Anxiety Ally</h1>
              </div>
            </div>
            <div className="flex items-center">
              {user ? (
                <Link 
                  href="/dashboard" 
                  className="btn btn-primary"
                >
                  Dashboard
                </Link>
              ) : (
                <div className="space-x-4">
                  <Link 
                    href="/auth/login" 
                    className="btn btn-outline"
                  >
                    Sign In
                  </Link>
                  <Link 
                    href="/auth/register" 
                    className="btn btn-primary"
                  >
                    Get Started
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="flex-1 flex flex-col items-center justify-center px-4 sm:px-6 lg:px-8 py-12 bg-gradient-to-b from-primary-50 to-white dark:from-gray-900 dark:to-gray-800">
        <div className="max-w-4xl mx-auto text-center">
          <motion.h1 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="text-4xl font-bold text-gray-900 dark:text-white sm:text-5xl md:text-6xl"
          >
            Your daily companion for <span className="text-primary-600">mental wellbeing</span>
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="mt-6 text-xl text-gray-600 dark:text-gray-300"
          >
            Track moods, journal your thoughts, and practice guided exercises that help manage anxiety and improve your mental health.
          </motion.p>
          
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.6 }}
            className="mt-10"
          >
            {!user && (
              <Link 
                href="/auth/register" 
                className="btn btn-primary text-lg px-8 py-3"
              >
                Start Your Journey
              </Link>
            )}
          </motion.div>
        </div>
      </section>
      
      {/* Features Section */}
      <section className="bg-white dark:bg-gray-800 py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-center text-3xl font-bold text-gray-900 dark:text-white mb-12">Features to Support Your Mental Health</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Feature 1 */}
            <div className="card hover:shadow-lg transition-shadow">
              <div className="h-12 w-12 rounded-full bg-primary-100 flex items-center justify-center text-primary-600 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M15.182 15.182a4.5 4.5 0 01-6.364 0M21 12a9 9 0 11-18 0 9 9 0 0118 0zM9.75 9.75c0 .414-.168.75-.375.75S9 10.164 9 9.75 9.168 9 9.375 9s.375.336.375.75zm-.375 0h.008v.015h-.008V9.75zm5.625 0c0 .414-.168.75-.375.75s-.375-.336-.375-.75.168-.75.375-.75.375.336.375.75zm-.375 0h.008v.015h-.008V9.75z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Mood Tracking</h3>
              <p className="text-gray-600 dark:text-gray-300">Monitor your emotional patterns and identify triggers with our intuitive mood tracking tools.</p>
            </div>
            
            {/* Feature 2 */}
            <div className="card hover:shadow-lg transition-shadow">
              <div className="h-12 w-12 rounded-full bg-secondary-100 flex items-center justify-center text-secondary-600 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Journaling</h3>
              <p className="text-gray-600 dark:text-gray-300">Express your thoughts in a private, guided journal with helpful prompts and sentiment analysis.</p>
            </div>
            
            {/* Feature 3 */}
            <div className="card hover:shadow-lg transition-shadow">
              <div className="h-12 w-12 rounded-full bg-accent-100 flex items-center justify-center text-accent-600 mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-6 h-6">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M21 8.25c0-2.485-2.099-4.5-4.688-4.5-1.935 0-3.597 1.126-4.312 2.733-.715-1.607-2.377-2.733-4.313-2.733C5.1 3.75 3 5.765 3 8.25c0 7.22 9 12 9 12s9-4.78 9-12z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold mb-2">Guided Exercises</h3>
              <p className="text-gray-600 dark:text-gray-300">Practice breathing techniques and mindfulness exercises designed to reduce anxiety in the moment.</p>
            </div>
          </div>
        </div>
      </section>
      
      {/* Call to action */}
      <section className="bg-primary-600 text-white py-16 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-6">Begin Your Mental Health Journey Today</h2>
          <p className="text-xl mb-8">Join thousands who are already improving their mental wellbeing with Anxiety Ally.</p>
          
          {!user && (
            <Link 
              href="/auth/register" 
              className="btn bg-white text-primary-600 hover:bg-gray-100 text-lg px-8 py-3"
            >
              Create Free Account
            </Link>
          )}
        </div>
      </section>
      
      {/* Footer */}
      <footer className="bg-gray-100 dark:bg-gray-900 py-8 px-4 sm:px-6 lg:px-8">
        <div className="max-w-7xl mx-auto">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="mb-4 md:mb-0">
              <h2 className="text-xl font-bold text-primary-600">Anxiety Ally</h2>
              <p className="text-gray-600 dark:text-gray-400 mt-1">Your companion for mental wellbeing</p>
            </div>
            
            <div className="flex space-x-6">
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-primary-600">About</a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-primary-600">Privacy</a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-primary-600">Terms</a>
              <a href="#" className="text-gray-600 dark:text-gray-400 hover:text-primary-600">Contact</a>
            </div>
          </div>
          
          <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
            <p className="text-gray-500 dark:text-gray-400 text-center">&copy; {new Date().getFullYear()} Anxiety Ally. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
} 