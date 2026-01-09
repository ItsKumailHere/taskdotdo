"use client"

/**
 * Reusable authentication form component for login and registration.
 *
 * This is a Client Component because it uses useState and form handlers.
 */

import { useState, FormEvent } from "react"

interface AuthFormProps {
  mode: "login" | "register"
  onSubmit: (data: AuthFormData) => Promise<void>
  isLoading: boolean
}

export interface AuthFormData {
  email: string
  password: string
  username?: string
}

export function AuthForm({ mode, onSubmit, isLoading }: AuthFormProps) {
  const [formData, setFormData] = useState<AuthFormData>({
    email: "",
    password: "",
    username: "",
  })
  const [error, setError] = useState<string>("")

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault()
    setError("")

    try {
      await onSubmit(formData)
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {mode === "register" && (
        <div>
          <label htmlFor="username" className="block text-sm font-medium text-gray-700">
            Username
          </label>
          <input
            id="username"
            type="text"
            required
            minLength={3}
            maxLength={30}
            pattern="^[a-zA-Z0-9_]+$"
            value={formData.username}
            onChange={(e) => setFormData({ ...formData, username: e.target.value })}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            placeholder="johndoe"
          />
          <p className="mt-1 text-xs text-gray-500">
            3-30 characters, alphanumeric and underscores only
          </p>
        </div>
      )}

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-gray-700">
          Email
        </label>
        <input
          id="email"
          type="email"
          required
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
          placeholder="you@example.com"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-gray-700">
          Password
        </label>
        <input
          id="password"
          type="password"
          required
          minLength={8}
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
          placeholder="••••••••"
        />
        {mode === "register" && (
          <p className="mt-1 text-xs text-gray-500">
            Minimum 8 characters
          </p>
        )}
      </div>

      {error && (
        <div className="rounded-md bg-red-50 p-3 text-sm text-red-800">
          {error}
        </div>
      )}

      <button
        type="submit"
        disabled={isLoading}
        className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {isLoading ? (
          <span className="flex items-center">
            <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Processing...
          </span>
        ) : (
          mode === "login" ? "Sign In" : "Create Account"
        )}
      </button>
    </form>
  )
}
