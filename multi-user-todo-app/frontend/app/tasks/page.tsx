"use client";

import { useState, useEffect } from "react";
import { ResponsiveNav } from "@/components/responsive-nav";
import { TaskFilter } from "@/components/task-filter";
import { TaskSort } from "@/components/task-sort";
import { SearchBar } from "@/components/search-bar";
import { TaskCard } from "@/components/task-card";
import { TodoForm } from "@/components/TodoForm";
import { apiClient } from "@/lib/api";
import { Task, TaskFilters, TodoCreate } from "@/lib/types";

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<TaskFilters>({
    status: 'all',
    sort_by: 'created_at',
    order: 'desc',
    search: '',
    page: 1,
    limit: 20
  });

  useEffect(() => {
    loadTasks();
  }, [filters]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const response = await apiClient.getTodos(filters);
      setTasks(response.data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (status: 'all' | 'pending' | 'completed') => {
    setFilters(prev => ({
      ...prev,
      status: status === 'all' ? undefined : status
    }));
  };

  const handleSortChange = (sort_by: string, order: string) => {
    setFilters(prev => ({
      ...prev,
      sort_by,
      order
    }));
  };

  const handleSearch = (search: string) => {
    setFilters(prev => ({
      ...prev,
      search
    }));
  };

  const handleToggleComplete = async (id: string, completed: boolean) => {
    try {
      // Find the task to update
      const taskToUpdate = tasks.find(task => task.id === id);
      if (!taskToUpdate) return;

      // Update the task status
      const updatedTask = await apiClient.updateTodo(id, {
        ...taskToUpdate,
        status: completed ? 'completed' : 'pending'
      });

      // Update local state
      setTasks(tasks.map(task => 
        task.id === id ? updatedTask : task
      ));
    } catch (error) {
      console.error("Error updating task:", error);
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await apiClient.deleteTodo(id);
      setTasks(tasks.filter(task => task.id !== id));
    } catch (error) {
      console.error("Error deleting task:", error);
    }
  };

  const handleAddTask = async (taskData: TodoCreate) => {
    try {
      const newTask = await apiClient.createTodo(taskData);
      setTasks([newTask, ...tasks]);
    } catch (error) {
      console.error("Error creating task:", error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
      <ResponsiveNav />
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Tasks</h1>
          <p className="text-gray-600 dark:text-gray-400">
            Manage and organize your tasks
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sidebar with filters and form */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Add New Task</h2>
              <TodoForm onSubmit={handleAddTask} />
            </div>

            <div className="bg-white dark:bg-gray-800 rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4">Filters</h2>
              <TaskFilter 
                currentFilter={filters.status || 'all'} 
                onFilterChange={handleFilterChange} 
              />
              
              <h3 className="text-md font-medium text-gray-900 dark:text-white mt-4 mb-2">Sort</h3>
              <TaskSort 
                currentSort={filters.sort_by || 'created_at'} 
                currentOrder={filters.order || 'desc'} 
                onSortChange={handleSortChange} 
              />
              
              <SearchBar onSearch={handleSearch} />
            </div>
          </div>

          {/* Task list */}
          <div className="lg:col-span-3">
            <div className="bg-white dark:bg-gray-800 rounded-lg shadow overflow-hidden">
              <div className="p-6">
                <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                  {filters.status === 'pending' ? 'Pending Tasks' : 
                   filters.status === 'completed' ? 'Completed Tasks' : 'All Tasks'}
                  <span className="text-gray-500 dark:text-gray-400 text-base ml-2">({tasks.length})</span>
                </h2>
                
                {loading ? (
                  <div className="text-center py-8">
                    <p className="text-gray-600 dark:text-gray-400">Loading tasks...</p>
                  </div>
                ) : tasks.length === 0 ? (
                  <div className="text-center py-8">
                    <p className="text-gray-600 dark:text-gray-400">
                      {filters.search ? 'No tasks match your search.' : 'No tasks found.'}
                    </p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {tasks.map(task => (
                      <TaskCard 
                        key={task.id} 
                        task={task} 
                        onToggleComplete={handleToggleComplete}
                        onDelete={handleDeleteTask}
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}