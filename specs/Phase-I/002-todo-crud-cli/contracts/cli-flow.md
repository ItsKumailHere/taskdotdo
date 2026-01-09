# CLI Contract: Interaction Flow

## Input Patterns

The application uses an interactive loop based on `questionary`.

### Main Menu
- **Prompt**: "Select an action"
- **Type**: `select`
- **Options**: `["Add Task", "List Tasks", "Update Task", "Complete Task", "Delete Task", "Exit"]`

### Task Creation
1. User selects "Add Task".
2. **Prompt**: "Enter task description"
3. **Type**: `text`
4. **Validation**: Must not be empty, max 255 characters.

### Task Update
1. User selects "Update Task".
2. **Prompt**: "Enter Task ID to update"
3. **Type**: `text` (validated as `int`)
4. **Validation**: Task must exist.
5. **Prompt**: "Enter new description"
6. **Type**: `text`

## Error Taxonomy

| Error Case | Message Pattern | Action |
|------------|-----------------|--------|
| Task Not Found | "❌ Error: Task with ID {id} not found." | Return to Main Menu |
| Invalid ID | "❌ Error: Please enter a valid numeric ID." | Retry Input |
| Empty Description | "❌ Error: Description cannot be empty." | Retry Input |
| Long Description | "❌ Error: Description exceeds 255 characters." | Retry Input |
| Store Failure | "❌ IO Error: Could not save to todos.json." | Log and Exit |

## Output Formatting

- **Success**: "✅ Success: [Action Description]"
- **List Table**:
  - Columns: `ID`, `Status`, `Description`
  - Styling: Color status (Green for Completed, Yellow for Pending).
