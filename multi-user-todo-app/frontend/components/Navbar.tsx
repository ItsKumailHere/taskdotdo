'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { isAuthenticated, logout, getCurrentUser } from '../lib/auth-utils';
import { User } from '../lib/types';

const Navbar: React.FC = () => {
  const [authStatus, setAuthStatus] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const [menuOpen, setMenuOpen] = useState(false);

  useEffect(() => {
    const checkAuthStatus = async () => {
      const status = isAuthenticated();
      setAuthStatus(status);

      if (status) {
        const currentUser = await getCurrentUser();
        setUser(currentUser);
      }
    };

    checkAuthStatus();
  }, []);

  const handleLogout = async () => {
    await logout();
    setAuthStatus(false);
    setUser(null);
    window.location.href = '/';
  };

  return (
    <nav className="bg-blue-600 text-white shadow-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <span className="text-xl font-bold">TaskDotDo</span>
            </Link>
            <div className="hidden md:ml-6 md:flex md:space-x-8">
              <Link
                href="/"
                className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-blue-100 hover:border-blue-300 hover:text-white"
              >
                Home
              </Link>
              {authStatus && (
                <>
                  <Link
                    href="/dashboard"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-blue-100 hover:border-blue-300 hover:text-white"
                  >
                    Dashboard
                  </Link>
                  <Link
                    href="/todos"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent text-sm font-medium text-blue-100 hover:border-blue-300 hover:text-white"
                  >
                    Todos
                  </Link>
                </>
              )}
            </div>
          </div>

          <div className="flex items-center">
            <div className="hidden md:ml-4 md:flex md:items-center space-x-4">
              {!authStatus ? (
                <>
                  <Link
                    href="/login"
                    className="text-sm font-medium text-blue-100 hover:text-white"
                  >
                    Login
                  </Link>
                  <Link
                    href="/register"
                    className="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-blue-600 bg-white hover:bg-blue-50"
                  >
                    Register
                  </Link>
                </>
              ) : (
                <div className="relative">
                  <button
                    onClick={() => setMenuOpen(!menuOpen)}
                    className="flex items-center text-sm rounded-full focus:outline-none"
                  >
                    <span className="sr-only">Open user menu</span>
                    <div className="h-8 w-8 rounded-full bg-blue-500 flex items-center justify-center">
                      {user?.username?.charAt(0).toUpperCase() || 'U'}
                    </div>
                  </button>

                  {menuOpen && (
                    <div className="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-50">
                      <div className="px-4 py-2 border-b">
                        <p className="text-sm font-medium text-gray-900">{user?.username}</p>
                        <p className="text-xs text-gray-500 truncate">{user?.email}</p>
                      </div>
                      <button
                        onClick={handleLogout}
                        className="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Sign out
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>

            {/* Mobile menu button */}
            <div className="-mr-2 flex items-center md:hidden">
              <button
                onClick={() => setMenuOpen(!menuOpen)}
                className="inline-flex items-center justify-center p-2 rounded-md text-blue-200 hover:text-white hover:bg-blue-700 focus:outline-none"
              >
                <span className="sr-only">Open main menu</span>
                {/* Mobile menu icon */}
                <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden">
          <div className="pt-2 pb-3 space-y-1">
            <Link
              href="/"
              className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-blue-100 hover:bg-blue-700"
            >
              Home
            </Link>
            {authStatus && (
              <>
                <Link
                  href="/dashboard"
                  className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-blue-100 hover:bg-blue-700"
                >
                  Dashboard
                </Link>
                <Link
                  href="/todos"
                  className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-blue-100 hover:bg-blue-700"
                >
                  Todos
                </Link>
              </>
            )}
            {!authStatus ? (
              <>
                <Link
                  href="/login"
                  className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-blue-100 hover:bg-blue-700"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className="block pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-blue-100 hover:bg-blue-700"
                >
                  Register
                </Link>
              </>
            ) : (
              <button
                onClick={handleLogout}
                className="block w-full text-left pl-3 pr-4 py-2 border-l-4 border-transparent text-base font-medium text-blue-100 hover:bg-blue-700"
              >
                Sign out
              </button>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;