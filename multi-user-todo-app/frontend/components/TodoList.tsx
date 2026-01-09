'use client';

import React, { useState, useEffect } from 'react';
import { Todo } from '../lib/types';
import TodoItem from './TodoItem';
import { apiClient } from '../lib/api';

interface TodoListProps {
  filter?: 'all' | 'active' | 'completed';
}

const TodoList: React.FC<TodoListProps> = ({ filter = 'all' }) => {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTodos();
  }, [filter]);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const params: { status?: 'pending' | 'completed' } = {};

      if (filter === 'active') {
        params.status = 'pending';
      } else if (filter === 'completed') {
        params.status = 'completed';
      }

      const response = await apiClient.getTodos(params);
      setTodos(response.data);
    } catch (err) {
      setError('Failed to fetch todos');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTodoUpdate = (updatedTodo: Todo) => {
    setTodos(todos.map(todo => 
      todo.id === updatedTodo.id ? updatedTodo : todo
    ));
  };

  const handleTodoDelete = (id: string) => {
    setTodos(todos.filter(todo => todo.id !== id));
  };

  if (loading) {
    return <div className="text-center py-4">Loading todos...</div>;
  }

  if (error) {
    return <div className="text-center py-4 text-red-500">{error}</div>;
  }

  if (todos.length === 0) {
    return <div className="text-center py-4 text-gray-500">No todos found</div>;
  }

  return (
    <div>
      {todos.map(todo => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onTodoUpdate={handleTodoUpdate}
          onTodoDelete={handleTodoDelete}
        />
      ))}
    </div>
  );
};

export default TodoList;