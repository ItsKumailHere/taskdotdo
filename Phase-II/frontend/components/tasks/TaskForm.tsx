'use client';

import React, { useState } from 'react';
import { createTodo, updateTodo } from '@/lib/api/todo-api';
import { TodoCreate, TodoUpdate } from '@/lib/types/todo';

interface TaskFormProps {
  onTaskCreated?: () => void;
  onTaskUpdated?: () => void;
  editingTask?: { id: string; title: string; description?: string };
  onCancelEdit?: () => void;
}

const TaskForm: React.FC<TaskFormProps> = ({
  onTaskCreated,
  onTaskUpdated,
  editingTask,
  onCancelEdit
}) => {
  const [title, setTitle] = useState(editingTask?.title || '');
  const [description, setDescription] = useState(editingTask?.description || '');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const isEditing = !!editingTask;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      setError('Title is required');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      if (isEditing && editingTask) {
        // Update existing task
        const updateData: TodoUpdate = {
          title: title.trim(),
          description: description.trim() || undefined,
        };

        await updateTodo(editingTask.id, updateData);
        if (onTaskUpdated) {
          onTaskUpdated();
        }
      } else {
        // Create new task
        const newTaskData: TodoCreate = {
          title: title.trim(),
          description: description.trim() || undefined,
          completed: false,
        };

        await createTodo(newTaskData);
        setTitle('');
        setDescription('');
        if (onTaskCreated) {
          onTaskCreated();
        }
      }
    } catch (err) {
      console.error(isEditing ? 'Error updating task:' : 'Error creating task:', err);
      setError(isEditing
        ? 'Failed to update task. Please try again.'
        : 'Failed to create task. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    if (onCancelEdit) {
      onCancelEdit();
    }
    setTitle(editingTask?.title || '');
    setDescription(editingTask?.description || '');
  };

  return (
    <form onSubmit={handleSubmit} className="mb-6 p-4 bg-white rounded-lg shadow">
      <h2 className="text-xl font-semibold mb-4 text-gray-800">
        {isEditing ? 'Edit Task' : 'Add New Task'}
      </h2>

      {error && (
        <div className="mb-4 p-2 bg-red-100 text-red-700 rounded">
          {error}
        </div>
      )}

      <div className="mb-4">
        <label htmlFor="title" className="block text-sm font-medium text-gray-700 mb-1">
          Title *
        </label>
        <input
          type="text"
          id="title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter task title"
          maxLength={255}
        />
      </div>

      <div className="mb-4">
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          placeholder="Enter task description (optional)"
          rows={3}
          maxLength={1000}
        />
      </div>

      <div className="flex space-x-2">
        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded-md text-white ${
            loading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'
          }`}
        >
          {loading ? (isEditing ? 'Updating...' : 'Creating...') : isEditing ? 'Update Task' : 'Create Task'}
        </button>

        {isEditing && (
          <button
            type="button"
            onClick={handleCancel}
            className="px-4 py-2 rounded-md text-white bg-gray-500 hover:bg-gray-600"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default TaskForm;