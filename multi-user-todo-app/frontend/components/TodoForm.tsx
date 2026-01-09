'use client';

import React, { useState } from 'react';
import { TodoCreate } from '../lib/types';
import { apiClient } from '../lib/api';

interface TodoFormProps {
  onSubmit?: (todo: TodoCreate) => void;
}

const TodoForm: React.FC<TodoFormProps> = ({ onSubmit }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    const todoData: TodoCreate = {
      title: title.trim(),
      description: description.trim() || undefined,
      due_date: dueDate || undefined,
      status: 'pending',
    };

    try {
      setLoading(true);
      setError(null);
      const newTodo = await apiClient.createTodo(todoData);
      setTitle('');
      setDescription('');
      setDueDate('');
      onSubmit?.(todoData);
    } catch (err) {
      setError('Failed to create todo');
      console.error('Error creating todo:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 bg-white dark:bg-gray-800 rounded-lg shadow">
      <div className="mb-4">
        <label htmlFor="title" className="block text-gray-700 dark:text-gray-300 mb-2">
          Task Title
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="What needs to be done?"
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        />
      </div>

      <div className="mb-4">
        <label htmlFor="description" className="block text-gray-700 dark:text-gray-300 mb-2">
          Description (optional)
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Add details..."
          rows={3}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        />
      </div>

      <div className="mb-4">
        <label htmlFor="dueDate" className="block text-gray-700 dark:text-gray-300 mb-2">
          Due Date (optional)
        </label>
        <input
          type="date"
          id="dueDate"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:text-white"
        />
      </div>

      {error && (
        <div className="mb-4 p-3 bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300 rounded">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 disabled:opacity-50"
      >
        {loading ? 'Creating...' : 'Add Task'}
      </button>
    </form>
  );
};

export default TodoForm;