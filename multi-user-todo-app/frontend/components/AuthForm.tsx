'use client';

import React, { useState } from 'react';
import { UserRegister, UserLogin } from '../lib/types';
import { signIn, signUp } from '../lib/auth-client';
import { useRouter } from 'next/navigation';

interface AuthFormProps {
  mode: 'login' | 'register';
  onAuthSuccess: () => void;
}

const AuthForm: React.FC<AuthFormProps> = ({ mode, onAuthSuccess }) => {
  const [formData, setFormData] = useState<UserRegister | UserLogin>({
    email: '',
    password: '',
    ...(mode === 'register' && { username: '', password_confirm: '' }),
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
      if (mode === 'register') {
        // For register, we'll use the Better Auth sign up
        const result = await signUp.email({
          email: (formData as UserRegister).email,
          password: (formData as UserRegister).password,
          name: (formData as UserRegister).username || '',
        });

        if (result?.error) {
          throw new Error(result.error.message);
        }
      } else {
        // For login, we'll use the Better Auth sign in
        const result = await signIn.email({
          email: (formData as UserLogin).email,
          password: (formData as UserLogin).password,
          // Remember me option can be added here if needed
        });

        if (result?.error) {
          throw new Error(result.error.message);
        }
      }
      
      onAuthSuccess();
    } catch (err: any) {
      setError(err.message || 'Authentication failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-md">
      <h2 className="text-2xl font-bold mb-6 text-center">
        {mode === 'login' ? 'Login' : 'Create Account'}
      </h2>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="email" className="block text-gray-700 mb-2">Email</label>
          <input
            type="email"
            id="email"
            name="email"
            value={(formData as any).email}
            onChange={handleChange}
            required
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {mode === 'register' && (
          <div className="mb-4">
            <label htmlFor="username" className="block text-gray-700 mb-2">Username</label>
            <input
              type="text"
              id="username"
              name="username"
              value={(formData as any).username || ''}
              onChange={handleChange}
              required
              minLength={3}
              maxLength={30}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        )}

        <div className="mb-4">
          <label htmlFor="password" className="block text-gray-700 mb-2">Password</label>
          <input
            type="password"
            id="password"
            name="password"
            value={(formData as any).password}
            onChange={handleChange}
            required
            minLength={8}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>

        {mode === 'register' && (
          <div className="mb-4">
            <label htmlFor="password_confirm" className="block text-gray-700 mb-2">Confirm Password</label>
            <input
              type="password"
              id="password_confirm"
              name="password_confirm"
              value={(formData as any).password_confirm || ''}
              onChange={handleChange}
              required
              minLength={8}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {loading ? 'Processing...' : mode === 'login' ? 'Login' : 'Register'}
        </button>
      </form>

      <div className="mt-4 text-center">
        <p className="text-gray-600">
          {mode === 'login'
            ? "Don't have an account? "
            : "Already have an account? "}
          <a
            href={mode === 'login' ? '/register' : '/login'}
            className="text-blue-600 hover:underline"
          >
            {mode === 'login' ? 'Register' : 'Login'}
          </a>
        </p>
      </div>
    </div>
  );
};

export default AuthForm;