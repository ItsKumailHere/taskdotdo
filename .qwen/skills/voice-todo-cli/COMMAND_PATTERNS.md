# Command Parsing Patterns

This document defines the exact regex patterns and keyword matching logic for parsing voice commands without LLM involvement.

## Core Parsing Logic

### Pattern Extraction Strategy
1. Convert input to lowercase
2. Search for primary action keywords
3. Extract task names and IDs based on context
4. Return structured command object

## Command Patterns

### Add Task
**Keywords**: `add`, `create`, `new`, `make`

**Extraction Pattern**:
```python
import re

def parse_add_command(text: str) -> dict:
    """
    Examples:
    - "add do boxing" → {action: 'add', task_name: 'do boxing'}
    - "please add do boxing as a todo" → {action: 'add', task_name: 'do boxing'}
    - "create new task buy groceries" → {action: 'add', task_name: 'buy groceries'}
    """
    text_lower = text.lower()
    
    # Find the action keyword
    add_keywords = ['add', 'create', 'new', 'make']
    action_keyword = None
    action_position = -1
    
    for keyword in add_keywords:
        pattern = r'\b' + keyword + r'\b'
        match = re.search(pattern, text_lower)
        if match:
            action_keyword = keyword
            action_position = match.end()
            break
    
    if action_keyword is None:
        return None
    
    # Extract everything after the action keyword as task name
    # Remove filler words: "as a todo", "as a task", "please", etc.
    task_text = text[action_position:].strip()
    
    # Remove common filler phrases
    filler_patterns = [
        r'\bas\s+a\s+todo\b',
        r'\bas\s+a\s+task\b',
        r'\bplease\b',
        r'\bfor\s+me\b',
    ]
    
    for pattern in filler_patterns:
        task_text = re.sub(pattern, '', task_text, flags=re.IGNORECASE)
    
    task_text = task_text.strip()
    
    return {
        'action': 'add',
        'task_name': task_text,
        'task_id': None
    }
```

### Delete Task
**Keywords**: `delete`, `remove`, `erase`

**ID Extraction Pattern**:
```python
def parse_delete_command(text: str) -> dict:
    """
    Examples:
    - "delete id 2" → {action: 'delete', task_id: 2}
    - "remove task 5" → {action: 'delete', task_id: 5}
    - "delete task with id 3" → {action: 'delete', task_id: 3}
    """
    text_lower = text.lower()
    
    # Find delete keyword
    delete_keywords = ['delete', 'remove', 'erase']
    has_delete_keyword = any(kw in text_lower for kw in delete_keywords)
    
    if not has_delete_keyword:
        return None
    
    # Extract ID using multiple patterns
    id_patterns = [
        r'id\s+(\d+)',           # "id 2"
        r'task\s+(\d+)',         # "task 2"
        r'number\s+(\d+)',       # "number 2"
        r'\bid\s+is\s+(\d+)',    # "id is 2"
        r'\b(\d+)\b',            # standalone number
    ]
    
    task_id = None
    for pattern in id_patterns:
        match = re.search(pattern, text_lower)
        if match:
            task_id = int(match.group(1))
            break
    
    if task_id is None:
        return {
            'action': 'delete',
            'task_id': None,
            'needs_clarification': 'task_id'
        }
    
    return {
        'action': 'delete',
        'task_id': task_id,
        'task_name': None
    }
```

### Mark Complete/Incomplete
**Keywords**: `mark`, `complete`, `done`, `finish`, `incomplete`, `uncomplete`, `undo`

**Extraction Pattern**:
```python
def parse_mark_command(text: str) -> dict:
    """
    Examples:
    - "mark id 2 as complete" → {action: 'mark_complete', task_id: 2}
    - "mark task complete id 2" → {action: 'mark_complete', task_id: 2}
    - "complete task 3" → {action: 'mark_complete', task_id: 3}
    - "mark incomplete id 1" → {action: 'mark_incomplete', task_id: 1}
    """
    text_lower = text.lower()
    
    # Determine if completing or uncompleting
    complete_keywords = ['complete', 'done', 'finish', 'finished']
    incomplete_keywords = ['incomplete', 'uncomplete', 'undo', 'unmark']
    
    is_complete = any(kw in text_lower for kw in complete_keywords)
    is_incomplete = any(kw in text_lower for kw in incomplete_keywords)
    
    if not (is_complete or is_incomplete):
        return None
    
    action = 'mark_complete' if is_complete else 'mark_incomplete'
    
    # Extract ID
    id_patterns = [
        r'id\s+(\d+)',
        r'task\s+(\d+)',
        r'number\s+(\d+)',
        r'\b(\d+)\b',
    ]
    
    task_id = None
    for pattern in id_patterns:
        match = re.search(pattern, text_lower)
        if match:
            task_id = int(match.group(1))
            break
    
    if task_id is None:
        return {
            'action': action,
            'task_id': None,
            'needs_clarification': 'task_id'
        }
    
    return {
        'action': action,
        'task_id': task_id,
        'task_name': None
    }
```

### List Tasks
**Keywords**: `list`, `show`, `display`, `view`, `all`, `see`

**Extraction Pattern**:
```python
def parse_list_command(text: str) -> dict:
    """
    Examples:
    - "list all tasks" → {action: 'list'}
    - "show me tasks" → {action: 'list'}
    - "display todos" → {action: 'list'}
    """
    text_lower = text.lower()
    
    list_keywords = ['list', 'show', 'display', 'view', 'see']
    has_list_keyword = any(kw in text_lower for kw in list_keywords)
    
    # Also check for words like "all", "tasks", "todos"
    context_words = ['all', 'tasks', 'todos', 'items']
    has_context = any(word in text_lower for word in context_words)
    
    if has_list_keyword or (has_context and len(text_lower.split()) <= 3):
        return {
            'action': 'list',
            'task_id': None,
            'task_name': None
        }
    
    return None
```

### Update Task
**Keywords**: `update`, `edit`, `change`, `modify`

**Extraction Pattern**:
```python
def parse_update_command(text: str) -> dict:
    """
    Examples:
    - "update id 2" → {action: 'update', task_id: 2}
    - "edit task 3" → {action: 'update', task_id: 3}
    - "change task 1 to buy milk" → {action: 'update', task_id: 1, new_name: 'buy milk'}
    """
    text_lower = text.lower()
    
    update_keywords = ['update', 'edit', 'change', 'modify']
    has_update_keyword = any(kw in text_lower for kw in update_keywords)
    
    if not has_update_keyword:
        return None
    
    # Extract ID
    id_patterns = [
        r'id\s+(\d+)',
        r'task\s+(\d+)',
        r'\b(\d+)\b',
    ]
    
    task_id = None
    for pattern in id_patterns:
        match = re.search(pattern, text_lower)
        if match:
            task_id = int(match.group(1))
            break
    
    # Try to extract new task name if "to" keyword present
    new_name = None
    to_pattern = r'\bto\s+(.+)$'
    to_match = re.search(to_pattern, text_lower)
    if to_match:
        new_name = to_match.group(1).strip()
    
    if task_id is None:
        return {
            'action': 'update',
            'task_id': None,
            'new_name': new_name,
            'needs_clarification': 'task_id'
        }
    
    return {
        'action': 'update',
        'task_id': task_id,
        'new_name': new_name,
        'task_name': None
    }
```

## Master Parsing Function

Combine all patterns into a single parser:

```python
def parse_voice_command(text: str) -> dict:
    """
    Main parsing function that tries all command patterns.
    Returns command dict or None if no pattern matches.
    """
    # Try each command parser in priority order
    parsers = [
        parse_add_command,
        parse_mark_command,
        parse_delete_command,
        parse_update_command,
        parse_list_command,
    ]
    
    for parser in parsers:
        result = parser(text)
        if result is not None:
            return result
    
    # No pattern matched
    return {
        'action': 'unknown',
        'raw_text': text,
        'needs_clarification': 'command'
    }
```

## Clarification Handling

When IDs or other info is missing:

```python
def handle_clarification(parsed_command: dict) -> str:
    """
    Generate clarification prompts based on missing information.
    """
    if 'needs_clarification' not in parsed_command:
        return None
    
    needs = parsed_command['needs_clarification']
    
    clarifications = {
        'task_id': "Please provide the task ID. Say 'id' followed by the number (e.g., 'id 2')",
        'command': "I didn't understand that command. Try: 'add [task]', 'list', 'delete id [number]', or 'mark complete id [number]'"
    }
    
    return clarifications.get(needs, "Please clarify your command")
```

## Testing Patterns

Test each pattern with various phrasings:

```python
# Add command tests
assert parse_add_command("add do boxing")['task_name'] == "do boxing"
assert parse_add_command("please add do boxing as a todo")['task_name'] == "do boxing"
assert parse_add_command("create buy groceries")['task_name'] == "buy groceries"

# Delete command tests
assert parse_delete_command("delete id 2")['task_id'] == 2
assert parse_delete_command("remove task 5")['task_id'] == 5

# Mark command tests
assert parse_mark_command("mark complete id 2")['action'] == 'mark_complete'
assert parse_mark_command("mark incomplete id 1")['action'] == 'mark_incomplete'

# List command tests
assert parse_list_command("list all tasks")['action'] == 'list'
assert parse_list_command("show me todos")['action'] == 'list'
```

## Edge Cases

Handle these special cases:

1. **Multiple numbers in input**: Use first number after action keyword
2. **No clear action word**: Return unknown command
3. **Task name contains numbers**: Don't extract as ID if not after "id" or "task"
4. **Empty task name after add**: Request clarification
5. **ID out of range**: Handle at execution level, not parsing level