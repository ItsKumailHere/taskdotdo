"use client"

/**
 * Auth Context for managing authentication state across the application.
 *
 * This is a Client Component because it uses React hooks (useState, useEffect, useContext).
 */

import { createContext, useContext, useState, useEffect, ReactNode } from "react"
import { User } from "@/lib/types"
import { getSession, saveSession, clearSession } from "@/lib/auth"

interface AuthContextType {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  login: (token: string, user: User, expiresAt: string) => void
  logout: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Load session on mount
  useEffect(() => {
    const session = getSession()
    if (session) {
      setUser(session.user)
    }
    setIsLoading(false)
  }, [])

  const login = (token: string, user: User, expiresAt: string) => {
    saveSession({ user, token, expires_at: expiresAt })
    setUser(user)
  }

  const logout = () => {
    clearSession()
    setUser(null)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated: !!user,
        isLoading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}
