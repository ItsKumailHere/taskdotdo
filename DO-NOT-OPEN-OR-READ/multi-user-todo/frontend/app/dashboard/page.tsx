"use client"

/**
 * Dashboard page - Redirects to /todos
 */

import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { ProtectedRoute } from "@/components/ProtectedRoute"

export default function DashboardPage() {
  const router = useRouter()

  useEffect(() => {
    router.push("/todos")
  }, [router])

  return (
    <ProtectedRoute>
      <div className="min-h-screen flex items-center justify-center">
        <p className="text-gray-600">Redirecting to todos...</p>
      </div>
    </ProtectedRoute>
  )
}
