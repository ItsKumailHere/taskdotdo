'use client';

import React, { useState, useEffect } from 'react';
import { Todo, getTodos, updateTodoStatus, deleteTodo, updateTodo } from '@/lib/api/todo-api';
import { StatusToggle } from '../tasks/StatusToggle';
import { DeleteConfirmation } from '../tasks/DeleteConfirmation';

interface TaskListProps {
  onTaskUpdated?: () => void;
  onTaskDeleted?: () => void;
  onEditTask?: (task: { id: string; title: string; description?: string }) => void;
  filters?: {
    status: string;
    sortBy: string;
    sortOrder: string;
    searchQuery: string;
  };
}

const TaskList: React.FC<TaskListProps> = ({ onTaskUpdated, onTaskDeleted, onEditTask, filters }) => {
  const [tasks, setTasks] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editText, setEditText] = useState('');

  useEffect(() => {
    fetchTasks();
  }, [filters]);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      // Build query parameters from filters
      const params = new URLSearchParams();

      if (filters?.status && filters.status !== 'all') {
        params.append('completed', filters.status === 'completed' ? 'true' : 'false');
      }

      if (filters?.sortBy) {
        params.append('sort_by', filters.sortBy);
      }

      if (filters?.sortOrder) {
        params.append('sort_order', filters.sortOrder);
      }

      // Determine completed filter
      let completedFilter: boolean | null = null;
      if (filters?.status === 'completed') {
        completedFilter = true;
      } else if (filters?.status === 'pending') {
        completedFilter = false;
      }

      // For search, we'll filter client-side after fetching
      // In a real application, you'd want to implement server-side search
      const fetchedTasks = await getTodos(
        completedFilter,
        filters?.sortBy || 'created_at',
        (filters?.sortOrder as 'asc' | 'desc') || 'desc'
      );

      // Apply search filter client-side
      let filteredTasks = fetchedTasks;
      if (filters?.searchQuery) {
        const query = filters.searchQuery.toLowerCase();
        filteredTasks = fetchedTasks.filter(task =>
          task.title.toLowerCase().includes(query) ||
          (task.description && task.description.toLowerCase().includes(query))
        );
      }

      setTasks(filteredTasks);
    } catch (err) {
      console.error('Error fetching tasks:', err);
      setError('Failed to load tasks. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  const handleStatusChange = async (taskId: string, completed: boolean) => {
    try {
      await updateTodoStatus(taskId, completed);
      if (onTaskUpdated) {
        onTaskUpdated();
      } else {
        fetchTasks(); // Refresh tasks if no callback provided
      }
    } catch (err) {
      console.error('Error updating task status:', err);
      setError('Failed to update task status. Please try again.');
    }
  };

  const handleDelete = async (taskId: string) => {
    try {
      await deleteTodo(taskId);
      if (onTaskDeleted) {
        onTaskDeleted();
      } else {
        fetchTasks(); // Refresh tasks if no callback provided
      }
    } catch (err) {
      console.error('Error deleting task:', err);
      setError('Failed to delete task. Please try again.');
    }
  };

  const startEditing = (task: Todo) => {
    setEditingTaskId(task.id);
    setEditText(task.title);
  };

  const cancelEditing = () => {
    setEditingTaskId(null);
    setEditText('');
  };

  const saveEdit = async (taskId: string) => {
    if (!editText.trim()) {
      setError('Task title cannot be empty');
      return;
    }

    try {
      await updateTodo(taskId, { title: editText.trim() });
      setEditingTaskId(null);
      setEditText('');
      if (onTaskUpdated) {
        onTaskUpdated();
      } else {
        fetchTasks(); // Refresh tasks if no callback provided
      }
    } catch (err) {
      console.error('Error updating task:', err);
      setError('Failed to update task. Please try again.');
    }
  };

  if (error) {
    return (
      <div className="mb-4 p-4 bg-red-100 text-red-700 rounded">
        {error}
      </div>
    );
  }

  if (loading) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">Loading tasks...</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-8">
        <p className="text-gray-600">No tasks yet. Add a new task to get started!</p>
      </div>
    );
  }

  return (
    <div>
      <h2 className="text-xl font-semibold mb-4 text-gray-700">Your Tasks</h2>
      <ul className="space-y-2">
        {tasks.map((task) => (
          <li
            key={task.id}
            className={`p-4 rounded-lg border ${
              task.completed
                ? 'bg-green-50 border-green-200'
                : 'bg-white border-gray-200'
            }`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <StatusToggle
                  taskId={task.id}
                  completed={task.completed}
                  onStatusChange={handleStatusChange}
                  className="mr-3"
                />
                
                {editingTaskId === task.id ? (
                  <div className="flex items-center space-x-2">
                    <input
                      type="text"
                      value={editText}
                      onChange={(e) => setEditText(e.target.value)}
                      className="border border-gray-300 rounded px-2 py-1 flex-grow"
                      autoFocus
                    />
                    <button
                      onClick={() => saveEdit(task.id)}
                      className="bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700"
                    >
                      Save
                    </button>
                    <button
                      onClick={cancelEditing}
                      className="bg-gray-500 text-white px-3 py-1 rounded hover:bg-gray-600"
                    >
                      Cancel
                    </button>
                  </div>
                ) : (
                  <div className="flex flex-col">
                    <span className={`${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                      <strong>{task.title}</strong>
                    </span>
                    {task.description && (
                      <p className="text-gray-600 text-sm mt-1">{task.description}</p>
                    )}
                  </div>
                )}
              </div>
              
              <div className="flex space-x-2">
                {editingTaskId !== task.id && onEditTask && (
                  <button
                    onClick={() => onEditTask({ id: task.id, title: task.title, description: task.description })}
                    className="text-blue-600 hover:text-blue-800"
                  >
                    Edit
                  </button>
                )}
                
                <DeleteConfirmation
                  taskId={task.id}
                  onDelete={handleDelete}
                  taskTitle={task.title}
                />
              </div>
            </div>
            
            <div className="mt-2 text-sm text-gray-500">
              Created: {new Date(task.created_at).toLocaleString()}
              {task.updated_at && ` | Updated: ${new Date(task.updated_at).toLocaleString()}`}
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default TaskList;