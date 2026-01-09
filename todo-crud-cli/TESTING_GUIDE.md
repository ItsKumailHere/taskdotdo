# Testing Guide for Voice-Enabled Todo CLI

## Test Coverage Summary

### Voice Command Parser Tests (`tests/test_voice_parser.py`)

**Total: 47 tests - All Passing ✅**

#### Test Categories

1. **List Commands (5 tests)**
   - Basic list command
   - Show/display variations
   - Natural language phrasings
   - All passing ✅

2. **Add Commands (6 tests)**
   - Simple additions
   - Create/new variations
   - Long descriptions
   - Polite phrasings ("please add...")
   - All passing ✅

3. **Complete Commands (6 tests)**
   - Mark done/complete
   - Task ID extraction
   - "mark as complete" variations
   - Task number patterns
   - All passing ✅

4. **Delete Commands (4 tests)**
   - Delete/remove variations
   - ID extraction patterns
   - All passing ✅

5. **Edit Commands (5 tests)**
   - Update/edit/change variations
   - Long descriptions
   - "to" and "with" connectors
   - All passing ✅

6. **Help Command (2 tests)**
   - Basic help
   - Polite variations
   - All passing ✅

7. **Ambiguous Commands (6 tests)**
   - Empty strings
   - Random text
   - Incomplete commands
   - Commands without required parameters
   - All passing ✅

8. **Case Insensitivity (3 tests)**
   - Uppercase commands
   - Mixed case
   - All passing ✅

9. **Natural Language Variations (5 tests)**
   - Polite phrasings
   - Conversational language
   - Punctuation handling
   - Multiple numbers in input
   - All passing ✅

10. **Edge Cases (5 tests)**
    - Whitespace handling
    - Numeric descriptions
    - Zero IDs
    - Large IDs
    - Special characters
    - All passing ✅

## Running Tests

### Run All Voice Parser Tests
```bash
uv run pytest tests/test_voice_parser.py -v
```

### Run Specific Test Class
```bash
uv run pytest tests/test_voice_parser.py::TestAddCommands -v
```

### Run Single Test
```bash
uv run pytest tests/test_voice_parser.py::TestAddCommands::test_add_simple -v
```

### Run All Tests in Project
```bash
uv run pytest tests/ -v
```

### Run with Coverage
```bash
uv run pytest tests/ --cov=todo_cli --cov-report=html
```

## Test Examples

### Add Command Variations
```python
"add buy milk" → {"action": "add", "description": "buy milk"}
"please add do boxing as a todo" → {"action": "add", "description": "do boxing as a todo"}
"create task record the video" → {"action": "add", "description": "record the video"}
```

### Complete Command Variations
```python
"done 1" → {"action": "done", "id": 1}
"mark task as complete, id is 2" → {"action": "done", "id": 2}
"complete task number 10" → {"action": "done", "id": 10}
```

### Edit Command Variations
```python
"edit 1 to buy chocolate" → {"action": "edit", "id": 1, "description": "buy chocolate"}
"update 7 to complete all unit tests" → {"action": "edit", "id": 7, "description": "complete all unit tests"}
```

### Delete Command Variations
```python
"delete 1" → {"action": "rm", "id": 1}
"remove task id 12" → {"action": "rm", "id": 12}
```

### List Command Variations
```python
"list" → {"action": "ls"}
"show all tasks" → {"action": "ls"}
"display tasks" → {"action": "ls"}
```

## Parser Design Principles

1. **No LLM Dependency**: Pure regex and keyword matching
2. **Order Matters**: More specific patterns checked before general ones
3. **Graceful Degradation**: Returns `None` for unparseable input
4. **Case Insensitive**: All input converted to lowercase
5. **Flexible Matching**: Supports multiple natural language variations

## Key Parser Features

- ✅ Handles polite language ("please", "could you")
- ✅ Case insensitive
- ✅ Flexible word order
- ✅ Multiple keyword variations per command
- ✅ Extracts IDs from various positions
- ✅ Handles punctuation in descriptions
- ✅ Validates completeness (e.g., "add" without description returns None)

## Adding New Tests

When adding new voice command patterns:

1. Add test in appropriate test class
2. Run tests to verify parser handles it
3. If test fails, update parser regex patterns
4. Ensure no regression in existing tests
5. Document new pattern in this guide

## Integration with Voice Input

The parser works with both:
- **Live microphone input** (when available)
- **File-based audio** (WAV/AIFF/FLAC)
- **Typed text** (fallback mode)

All inputs are processed through the same parser, ensuring consistent behavior.
