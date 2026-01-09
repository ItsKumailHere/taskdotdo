"use client"

/**
 * Login page - Client Component
 *
 * This must be a Client Component because it uses:
 * - useState for form handling
 * - useRouter for navigation
 * - useAuth for authentication
 */

import { useState } from "react"
import { useRouter } from "next/navigation"
import Link from "next/link"
import { AuthForm, AuthFormData } from "@/components/AuthForm"
import { useAuth } from "@/contexts/AuthContext"
import { authApi } from "@/lib/api"

export default function LoginPage() {
  const [isLoading, setIsLoading] = useState(false)
  const router = useRouter()
  const { login } = useAuth()

  const handleLogin = async (data: AuthFormData) => {
    setIsLoading(true)

    try {
      const response = await authApi.login({
        email: data.email,
        password: data.password,
      })

      if (response.error) {
        throw new Error(response.error.message)
      }

      if (response.data) {
        // Save session and update auth context
        login(response.data.token, response.data.user, response.data.expires_at)

        // Redirect to dashboard
        router.push("/dashboard")
      }
    } catch (error) {
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Or{" "}
            <Link href="/register" className="font-medium text-blue-600 hover:text-blue-500">
              create a new account
            </Link>
          </p>
        </div>

        <div className="mt-8 bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <AuthForm mode="login" onSubmit={handleLogin} isLoading={isLoading} />
        </div>
      </div>
    </div>
  )
}
