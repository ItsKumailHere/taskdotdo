'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { jwtDecode } from 'jwt-decode'; // Using jwt-decode library for decoding JWT tokens

interface TokenPayload {
  sub: string;
  email: string;
  role: string;
  exp: number;
}

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const router = useRouter();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Check if token exists in localStorage
        const token = localStorage.getItem('access_token');
        
        if (!token) {
          setIsAuthenticated(false);
          router.push('/login');
          return;
        }

        // Decode token to check expiration
        const decoded: TokenPayload = jwtDecode(token);
        const currentTime = Date.now() / 1000;

        if (decoded.exp < currentTime) {
          // Token is expired
          localStorage.removeItem('access_token');
          setIsAuthenticated(false);
          router.push('/login');
          return;
        }

        // Token is valid
        setIsAuthenticated(true);
      } catch (error) {
        console.error('Error checking authentication:', error);
        setIsAuthenticated(false);
        router.push('/login');
      }
    };

    checkAuth();
  }, [router]);

  // While checking authentication status, show a loading indicator
  if (isAuthenticated === null) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-gray-600">Checking authentication...</p>
        </div>
      </div>
    );
  }

  // If not authenticated, don't render children
  if (!isAuthenticated) {
    return null;
  }

  // If authenticated, render children
  return <>{children}</>;
};

export default ProtectedRoute;