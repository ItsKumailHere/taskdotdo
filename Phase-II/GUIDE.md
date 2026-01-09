   # Manual Testing Guide for TaskDo CRUD Implementation

This guide will walk you through manually testing the TaskDo application to validate the implementation of all CRUD operations and features.

## Prerequisites

Before starting the tests, ensure you have:

1. The backend server running on `http://localhost:8000`
2. The frontend running on `http://localhost:3000`
3. A registered user account for testing
4. Access to the database (PostgreSQL/Neon) for verification

## Test Environment Setup

### Backend Server
1. Navigate to the backend directory:
   ```bash
   cd /mnt/c/Users/DELL/desktop/panaversity-hackathons/hackathon-ii/taskdotdo/Phase-II/backend
   ```
2. Start the backend server:
   ```bash
   uv run python main.py
   ```

### Frontend Server
1. Navigate to the frontend directory:
   ```bash
   cd /mnt/c/Users/DELL/desktop/panaversity-hackathons/hackathon-ii/taskdotdo/Phase-II/frontend
   ```
2. Start the frontend server:
   ```bash
   npm run dev
   ```

## Test Cases

### 1. User Registration and Login
**Objective**: Verify that user authentication works properly

1. Open your browser and navigate to `http://localhost:3000`
2. Click on the "Register" link
3. Fill in the registration form with:
   - Name: Test User
   - Email: test@example.com
   - Password: TestPassword123!
4. Submit the form and verify you receive a success message
5. Navigate to the login page and log in with the credentials
6. Verify you're redirected to the dashboard

### 2. Create New Tasks (User Story 1)
**Objective**: Verify that authenticated users can create new tasks

1. Log in to the application
2. Navigate to the dashboard
3. Locate the "Add New Task" form
4. Fill in the form with:
   - Title: "Test Task 1"
   - Description: "This is a test task for validation"
5. Click "Create Task"
6. Verify the task appears in the task list
7. Create a few more tasks with different titles and descriptions
8. Verify all tasks appear in the list

### 3. View All Tasks (User Story 2)
**Objective**: Verify that authenticated users can view all their tasks

1. Log in to the application
2. Navigate to the dashboard
3. Verify all tasks created in the previous step are displayed
4. Verify that each task shows:
   - Title
   - Description (if provided)
   - Creation date
   - Update date (if updated)
   - Completion status
5. Create additional tasks in another session and verify they appear after refresh

### 4. Update Existing Tasks (User Story 3)
**Objective**: Verify that authenticated users can update their existing tasks

1. Log in to the application
2. Navigate to the dashboard
3. Find an existing task in the list
4. Click the "Edit" button for that task
5. The form should populate with the task's current information
6. Modify the title and/or description
7. Click "Update Task"
8. Verify the task in the list reflects the updated information
9. Verify the "Updated" timestamp has changed

### 5. Mark Tasks Complete/Incomplete (User Story 5)
**Objective**: Verify that authenticated users can mark tasks as complete or incomplete

1. Log in to the application
2. Navigate to the dashboard
3. Find a pending task in the list
4. Click the toggle switch next to the task
5. Verify the task's status changes to "Completed" (visual indication like strikethrough)
6. Find a completed task in the list
7. Click the toggle switch next to the task
8. Verify the task's status changes back to "Pending"
9. Verify the "Updated" timestamp changes when toggling status

### 6. Delete Tasks (User Story 4)
**Objective**: Verify that authenticated users can delete tasks

1. Log in to the application
2. Navigate to the dashboard
3. Find a task in the list that you wish to delete
4. Click the "Delete" button for that task
5. A confirmation dialog should appear
6. Confirm the deletion
7. Verify the task is removed from the list
8. Verify the task statistics update appropriately

### 7. Task Filtering and Sorting (Phase 7)
**Objective**: Verify that filtering and sorting features work correctly

1. Log in to the application
2. Navigate to the dashboard
3. Create several tasks with different statuses (some completed, some pending)
4. Use the "Filter & Sort Tasks" section:
   - **Status Filter**: Select "Completed" and verify only completed tasks are shown
   - **Status Filter**: Select "Pending" and verify only pending tasks are shown
   - **Status Filter**: Select "All Tasks" and verify all tasks are shown
   - **Sort By**: Change to "Title" and verify tasks are sorted alphabetically
   - **Sort By**: Change to "Created Date" and verify tasks are sorted by creation date
   - **Sort By**: Change to "Updated Date" and verify tasks are sorted by update date
   - **Sort Order**: Change to "Ascending" and verify order changes
   - **Sort Order**: Change to "Descending" and verify order changes
   - **Search**: Enter text that matches a task title or description and verify only matching tasks are shown

### 8. Task Statistics (Phase 7)
**Objective**: Verify that task statistics are calculated and displayed correctly

1. Log in to the application
2. Navigate to the dashboard
3. Verify the statistics cards show:
   - Total Tasks: Count of all tasks
   - Completed: Count of completed tasks
   - Pending: Count of pending tasks
4. Perform some operations (create, complete, delete tasks)
5. Verify the statistics update appropriately after refresh

### 9. Error Handling
**Objective**: Verify proper error handling for invalid operations

1. Try to update a task with an empty title
   - Expected: Error message "Title is required"
2. Try to create a task with an empty title
   - Expected: Error message "Title is required"
3. Try to access another user's tasks directly (if possible through API)
   - Expected: 404 or 403 error
4. Try to update/delete a task that doesn't exist
   - Expected: Appropriate error message

### 10. Session Management
**Objective**: Verify that tasks are properly isolated by user

1. Register two different users
2. Log in as User 1 and create several tasks
3. Log out and log in as User 2
4. Verify User 2 does not see User 1's tasks
5. Create tasks as User 2
6. Log out and log back in as User 1
7. Verify User 1 only sees their own tasks

## Database Verification

For additional validation, you can directly check the database:

1. Connect to your PostgreSQL/Neon database
2. Query the `todos` table:
   ```sql
   SELECT * FROM todos WHERE user_id = '<your-user-id>';
   ```
3. Verify that all tasks created through the UI appear in the database
4. Verify that deleted tasks are removed from the database
5. Verify that updated tasks reflect changes in the database
6. Verify that completed tasks have the `completed` field set to `true`

## API Endpoint Testing

You can also test the API endpoints directly using curl or a tool like Postman:

1. **Get all tasks**: `GET /api/v1/todos`
2. **Create task**: `POST /api/v1/todos` with JSON body `{"title": "Test", "description": "Test description"}`
3. **Get specific task**: `GET /api/v1/todos/{id}`
4. **Update task**: `PUT /api/v1/todos/{id}` with JSON body `{"title": "Updated title"}`
5. **Update task status**: `PATCH /api/v1/todos/{id}/status` with JSON body `{"completed": true}`
6. **Delete task**: `DELETE /api/v1/todos/{id}`

## Expected Outcomes

After completing all tests, you should have verified:

- ✅ Users can register and log in
- ✅ Users can create new tasks
- ✅ Users can view all their tasks
- ✅ Users can update existing tasks
- ✅ Users can mark tasks as complete/incomplete
- ✅ Users can delete tasks
- ✅ Tasks can be filtered by status
- ✅ Tasks can be sorted by various fields
- ✅ Tasks can be searched by content
- ✅ Task statistics are displayed correctly
- ✅ Proper error handling for invalid operations
- ✅ Tasks are properly isolated between users
- ✅ All operations are persisted in the database

## Troubleshooting

If any tests fail:

1. Check the browser console for JavaScript errors
2. Check the backend server logs for error messages
3. Verify the database connection is working
4. Ensure all environment variables are properly set
5. Confirm the authentication tokens are being sent with requests
6. Verify the CORS settings allow frontend-backend communication

This testing guide covers all aspects of the implemented TaskDo application functionality, ensuring a comprehensive validation of the CRUD operations and additional features.