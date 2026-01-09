/**
 * Unit tests for ProtectedRoute component
 */

import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, jest } from '@jest/globals';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
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

describe('ProtectedRoute', () => {
  const MockChildComponent = () => <div data-testid="child-component">Child Content</div>;

  beforeEach(() => {
    // Clear localStorage before each test
    mockLocalStorage.clear();
    
    // Reset jwtDecode mock
    (jwtDecode as jest.MockedFunction<typeof jwtDecode>).mockClear();
  });

  it('should redirect to login when no token is present', async () => {
    // Don't set any token in localStorage
    render(
      <ProtectedRoute>
        <MockChildComponent />
      </ProtectedRoute>
    );

    // Expect the child component not to be rendered
    expect(screen.queryByTestId('child-component')).not.toBeInTheDocument();
  });

  it('should redirect to login when token is expired', async () => {
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

    // Expect the child component not to be rendered
    expect(screen.queryByTestId('child-component')).not.toBeInTheDocument();
  });

  it('should render children when token is valid', async () => {
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
      expect(screen.getByTestId('child-component')).toBeInTheDocument();
    });
  });

  it('should handle token decoding errors gracefully', async () => {
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

    // Expect the child component not to be rendered due to error
    expect(screen.queryByTestId('child-component')).not.toBeInTheDocument();
  });

  it('should show loading state initially', () => {
    // Initially, the component should show a loading state
    render(
      <ProtectedRoute>
        <MockChildComponent />
      </ProtectedRoute>
    );

    // Check if loading indicator is present
    expect(screen.getByText('Checking authentication...')).toBeInTheDocument();
  });
});