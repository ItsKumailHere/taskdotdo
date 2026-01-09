'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

interface FormData {
  name: string;
  email: string;
  password: string;
}

const RegisterForm = () => {
  const [formData, setFormData] = useState<FormData>({
    name: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  
  const router = useRouter();

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    try {
      // Use the API client to connect to the backend API
      const { apiClient } = await import('@/lib/api/client');

      const data = await apiClient.post('/auth/register', formData);

      // Redirect to login or dashboard after successful registration
      router.push('/login');
      router.refresh(); // Refresh to update auth state
    } catch (err: any) {
      // Handle different error types
      if (err instanceof Error) {
        setError(err.message || 'An error occurred during registration');
      } else if (typeof err === 'string') {
        setError(err);
      } else {
        setError('An error occurred during registration');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md w-full mx-auto mt-10 p-8 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-center">Create Account</h2>
      
      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-md">
          {error}
        </div>
      )}
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="name" className="block text-gray-700 mb-2">
            Full Name
          </label>
          <input
            type="text"
            id="name"
            name="name"
            value={formData.name}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="John Doe"
          />
        </div>
        
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 mb-2">
            Email
          </label>
          <input
            type="email"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="john@example.com"
          />
        </div>
        
        <div className="mb-6">
          <label htmlFor="password" className="block text-black-700 mb-2">
            Password
          </label>
          <input
            type="text"
            id="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            required
            minLength={8}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 font-black"
            placeholder=""
          />
          <p className="mt-1 text-sm text-gray-500">
            Password must be at least 8 characters long and include uppercase, lowercase, number, and special character.
          </p>
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3 px-4 rounded-md text-white font-medium ${
            loading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
          } transition duration-200`}
        >
          {loading ? 'Creating Account...' : 'Register'}
        </button>
      </form>
      
      <div className="mt-6 text-center">
        <p className="text-gray-600">
          Already have an account?{' '}
          <Link href="/login" className="text-blue-600 hover:underline">
            Sign in
          </Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterForm;