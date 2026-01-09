# When NOT to Query Context7: Anti-Patterns

## The Over-Querying Problem

Over-querying Context7 wastes time, clutters context, and delays implementation. This guide teaches you to recognize when to trust your existing knowledge instead of reaching for documentation.

---

## Anti-Pattern #1: Querying Basic Language Syntax

### ❌ Bad Queries:
```
"Python function definition syntax"
"JavaScript arrow function"
"Python list comprehension"
"async await in Python"
"try except error handling"
"for loop in JavaScript"
```

### ✅ What You Should Do:
```python
# Just write it - you know Python syntax
async def get_todos(user_id: str):
    try:
        todos = await fetch_todos(user_id)
        return [todo for todo in todos if not todo.deleted]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Why**: These are fundamental programming concepts covered extensively in your training data. Querying adds latency without value.

---

## Anti-Pattern #2: Querying Standard Library Features

### ❌ Bad Queries:
```
"Python datetime now"
"JavaScript JSON.parse"
"Python os.environ"
"JavaScript Array.map"
"Python uuid generation"
```

### ✅ What You Should Do:
```python
from datetime import datetime, timezone
from uuid import uuid4
import os

# Just use standard library
todo_id = str(uuid4())
created_at = datetime.now(timezone.utc)
database_url = os.environ.get("DATABASE_URL")
```

**Why**: Standard library APIs are stable, well-documented in your training, and unlikely to change.

---

## Anti-Pattern #3: Querying HTTP Fundamentals

### ❌ Bad Queries:
```
"HTTP status codes meaning"
"REST API principles"
"POST vs PUT difference"
"HTTP headers format"
"JSON request body structure"
```

### ✅ What You Should Do:
```python
from fastapi import HTTPException, status

# You know HTTP status codes
@app.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: TodoCreate):
    return created_todo

@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str):
    if not found:
        raise HTTPException(status_code=404, detail="Todo not found")
```

**Why**: HTTP is a fundamental protocol; you understand status codes, methods, and REST principles.

---

## Anti-Pattern #4: Re-Querying Same Information

### ❌ Bad Pattern:
```
1. Query: "Better Auth JWT setup Next.js 16"
2. [Implement auth.ts]
3. Query: "Better Auth JWT configuration" (DUPLICATE!)
4. [Create middleware]
5. Query: "Better Auth JWT tokens" (DUPLICATE AGAIN!)
```

### ✅ Good Pattern:
```
1. Query ONCE: "Better Auth JWT complete setup Next.js 16"
2. Store key information:
   - JWT config in auth.ts
   - Token structure
   - Verification approach
3. Reference stored info for all implementations
4. Only query again if you need something NEW (e.g., refresh tokens)
```

**Why**: First query should give you enough context for all related implementations.

---

## Anti-Pattern #5: Querying for Implementation Details You Can Derive

### ❌ Bad Query:
```
"How to filter todos by user_id in SQLModel"
```

### ✅ What You Should Do:
```python
# You know SQLModel select + where pattern from previous query
from sqlmodel import select

# Just apply filtering logic
statement = select(Todo).where(Todo.user_id == current_user.id)
todos = await session.exec(statement).all()
```

**Why**: Once you understand a framework's query pattern, filtering is a derivable application of that pattern.

---

## Anti-Pattern #6: Querying Before Attempting

### ❌ Bad Workflow:
```
Task: Add a new field to Todo model

Immediate action: Query "SQLModel add field to existing model"

Better approach: 
1. Try adding field (you know SQLModel Field syntax)
2. Hit issue? THEN query about migrations/schema updates
```

### ✅ Good Workflow:
```python
# First attempt (no query needed)
class Todo(SQLModel, table=True):
    id: str = Field(primary_key=True)
    title: str
    completed: bool = False
    priority: str = "medium"  # New field - just add it

# Only query if you hit migration issues
# Query: "SQLModel Alembic migrations for schema changes"
```

**Why**: Many tasks are straightforward; query only when you encounter actual uncertainty.

---

## Anti-Pattern #7: Querying Obvious Framework Patterns

### ❌ Bad Queries After Initial Setup:
```
"FastAPI route decorator syntax" (after already using @app.get)
"SQLModel model field types" (after already defining models)
"Next.js file naming conventions" (after already creating pages)
```

### ✅ What You Should Do:
```python
# You've already used these patterns, just continue:

@app.post("/todos")  # You know decorator syntax
async def create_todo(todo: TodoCreate):  # You know async
    ...

class Todo(SQLModel, table=True):  # You know model syntax
    title: str  # You know field types
    ...
```

**Why**: After your initial Context7 queries establish patterns, subsequent uses should follow the same pattern without re-querying.

---

## Anti-Pattern #8: Querying for Debugging Basic Issues

### ❌ Bad Query:
```
"Why is my FastAPI endpoint returning 500 error"
```

### ✅ What You Should Do:
```python
# Debug systematically:
1. Check server logs (you know how to read stack traces)
2. Add print statements / logging
3. Test endpoint in isolation
4. Verify database connection

# Query ONLY if issue is framework-specific:
# "FastAPI async session handling in route dependencies"
```

**Why**: Most bugs are logic errors you can debug with standard techniques, not framework mysteries.

---

## Decision Matrix: Should I Query Context7?

```
┌────────────────────────────────────────────────────────────┐
│ Ask Yourself:                                              │
├────────────────────────────────────────────────────────────┤
│ 1. Is this framework-specific? (Not generic programming)  │
│    NO → Don't query                                        │
│    YES → Continue...                                       │
│                                                            │
│ 2. Is this about a version I'm uncertain about?           │
│    NO → Don't query                                        │
│    YES → Continue...                                       │
│                                                            │
│ 3. Have I already queried this topic in this session?     │
│    YES → Don't query (use previous results)               │
│    NO → Continue...                                        │
│                                                            │
│ 4. Can I attempt this based on existing knowledge?        │
│    YES → Try first, query if you hit a real blocker       │
│    NO → Query now                                          │
└────────────────────────────────────────────────────────────┘
```

---

## When to Trust Your Knowledge

### You Already Know (Don't Query):
- ✅ Python syntax, type hints, async/await
- ✅ JavaScript/TypeScript fundamentals
- ✅ HTTP methods, status codes, REST principles
- ✅ SQL basics (SELECT, INSERT, UPDATE, DELETE, WHERE)
- ✅ Git commands and version control
- ✅ Environment variables usage
- ✅ JSON structure and serialization
- ✅ Basic error handling patterns
- ✅ Function/class design principles
- ✅ Import/export module syntax

### You Need Context7 (Do Query):
- 🔍 Next.js 16 App Router specific patterns
- 🔍 Better Auth configuration and setup
- 🔍 FastAPI + SQLModel integration patterns
- 🔍 Neon PostgreSQL connection specifics
- 🔍 Vercel deployment configuration
- 🔍 Framework-specific async patterns
- 🔍 New APIs introduced after Jan 2025
- 🔍 Provider-specific authentication flows

---

## Example: Building a Feature Without Over-Querying

### Task: Add priority field to todos

#### ❌ Over-Querying Approach:
```
1. Query: "SQLModel add field to model"
2. Query: "SQLModel field types"
3. Query: "SQLModel migrations"
4. Query: "FastAPI return updated model"
5. Query: "SQLModel commit changes"
```

#### ✅ Efficient Approach:
```
1. Add field to model (you know Field syntax from initial query)
   class Todo(SQLModel, table=True):
       priority: str = "medium"

2. Run migration (you know create_all or Alembic from setup)
   await create_all(engine)

3. Update CRUD endpoints (you know FastAPI patterns)
   @app.patch("/todos/{todo_id}")
   async def update_todo(...):
       todo.priority = todo_update.priority
       await session.commit()

4. Query ONLY if you hit something framework-specific:
   "SQLModel enum field validation with Field()"
```

**Result**: 1 query instead of 5, faster implementation

---

## Red Flags: Signs You're Over-Querying

🚩 **Querying the same framework multiple times**
   → Cache results from first comprehensive query

🚩 **Querying after you've already used a pattern**
   → Trust the pattern you've established

🚩 **Querying before looking at error messages**
   → Read stack traces first, they often tell you the issue

🚩 **Querying for "how to" when you can "just try"**
   → Attempt implementation, query only if blocked

🚩 **Querying for basic concepts like loops, variables, functions**
   → These are fundamental knowledge

---

## The Golden Rule

**Query Context7 when you need CURRENT, FRAMEWORK-SPECIFIC knowledge.**

**Trust your training data for FUNDAMENTAL, STABLE programming concepts.**

The best developers know when to look things up and when to trust their expertise. Context7 is a tool for bridging knowledge gaps about new frameworks and versions, not a replacement for fundamental programming knowledge.

---

## Quick Self-Check

Before querying Context7, ask:

1. ✅ "Would this information be in my training data?"
2. ✅ "Is this specific to Next.js 16 / Better Auth / SQLModel?"
3. ✅ "Have I already learned this pattern in this session?"
4. ✅ "Can I attempt this and query only if stuck?"

If you answer "YES" to questions 1 or 3, or "NO" to question 2, **don't query** - trust your knowledge and implement directly.