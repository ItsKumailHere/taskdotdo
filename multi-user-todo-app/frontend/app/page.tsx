import React from 'react';
import Link from 'next/link';
import Navbar from '../components/Navbar';

const HomePage: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="text-center">
          <h1 className="text-4xl font-extrabold tracking-tight text-gray-900 dark:text-white sm:text-5xl md:text-6xl">
            <span className="block">TaskDotDo</span>
            <span className="block text-blue-600 mt-2">Your Personal Todo Manager</span>
          </h1>
          <p className="mt-4 max-w-lg mx-auto text-xl text-gray-500 dark:text-gray-300">
            Organize your tasks, boost your productivity. A simple and elegant todo application for your daily needs.
          </p>
          <div className="mt-10">
            <Link 
              href="/register" 
              className="inline-block w-full md:w-auto px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Get Started
            </Link>
            <div className="mt-4 text-sm text-gray-500 dark:text-gray-400">
              Already have an account?{' '}
              <Link 
                href="/login" 
                className="font-medium text-blue-600 hover:text-blue-500 dark:text-blue-400 dark:hover:text-blue-300"
              >
                Sign in
              </Link>
            </div>
          </div>
        </div>

        <div className="mt-16 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-3">
          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">Organize Tasks</h3>
            <p className="mt-2 text-base text-gray-500 dark:text-gray-300">
              Create, categorize, and manage your todos with ease. Set due dates and priorities to stay on track.
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">Secure & Private</h3>
            <p className="mt-2 text-base text-gray-500 dark:text-gray-300">
              Your data is protected with industry-standard security practices. Only you have access to your tasks.
            </p>
          </div>

          <div className="bg-white dark:bg-gray-800 p-6 rounded-lg shadow">
            <div className="flex items-center justify-center h-12 w-12 rounded-md bg-blue-500 text-white">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
              </svg>
            </div>
            <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">Cross-Device Sync</h3>
            <p className="mt-2 text-base text-gray-500 dark:text-gray-300">
              Access your todos from any device. Your tasks are always up-to-date across all your devices.
            </p>
          </div>
        </div>
      </main>
    </div>
  );
};

export default HomePage;