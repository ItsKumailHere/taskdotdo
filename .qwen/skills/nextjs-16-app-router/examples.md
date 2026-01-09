# Examples

## Server Component Page
```tsx
export default async function TodosPage() {
  const todos = await getTodos()
  return <TodoList todos={todos} />
}

Client Component (UI Only)

tsx
"use client"

export function TodoItem({ todo }) {
  return <button>{todo.title}</button>
}

Client Component (Allowed Fetch Case)

tsx
"use client"

import useSWR from "swr"

export function LiveStats() {
  const { data } = useSWR("/api/stats")
  return <div>{data?.count}</div>
}

Protected Layout


tsx
export default async function DashboardLayout({ children }) {
  await requireAuth()
  return <>{children}</>
}