'use client';

import React, { useState } from 'react';
import { Todo, TodoUpdate } from '../lib/types';
import { apiClient } from '../lib/api';

interface TodoItemProps {
  todo: Todo;
  onTodoUpdate: (updatedTodo: Todo) => void;
  onTodoDelete: (id: string) => void;
}

const TodoItem: React.FC<TodoItemProps> = ({ todo, onTodoUpdate, onTodoDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [status, setStatus] = useState(todo.status);
  const [loading, setLoading] = useState(false);

  const handleUpdate = async () => {
    setLoading(true);
    try {
      const updatedTodo: TodoUpdate = {
        title: editTitle,
        description: editDescription || undefined,
        status: status
      };

      const result = await apiClient.updateTodo(todo.id, updatedTodo);
      onTodoUpdate(result);
      setIsEditing(false);
    } catch (error) {
      console.error('Error updating todo:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      try {
        await apiClient.deleteTodo(todo.id);
        onTodoDelete(todo.id);
      } catch (error) {
        console.error('Error deleting todo:', error);
      }
    }
  };

  const handleToggleComplete = async () => {
    const newCompletedStatus = !completed;
    setCompleted(newCompletedStatus);
    
    try {
      const updatedTodo: TodoUpdate = {
        completed: newCompletedStatus
      };
      
      const result = await apiClient.updateTodo(todo.id, updatedTodo);
      onTodoUpdate(result);
    } catch (error) {
      console.error('Error updating todo completion:', error);
      // Revert the UI if the API call fails
      setCompleted(!newCompletedStatus);
    }
  };

  return (
    <div className={`p-4 mb-2 rounded-lg shadow flex items-start ${completed ? 'bg-green-50 dark:bg-green-900/30' : 'bg-white dark:bg-gray-800'}`}>
      <input
        type="checkbox"
        checked={completed}
        onChange={handleToggleComplete}
        className="mt-1 mr-3 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
      />
      
      {isEditing ? (
        <div className="flex-1">
          <input
            type="text"
            value={editText}
            onChange={(e) => setEditText(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:text-white"
          />
          <div className="mt-2 flex space-x-2">
            <button
              onClick={handleUpdate}
              disabled={loading}
              className="px-3 py-1 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save'}
            </button>
            <button
              onClick={() => {
                setIsEditing(false);
                setEditText(todo.description);
              }}
              className="px-3 py-1 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
            >
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <div className="flex-1">
          <div className={`${completed ? 'line-through text-gray-500 dark:text-gray-400' : ''}`}>
            {todo.description}
          </div>
          {todo.due_date && (
            <div className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Due: {new Date(todo.due_date).toLocaleDateString()}
            </div>
          )}
        </div>
      )}
      
      <div className="flex space-x-2 ml-4">
        {!isEditing && (
          <button
            onClick={() => setIsEditing(true)}
            className="p-2 text-blue-600 hover:text-blue-800 focus:outline-none"
            aria-label="Edit todo"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </button>
        )}
        <button
          onClick={handleDelete}
          className="p-2 text-red-600 hover:text-red-800 focus:outline-none"
          aria-label="Delete todo"
        >
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
  );
};

export default TodoItem;