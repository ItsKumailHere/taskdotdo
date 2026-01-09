"use client"

import { Todo } from "@/lib/types"
import TodoItem from "./TodoItem"

interface TodoListProps {
  todos: Todo[]
  onToggle: (id: string) => void
  onDelete: (id: string) => void
  onEdit: (todo: Todo) => void
  isLoading?: boolean
}

export default function TodoList({ todos, onToggle, onDelete, onEdit, isLoading }: TodoListProps) {
  if (isLoading) {
    return (
      <div className="space-y-3">
        {[1, 2, 3].map((i) => (
          <div key={i} className="h-24 bg-gray-100 rounded-lg animate-pulse" />
        ))}
      </div>
    )
  }

  if (todos.length === 0) {
    return (
      <div className="text-center py-12 text-gray-500">
        <p className="text-xl mb-2">No todos yet!</p>
        <p className="text-sm">Create your first todo to get started.</p>
      </div>
    )
  }

  return (
    <div className="space-y-3">
      {todos.map((todo) => (
        <TodoItem
          key={todo.id}
          todo={todo}
          onToggle={onToggle}
          onDelete={onDelete}
          onEdit={onEdit}
        />
      ))}
    </div>
  )
}
