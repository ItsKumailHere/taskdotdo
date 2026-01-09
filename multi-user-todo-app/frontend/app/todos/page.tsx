'use client';

import React, { useState, useEffect } from 'react';
import { getCurrentUser } from '@/lib/auth-utils';
import { User } from '@/lib/types';
import Navbar from '@/components/Navbar';
import TodoForm from '@/components/TodoForm';
import TodoList from '@/components/TodoList';
import { useRouter } from 'next/navigation';

const TodosPage: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const userData = await getCurrentUser();
        if (!userData) {
          router.push('/login');
          return;
        }
        setUser(userData);
      } catch (error) {
        console.error('Error fetching user:', error);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [router]);

  const handleTodoCreated = () => {
    // This function can be used to refresh the todo list if needed
    // For now, we'll just let the TodoList component handle its own refresh
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        <Navbar />
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="text-center">
            <p className="text-gray-500 dark:text-gray-400">Loading...</p>
          </div>
        </main>
      </div>
    );
  }

  if (!user) {
    return null; // Redirect will happen in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <Navbar />
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
            My Todos
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-400">
            Manage your tasks efficiently. Add new todos or update existing ones.
          </p>
        </div>

        <TodoForm onTodoCreated={handleTodoCreated} />

        <div className="mt-8">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200">All Todos</h2>
          </div>
          <TodoList filter="all" />
        </div>
      </main>
    </div>
  );
};

export default TodosPage;