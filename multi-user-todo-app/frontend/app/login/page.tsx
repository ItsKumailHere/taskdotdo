'use client';

import React from 'react';
import { useState, useEffect } from 'react';
import { useSession } from '@/lib/auth-client';
import AuthForm from '@/components/AuthForm';
import Navbar from '@/components/Navbar';
import { useRouter } from 'next/navigation';

const LoginPage: React.FC = () => {
  const { data: session, isPending } = useSession();
  const router = useRouter();

  useEffect(() => {
    if (!isPending && session) {
      router.push('/dashboard');
    }
  }, [session, isPending, router]);

  const handleAuthSuccess = () => {
    router.push('/dashboard');
  };

  if (!isPending && session) {
    return null; // Redirect will happen in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <main className="max-w-md mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <AuthForm mode="login" onAuthSuccess={handleAuthSuccess} />
      </main>
    </div>
  );
};

export default LoginPage;