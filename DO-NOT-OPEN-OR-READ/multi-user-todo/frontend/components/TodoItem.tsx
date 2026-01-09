"use client"

import { Todo } from "@/lib/types"
import { formatDistanceToNow } from "date-fns"
import { useState } from "react"

interface TodoItemProps {
  todo: Todo
  onToggle: (id: string) => void
  onDelete: (id: string) => void
  onEdit: (todo: Todo) => void
}

export default function TodoItem({ todo, onToggle, onDelete, onEdit }: TodoItemProps) {
  const [isDeleting, setIsDeleting] = useState(false)

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this todo?")) return
    setIsDeleting(true)
    await onDelete(todo.id)
  }

  return (
    <div
      className={`p-4 border rounded-lg hover:shadow-md transition-shadow ${
        todo.completed ? "bg-gray-50" : "bg-white"
      }`}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox */}
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => onToggle(todo.id)}
          className="mt-1 w-5 h-5 cursor-pointer"
        />

        {/* Content */}
        <div className="flex-1">
          <p
            className={`text-lg ${
              todo.completed ? "line-through text-gray-500" : "text-gray-900"
            }`}
          >
            {todo.description}
          </p>

          {/* Metadata */}
          <div className="flex flex-wrap gap-3 mt-2 text-sm text-gray-600">
            {todo.due_date && (
              <span>
                Due: {formatDistanceToNow(new Date(todo.due_date), { addSuffix: true })}
              </span>
            )}
            {todo.category_id && (
              <span className="px-2 py-0.5 bg-blue-100 text-blue-700 rounded">
                {todo.category_id}
              </span>
            )}
            <span className="text-xs text-gray-400">
              Created {formatDistanceToNow(new Date(todo.created_at), { addSuffix: true })}
            </span>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-2">
          <button
            onClick={() => onEdit(todo)}
            className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded"
            disabled={isDeleting}
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            className="px-3 py-1 text-sm text-red-600 hover:text-red-800 hover:bg-red-50 rounded"
            disabled={isDeleting}
          >
            {isDeleting ? "Deleting..." : "Delete"}
          </button>
        </div>
      </div>
    </div>
  )
}
