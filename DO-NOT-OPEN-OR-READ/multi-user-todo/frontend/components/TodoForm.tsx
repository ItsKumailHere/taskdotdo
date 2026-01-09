"use client"

import { Todo } from "@/lib/types"
import { useState, useEffect } from "react"

interface TodoFormProps {
  onSubmit: (data: { description: string; due_date?: string; category_id?: string }) => Promise<void>
  initialData?: Todo
  isEditing?: boolean
  onCancel?: () => void
}

export default function TodoForm({ onSubmit, initialData, isEditing, onCancel }: TodoFormProps) {
  const [description, setDescription] = useState(initialData?.description || "")
  const [dueDate, setDueDate] = useState(
    initialData?.due_date ? new Date(initialData.due_date).toISOString().slice(0, 16) : ""
  )
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (initialData) {
      setDescription(initialData.description)
      setDueDate(
        initialData.due_date ? new Date(initialData.due_date).toISOString().slice(0, 16) : ""
      )
    }
  }, [initialData])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!description.trim()) {
      setError("Description is required")
      return
    }

    if (description.length > 500) {
      setError("Description must be 500 characters or less")
      return
    }

    setIsSubmitting(true)

    try {
      await onSubmit({
        description: description.trim(),
        due_date: dueDate || undefined,
      })

      // Reset form if not editing
      if (!isEditing) {
        setDescription("")
        setDueDate("")
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to save todo")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {/* Description */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium text-gray-700 mb-1">
          Description *
        </label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="What needs to be done?"
          rows={3}
          maxLength={500}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isSubmitting}
        />
        <p className="mt-1 text-xs text-gray-500">{description.length}/500 characters</p>
      </div>

      {/* Due Date */}
      <div>
        <label htmlFor="due_date" className="block text-sm font-medium text-gray-700 mb-1">
          Due Date (Optional)
        </label>
        <input
          id="due_date"
          type="datetime-local"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={isSubmitting}
        />
      </div>

      {/* Error */}
      {error && (
        <div className="p-3 bg-red-50 text-red-700 text-sm rounded-lg">
          {error}
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3">
        <button
          type="submit"
          disabled={isSubmitting}
          className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          {isSubmitting ? "Saving..." : isEditing ? "Update Todo" : "Add Todo"}
        </button>
        {isEditing && onCancel && (
          <button
            type="button"
            onClick={onCancel}
            disabled={isSubmitting}
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50"
          >
            Cancel
          </button>
        )}
      </div>
    </form>
  )
}
