'use client';

import React, { useState } from 'react';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import TaskForm from '@/components/tasks/TaskForm';
import TaskList from '@/components/tasks/TaskList';
import { TaskFilters } from '@/components/tasks/TaskFilters';
import { getTodos, Todo } from '@/lib/api/todo-api';

const DashboardPage = () => {
  const [editingTask, setEditingTask] = useState<{ id: string; title: string; description?: string } | null>(null);
  const [filters, setFilters] = useState({
    status: 'all',
    sortBy: 'created_at',
    sortOrder: 'desc',
    searchQuery: ''
  });
  const [taskStats, setTaskStats] = useState({ total: 0, completed: 0, pending: 0 });

  const handleTaskUpdated = () => {
    setEditingTask(null);
    // Refresh the task list when a task is updated
    window.location.reload();
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
  };

  const handleFilterChange = (newFilters: {
    status: string;
    sortBy: string;
    sortOrder: string;
    searchQuery: string;
  }) => {
    setFilters(newFilters);
  };

  // Calculate task statistics
  React.useEffect(() => {
    const calculateStats = async () => {
      try {
        const allTasks = await getTodos();
        const total = allTasks.length;
        const completed = allTasks.filter(task => task.completed).length;
        const pending = total - completed;

        setTaskStats({
          total,
          completed,
          pending
        });
      } catch (error) {
        console.error('Error calculating task stats:', error);
      }
    };

    calculateStats();
  }, []);

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>

      {/* Task Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="bg-blue-100 p-4 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-blue-800">Total Tasks</h3>
          <p className="text-3xl font-bold text-blue-600">{taskStats.total}</p>
        </div>
        <div className="bg-green-100 p-4 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-green-800">Completed</h3>
          <p className="text-3xl font-bold text-green-600">{taskStats.completed}</p>
        </div>
        <div className="bg-yellow-100 p-4 rounded-lg shadow">
          <h3 className="text-lg font-semibold text-yellow-800">Pending</h3>
          <p className="text-3xl font-bold text-yellow-600">{taskStats.pending}</p>
        </div>
      </div>

      <TaskForm
        onTaskCreated={() => {
          // Refresh the task list when a new task is created
          window.location.reload();
        }}
        editingTask={editingTask}
        onTaskUpdated={handleTaskUpdated}
        onCancelEdit={handleCancelEdit}
      />

      <TaskFilters onFilterChange={handleFilterChange} />

      <TaskList
        onTaskUpdated={() => {
          // Refresh the task list when a task is updated
          window.location.reload();
        }}
        onTaskDeleted={() => {
          // Refresh the task list when a task is deleted
          window.location.reload();
        }}
        onEditTask={(task) => {
          setEditingTask(task);
        }}
        filters={filters}
      />
    </div>
  );
};

const DashboardWithAuth = () => (
  <ProtectedRoute>
    <DashboardPage />
  </ProtectedRoute>
);

export default DashboardWithAuth;