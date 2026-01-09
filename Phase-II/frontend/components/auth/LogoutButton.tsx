'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { apiClient } from '@/lib/api/client';

interface LogoutButtonProps {
  className?: string;
}

const LogoutButton: React.FC<LogoutButtonProps> = ({ className = '' }) => {
  const router = useRouter();

  const handleLogout = async () => {
    try {
      // Call the backend logout endpoint
      await apiClient.post('/auth/logout');
    } catch (error) {
      console.error('Logout error:', error);
      // Even if the backend call fails, we should still clear the local token
    } finally {
      // Remove the token from localStorage
      localStorage.removeItem('access_token');
      
      // Redirect to login page
      router.push('/login');
      router.refresh(); // Refresh to update auth state
    }
  };

  return (
    <button
      onClick={handleLogout}
      className={`px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors ${className}`}
    >
      Logout
    </button>
  );
};

export default LogoutButton;