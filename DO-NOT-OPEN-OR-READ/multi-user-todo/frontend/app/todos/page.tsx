"use client"

import { useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/contexts/AuthContext"
import { ProtectedRoute } from "@/components/ProtectedRoute"
import TodoList from "@/components/TodoList"
import TodoForm from "@/components/TodoForm"
import { todoApi } from "@/lib/api"
import { Todo } from "@/lib/types"

export default function TodosPage() {
  return (
    <ProtectedRoute>
      <TodosContent />
    </ProtectedRoute>
  )
}

function TodosContent() {
  const { user, logout } = useAuth()
  const router = useRouter()
  const [todos, setTodos] = useState<Todo[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState("")
  const [filter, setFilter] = useState<"all" | "active" | "completed">("all")
  const [editingTodo, setEditingTodo] = useState<Todo | null>(null)

  useEffect(() => {
    loadTodos()
  }, [filter])

  const loadTodos = async () => {
    setIsLoading(true)
    setError("")

    try {
      const completed = filter === "all" ? undefined : filter === "completed"
      const result = await todoApi.getAll(completed)

      if (result.error) {
        setError(result.error.message)
      } else {
        setTodos(result.data || [])
      }
    } catch (err) {
      setError("Failed to load todos")
    } finally {
      setIsLoading(false)
    }
  }

  const handleCreate = async (data: { description: string; due_date?: string }) => {
    const result = await todoApi.create(data)

    if (result.error) {
      throw new Error(result.error.message)
    }

    await loadTodos()
  }

  const handleUpdate = async (data: { description: string; due_date?: string }) => {
    if (!editingTodo) return

    const result = await todoApi.update(editingTodo.id, data)

    if (result.error) {
      throw new Error(result.error.message)
    }

    setEditingTodo(null)
    await loadTodos()
  }

  const handleToggle = async (id: string) => {
    const result = await todoApi.toggleComplete(id)

    if (result.error) {
      setError(result.error.message)
      return
    }

    await loadTodos()
  }

  const handleDelete = async (id: string) => {
    const result = await todoApi.delete(id)

    if (result.error) {
      setError(result.error.message)
      return
    }

    await loadTodos()
  }

  const handleEdit = (todo: Todo) => {
    setEditingTodo(todo)
  }

  const handleCancelEdit = () => {
    setEditingTodo(null)
  }

  const handleLogout = async () => {
    await logout()
    router.push("/login")
  }

  const stats = {
    total: todos.length,
    active: todos.filter((t) => !t.completed).length,
    completed: todos.filter((t) => t.completed).length,
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">My Todos</h1>
              <p className="text-sm text-gray-600">Welcome back, {user?.email}!</p>
            </div>
            <button
              onClick={handleLogout}
              className="px-4 py-2 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-100 rounded-lg"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2 space-y-6">
            {/* Stats */}
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-white p-4 rounded-lg shadow-sm">
                <p className="text-sm text-gray-600">Total</p>
                <p className="text-2xl font-bold text-gray-900">{stats.total}</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-sm">
                <p className="text-sm text-gray-600">Active</p>
                <p className="text-2xl font-bold text-blue-600">{stats.active}</p>
              </div>
              <div className="bg-white p-4 rounded-lg shadow-sm">
                <p className="text-sm text-gray-600">Completed</p>
                <p className="text-2xl font-bold text-green-600">{stats.completed}</p>
              </div>
            </div>

            {/* Filters */}
            <div className="bg-white p-4 rounded-lg shadow-sm">
              <div className="flex gap-2">
                <button
                  onClick={() => setFilter("all")}
                  className={`px-4 py-2 rounded-lg text-sm font-medium ${
                    filter === "all"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  All
                </button>
                <button
                  onClick={() => setFilter("active")}
                  className={`px-4 py-2 rounded-lg text-sm font-medium ${
                    filter === "active"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  Active
                </button>
                <button
                  onClick={() => setFilter("completed")}
                  className={`px-4 py-2 rounded-lg text-sm font-medium ${
                    filter === "completed"
                      ? "bg-blue-600 text-white"
                      : "bg-gray-100 text-gray-700 hover:bg-gray-200"
                  }`}
                >
                  Completed
                </button>
              </div>
            </div>

            {/* Error */}
            {error && (
              <div className="bg-red-50 text-red-700 p-4 rounded-lg">
                {error}
              </div>
            )}

            {/* Todo List */}
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <TodoList
                todos={todos}
                onToggle={handleToggle}
                onDelete={handleDelete}
                onEdit={handleEdit}
                isLoading={isLoading}
              />
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Create/Edit Form */}
            <div className="bg-white p-6 rounded-lg shadow-sm">
              <h2 className="text-lg font-semibold text-gray-900 mb-4">
                {editingTodo ? "Edit Todo" : "Create New Todo"}
              </h2>
              <TodoForm
                onSubmit={editingTodo ? handleUpdate : handleCreate}
                initialData={editingTodo || undefined}
                isEditing={!!editingTodo}
                onCancel={editingTodo ? handleCancelEdit : undefined}
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
