---
name: voice-todo-cli-builder
description: Builds voice-enabled CLI todo applications with speech-to-text input, keyword parsing, and persistent JSON storage. Use when creating or extending CLI todo apps with voice control capabilities, or when working with SpeechRecognition and command parsing.
allowed-tools: Read, Write, Bash, Grep, Glob
---

# Voice-Enabled Todo CLI Builder

This SKILL guides the implementation of a hybrid CLI todo application that accepts both typed and voice commands. Users can control the entire app through voice while receiving text-based feedback.

## Core Requirements

### Voice Input Architecture
- Use `SpeechRecognition` library with Google Speech API for voice-to-text
- NO LLM involvement - pure keyword extraction and pattern matching
- Support both voice and typed input seamlessly
- Return text output only (no text-to-speech required)

### Command Parsing Strategy
- Extract command keywords using regex and string matching
- Pattern-based parsing: detect "add", "delete", "mark", "complete", "list", "update", "id"
- Handle natural language variations without LLM:
  - "please add do boxing as a todo" → extract "add" + "do boxing"
  - "mark task as complete, id is 2" → extract "mark complete" + "id 2"
  - "show me all tasks" → extract "list"

### Storage and Installation
- Persistent JSON storage in `~/.todo-app/tasks.json`
- Global installation via curl script
- UV package manager for Python 3.12+
- Cross-platform compatibility

## Implementation Steps

### 1. Project Setup
```bash
# Initialize with UV
uv init voice-todo-cli
cd voice-todo-cli
```

### 2. Dependencies
Add to `pyproject.toml`:
```toml
[project]
name = "voice-todo-cli"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    "SpeechRecognition>=3.10.0",
    "pyaudio>=0.2.13",
    "pyyaml>=6.0",
]

[project.scripts]
todo-voice = "voice_todo_cli.main:main"
```

### 3. Project Structure
```
voice-todo-cli/
├── constitution.yaml
├── specs/
│   ├── 01-voice-input-spec.md
│   ├── 02-command-parser-spec.md
│   ├── 03-persistent-storage-spec.md
│   └── 04-installation-spec.md
├── src/voice_todo_cli/
│   ├── __init__.py
│   ├── main.py
│   ├── voice_input.py
│   ├── command_parser.py
│   ├── task_manager.py
│   └── storage.py
├── install.sh
├── pyproject.toml
├── README.md
└── CLAUDE.md
```

### 4. Core Modules

#### voice_input.py
- Initialize microphone with `speech_recognition.Microphone()`
- Listen with timeout and phrase time limit
- Return raw text string
- Handle errors: no mic, no speech, API issues
- Provide fallback to typed input on voice failure

#### command_parser.py
- Define command patterns using regex
- Extract keywords: add, delete, mark, complete, list, update, show
- Extract task names and IDs from natural language
- Return structured command dict: `{action: str, task_name: str, task_id: int}`
- Handle ambiguous input with clarification prompts

#### storage.py
- Create `~/.todo-app/` directory if missing
- Read/write JSON atomically
- Schema: `{tasks: [{id, title, description, completed, created_at}]}`
- Auto-increment task IDs
- Handle file corruption gracefully

#### task_manager.py
- Integrate existing todo functionality
- Add voice command routing
- Maintain backwards compatibility with typed commands

### 5. Command Parsing Patterns

For detailed parsing logic, see [COMMAND_PATTERNS.md](COMMAND_PATTERNS.md).

Key patterns:
```python
# Add task: "add", "create", "new" + task description
# Delete: "delete", "remove" + "id" + number
# Complete: "mark", "complete", "done" + "id" + number  
# List: "list", "show", "display", "all"
# Update: "update", "edit", "change" + "id" + number
```

### 6. Voice Interaction Flow

For complete interaction examples, see [INTERACTION_EXAMPLES.md](INTERACTION_EXAMPLES.md).

Basic flow:
1. User speaks or types command
2. If voice: convert speech → text
3. Parse text for keywords and IDs
4. Execute command
5. Display result as text
6. Await next input

### 7. Installation Script

For complete installation script, see [INSTALL_SCRIPT.md](INSTALL_SCRIPT.md).

Create `install.sh` for curl-based installation:
```bash
#!/bin/bash
# Download, install, and configure voice-todo-cli globally
```

## Testing Strategy

### Voice Command Tests
- Test each command pattern with multiple phrasings
- Verify ID extraction from various positions
- Test error handling for missing/invalid IDs
- Verify fallback to typed input on voice failure

### Storage Tests
- Verify JSON file creation in `~/.todo-app/`
- Test concurrent access handling
- Verify task ID auto-increment
- Test recovery from corrupted JSON

### Integration Tests
- Test voice + typed command mixing
- Verify persistent storage across sessions
- Test installation script on clean system

## Error Handling

### Voice Input Errors
- No microphone: prompt for typed input
- No speech detected: timeout and retry
- API failure: fallback to typed mode
- Always provide clear feedback

### Parsing Errors
- Ambiguous commands: request clarification
- Missing IDs: prompt user for ID
- Invalid IDs: show available task IDs
- Use conversational error messages

## Best Practices

1. **No LLM dependency**: All parsing via regex/string matching
2. **Progressive prompting**: Ask for missing info (e.g., task ID)
3. **Atomic operations**: All storage writes are atomic
4. **Graceful degradation**: Voice fails → typed input works
5. **Clear feedback**: Every action confirms result
6. **Cross-platform paths**: Use `pathlib.Path` for all file operations

## Supporting Documentation

- [COMMAND_PATTERNS.md](COMMAND_PATTERNS.md) - Detailed regex patterns and parsing logic
- [INTERACTION_EXAMPLES.md](INTERACTION_EXAMPLES.md) - Complete voice interaction flows
- [INSTALL_SCRIPT.md](INSTALL_SCRIPT.md) - Full installation script with platform detection

## Constitutional Rules

When implementing this SKILL, follow the project's constitution.yaml:
- Clean code principles: Follow Python best practices
- Test all voice interaction paths

## Next Steps

1. Review supporting documentation files
3. Break into tasks for each module
4. Implement via Claude Code iteratively
5. Test voice commands with various phrasings
6. Package for curl-based installation