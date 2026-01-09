/**
 * Integration tests for route protection
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { describe, expect, it, jest, beforeEach } from '@jest/globals';
import { jwtDecode } from 'jwt-decode';

// Mock localStorage
const mockLocalStorage = (() => {
  let store: { [key: string]: string } = {};
  
  return {
    getItem: (key: string) => store[key] || null,
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    }
  };
})();

Object.defineProperty(window, 'localStorage', {
  value: mockLocalStorage
});

// Mock jwtDecode
jest.mock('jwt-decode', () => ({
  jwtDecode: jest.fn()
}));

// Mock next/navigation useRouter hook
const mockPush = jest.fn();
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: mockPush,
  }),
  redirect: jest.fn(),
}));

// Import the components after mocking
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import DashboardPage from '@/app/dashboard/page';

describe('Route Protection Integration', () => {
  const MockChildComponent = () => <div data-testid="child-component">Protected Content</div>;

  beforeEach(() => {
    // Clear mocks and localStorage before each test
    mockPush.mockClear();
    mockLocalStorage.clear();
    (jwtDecode as jest.MockedFunction<typeof jwtDecode>).mockClear();
  });

  it('should prevent access to protected routes when not authenticated', async () => {
    // Don't set any token in localStorage
    render(
      <ProtectedRoute>
        <MockChildComponent />
      </ProtectedRoute>
    );

    // Wait for the authentication check to complete
    await waitFor(() => {
      // Expect the router to have been called to redirect to login
      expect(mockPush).toHaveBeenCalledWith('/login');
    });

    // The protected content should not be rendered
    expect(screen.queryByTestId('child-component')).not.toBeInTheDocument();
  });

  it('should allow access to protected routes when authenticated', async () => {
    const validToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE3NjcyMzkwMjJ9.zB9FvB8Q5j0Q7X6F5v8Q5j0Q7X6F5v8Q5j0Q7X6F5v8'; // Valid token
    
    mockLocalStorage.setItem('access_token', validToken);
    
    // Mock jwtDecode to return a valid token
    (jwtDecode as jest.MockedFunction<typeof jwtDecode>).mockReturnValue({
      sub: '1234567890',
      email: 'test@example.com',
      role: 'user',
      exp: Math.floor(Date.now() / 1000) + 1000 // Expires in 1000 seconds
    });

    render(
      <ProtectedRoute>
        <MockChildComponent />
      </ProtectedRoute>
    );

    // Wait for the authentication check to complete
    await waitFor(() => {
      // The router should not have been called to redirect
      expect(mockPush).not.toHaveBeenCalled();
    });

    // The protected content should be rendered
    expect(screen.getByTestId('child-component')).toBeInTheDocument();
  });

  it('should redirect to login when accessing dashboard without authentication', async () => {
    render(<DashboardPage />);

    // Wait for the authentication check to complete
    await waitFor(() => {
      // Expect the router to have been called to redirect to login
      expect(mockPush).toHaveBeenCalledWith('/login');
    });
  });

  it('should render dashboard when accessing with valid authentication', async () => {
    const validToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE3NjcyMzkwMjJ9.zB9FvB8Q5j0Q7X6F5v8Q5j0Q7X6F5v8Q5j0Q7X6F5v8'; // Valid token
    
    mockLocalStorage.setItem('access_token', validToken);
    
    // Mock jwtDecode to return a valid token
    (jwtDecode as jest.MockedFunction<typeof jwtDecode>).mockReturnValue({
      sub: '1234567890',
      email: 'test@example.com',
      role: 'user',
      exp: Math.floor(Date.now() / 1000) + 1000 // Expires in 1000 seconds
    });

    render(<DashboardPage />);

    // Wait for the authentication check to complete
    await waitFor(() => {
      // The router should not have been called to redirect
      expect(mockPush).not.toHaveBeenCalled();
    });

    // The dashboard content should be rendered
    expect(screen.getByText('Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Welcome to your dashboard!')).toBeInTheDocument();
  });

  it('should handle token expiration correctly', async () => {
    const expiredToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJleHAiOjE1MTYyMzkwMjJ9.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'; // Expired token
    
    mockLocalStorage.setItem('access_token', expiredToken);
    
    // Mock jwtDecode to return an expired token
    (jwtDecode as jest.MockedFunction<typeof jwtDecode>).mockReturnValue({
      sub: '1234567890',
      email: 'test@example.com',
      role: 'user',
      exp: Math.floor(Date.now() / 1000) - 1000 // Expired 1000 seconds ago
    });

    render(
      <ProtectedRoute>
        <MockChildComponent />
      </ProtectedRoute>
    );

    // Wait for the authentication check to complete
    await waitFor(() => {
      // Expect the router to have been called to redirect to login
      expect(mockPush).toHaveBeenCalledWith('/login');
    });

    // The protected content should not be rendered
    expect(screen.queryByTestId('child-component')).not.toBeInTheDocument();
  });

  it('should handle invalid token format gracefully', async () => {
    const invalidToken = 'invalid.token.format';
    
    mockLocalStorage.setItem('access_token', invalidToken);
    
    // Mock jwtDecode to throw an error
    (jwtDecode as jest.MockedFunction<typeof jwtDecode>).mockImplementation(() => {
      throw new Error('Invalid token');
    });

    render(
      <ProtectedRoute>
        <MockChildComponent />
      </ProtectedRoute>
    );

    // Wait for the authentication check to complete
    await waitFor(() => {
      // Expect the router to have been called to redirect to login
      expect(mockPush).toHaveBeenCalledWith('/login');
    });

    // The protected content should not be rendered
    expect(screen.queryByTestId('child-component')).not.toBeInTheDocument();
  });
});