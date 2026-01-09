# Implementation Specifications

Detailed technical specifications for implementing each module of the voice-enabled todo CLI.

## Module 1: Voice Input (voice_input.py)

### Requirements
- Capture voice input using SpeechRecognition library
- Convert speech to text using Google Speech API
- Handle microphone errors gracefully
- Implement timeout for voice capture
- Provide fallback to typed input

### Implementation

```python
"""
Voice input module for speech-to-text conversion.
"""

import speech_recognition as sr
from typing import Optional, Tuple

class VoiceInput:
    def __init__(self, timeout: int = 3, phrase_time_limit: int = 5):
        """
        Initialize voice input handler.
        
        Args:
            timeout: Seconds to wait for speech to start
            phrase_time_limit: Maximum seconds for a phrase
        """
        self.recognizer = sr.Recognizer()
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        self.microphone = None
        
    def initialize_microphone(self) -> bool:
        """
        Initialize microphone. Returns True if successful.
        """
        try:
            self.microphone = sr.Microphone()
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            return True
        except Exception as e:
            print(f"⚠ Microphone initialization failed: {e}")
            return False
    
    def listen(self) -> Tuple[Optional[str], Optional[str]]:
        """
        Listen for voice input and convert to text.
        
        Returns:
            Tuple of (text, error_message)
            - If successful: (text, None)
            - If failed: (None, error_message)
        """
        if not self.microphone:
            if not self.initialize_microphone():
                return None, "No microphone available"
        
        print("🎤 Listening...")
        
        try:
            with self.microphone as source:
                audio = self.recognizer.listen(
                    source,
                    timeout=self.timeout,
                    phrase_time_limit=self.phrase_time_limit
                )
            
            print("⏳ Processing...")
            
            # Use Google Speech Recognition
            text = self.recognizer.recognize_google(audio)
            return text, None
            
        except sr.WaitTimeoutError:
            return None, "No speech detected (timeout)"
        except sr.UnknownValueError:
            return None, "Could not understand audio"
        except sr.RequestError as e:
            return None, f"API error: {e}"
        except Exception as e:
            return None, f"Unexpected error: {e}"
    
    def get_input(self, allow_typed: bool = True) -> Optional[str]:
        """
        Get input from voice or typed fallback.
        
        Args:
            allow_typed: Allow fallback to typed input if voice fails
            
        Returns:
            Input text or None
        """
        text, error = self.listen()
        
        if text:
            print(f"📝 Captured: \"{text}\"")
            return text
        
        # Handle error
        if error:
            print(f"❌ Voice input failed: {error}")
        
        # Fallback to typed input
        if allow_typed:
            print("⌨️  Please type your command:")
            typed = input("> ").strip()
            return typed if typed else None
        
        return None
```

### Testing

```python
def test_voice_input():
    """Test voice input module."""
    vi = VoiceInput()
    
    # Test microphone initialization
    assert vi.initialize_microphone() is True
    
    # Test listening (requires user to speak)
    print("Say 'add test task'")
    text = vi.get_input()
    assert text is not None
    assert "add" in text.lower()
```

## Module 2: Command Parser (command_parser.py)

### Requirements
- Parse voice/text input for command keywords
- Extract task names, IDs, and actions
- No LLM or AI - pure regex/string matching
- Return structured command objects
- Handle ambiguous input with clarification

### Implementation

```python
"""
Command parser for extracting actions and parameters from text.
"""

import re
from typing import Optional, Dict, Any
from dataclasses import dataclass

@dataclass
class Command:
    """Structured command representation."""
    action: str  # add, delete, mark_complete, mark_incomplete, list, update
    task_id: Optional[int] = None
    task_name: Optional[str] = None
    new_name: Optional[str] = None
    needs_clarification: Optional[str] = None
    raw_text: str = ""

class CommandParser:
    """Parse text commands using regex and keyword matching."""
    
    # Command keyword patterns
    ADD_KEYWORDS = ['add', 'create', 'new', 'make']
    DELETE_KEYWORDS = ['delete', 'remove', 'erase']
    COMPLETE_KEYWORDS = ['complete', 'done', 'finish', 'finished']
    INCOMPLETE_KEYWORDS = ['incomplete', 'uncomplete', 'undo', 'unmark']
    MARK_KEYWORDS = ['mark']
    LIST_KEYWORDS = ['list', 'show', 'display', 'view', 'see']
    UPDATE_KEYWORDS = ['update', 'edit', 'change', 'modify']
    
    # Filler words to remove
    FILLER_PATTERNS = [
        r'\bas\s+a\s+todo\b',
        r'\bas\s+a\s+task\b',
        r'\bplease\b',
        r'\bfor\s+me\b',
        r'\bthe\s+task\b',
    ]
    
    def parse(self, text: str) -> Command:
        """
        Parse text and return structured command.
        
        Args:
            text: User input text
            
        Returns:
            Command object with parsed information
        """
        if not text or not text.strip():
            return Command(
                action='unknown',
                raw_text=text,
                needs_clarification='command'
            )
        
        text_clean = text.strip()
        text_lower = text_clean.lower()
        
        # Try each command parser in order
        parsers = [
            self._parse_add,
            self._parse_mark,
            self._parse_delete,
            self._parse_update,
            self._parse_list,
        ]
        
        for parser in parsers:
            cmd = parser(text_clean, text_lower)
            if cmd:
                cmd.raw_text = text_clean
                return cmd
        
        # No pattern matched
        return Command(
            action='unknown',
            raw_text=text_clean,
            needs_clarification='command'
        )
    
    def _parse_add(self, text: str, text_lower: str) -> Optional[Command]:
        """Parse add task command."""
        # Check for add keywords
        keyword_pos = None
        for keyword in self.ADD_KEYWORDS:
            pattern = r'\b' + keyword + r'\b'
            match = re.search(pattern, text_lower)
            if match:
                keyword_pos = match.end()
                break
        
        if keyword_pos is None:
            return None
        
        # Extract task name after keyword
        task_text = text[keyword_pos:].strip()
        
        # Remove filler phrases
        for pattern in self.FILLER_PATTERNS:
            task_text = re.sub(pattern, '', task_text, flags=re.IGNORECASE)
        
        task_text = task_text.strip()
        
        if not task_text:
            return Command(
                action='add',
                needs_clarification='task_name'
            )
        
        return Command(action='add', task_name=task_text)
    
    def _parse_delete(self, text: str, text_lower: str) -> Optional[Command]:
        """Parse delete task command."""
        # Check for delete keywords
        has_delete = any(kw in text_lower for kw in self.DELETE_KEYWORDS)
        if not has_delete:
            return None
        
        # Extract ID
        task_id = self._extract_id(text_lower)
        
        if task_id is None:
            return Command(
                action='delete',
                needs_clarification='task_id'
            )
        
        return Command(action='delete', task_id=task_id)
    
    def _parse_mark(self, text: str, text_lower: str) -> Optional[Command]:
        """Parse mark complete/incomplete command."""
        # Check for mark keywords or complete/incomplete keywords
        has_mark = any(kw in text_lower for kw in self.MARK_KEYWORDS)
        is_complete = any(kw in text_lower for kw in self.COMPLETE_KEYWORDS)
        is_incomplete = any(kw in text_lower for kw in self.INCOMPLETE_KEYWORDS)
        
        if not (has_mark or is_complete or is_incomplete):
            return None
        
        # Determine action
        action = 'mark_complete' if is_complete else 'mark_incomplete'
        
        # Extract ID
        task_id = self._extract_id(text_lower)
        
        if task_id is None:
            return Command(
                action=action,
                needs_clarification='task_id'
            )
        
        return Command(action=action, task_id=task_id)
    
    def _parse_list(self, text: str, text_lower: str) -> Optional[Command]:
        """Parse list tasks command."""
        has_list = any(kw in text_lower for kw in self.LIST_KEYWORDS)
        
        # Also check for context words
        context_words = ['all', 'tasks', 'todos', 'items']
        has_context = any(word in text_lower for word in context_words)
        
        if has_list or (has_context and len(text_lower.split()) <= 3):
            return Command(action='list')
        
        return None
    
    def _parse_update(self, text: str, text_lower: str) -> Optional[Command]:
        """Parse update task command."""
        has_update = any(kw in text_lower for kw in self.UPDATE_KEYWORDS)
        if not has_update:
            return None
        
        # Extract ID
        task_id = self._extract_id(text_lower)
        
        # Try to extract new name if "to" keyword present
        new_name = None
        to_pattern = r'\bto\s+(.+)$'
        to_match = re.search(to_pattern, text_lower)
        if to_match:
            new_name = to_match.group(1).strip()
        
        if task_id is None:
            return Command(
                action='update',
                new_name=new_name,
                needs_clarification='task_id'
            )
        
        return Command(action='update', task_id=task_id, new_name=new_name)
    
    def _extract_id(self, text_lower: str) -> Optional[int]:
        """Extract task ID from text."""
        # Try multiple patterns
        id_patterns = [
            r'id\s+(\d+)',           # "id 2"
            r'task\s+(\d+)',         # "task 2"
            r'number\s+(\d+)',       # "number 2"
            r'\bid\s+is\s+(\d+)',    # "id is 2"
            r'\b(\d+)\b',            # standalone number (last resort)
        ]
        
        for pattern in id_patterns:
            match = re.search(pattern, text_lower)
            if match:
                try:
                    return int(match.group(1))
                except (ValueError, IndexError):
                    continue
        
        return None
    
    def get_clarification_prompt(self, needs: str) -> str:
        """Get clarification prompt based on what's needed."""
        prompts = {
            'task_id': "Please provide the task ID.\nSay 'id' followed by the number (e.g., 'id 2')",
            'task_name': "Please provide the task name.\nSay 'add' followed by the task description",
            'command': (
                "I didn't understand that command.\n"
                "Try: 'add [task]', 'list', 'delete id [number]', "
                "or 'mark complete id [number]'"
            )
        }
        return prompts.get(needs, "Please clarify your command")
```

### Testing

```python
def test_command_parser():
    """Test command parser."""
    parser = CommandParser()
    
    # Test add command
    cmd = parser.parse("add do boxing")
    assert cmd.action == 'add'
    assert cmd.task_name == 'do boxing'
    
    # Test with filler words
    cmd = parser.parse("please add do boxing as a todo")
    assert cmd.action == 'add'
    assert cmd.task_name == 'do boxing'
    
    # Test delete with ID
    cmd = parser.parse("delete id 2")
    assert cmd.action == 'delete'
    assert cmd.task_id == 2
    
    # Test mark complete
    cmd = parser.parse("mark complete id 3")
    assert cmd.action == 'mark_complete'
    assert cmd.task_id == 3
    
    # Test list
    cmd = parser.parse("show all tasks")
    assert cmd.action == 'list'
    
    # Test ambiguous command
    cmd = parser.parse("delete task")
    assert cmd.action == 'delete'
    assert cmd.needs_clarification == 'task_id'
```

## Module 3: Storage (storage.py)

### Requirements
- Store tasks in JSON format
- Location: `~/.todo-app/tasks.json`
- Atomic file writes
- Auto-create directory
- Handle file corruption
- Thread-safe operations

### Implementation

```python
"""
Persistent storage for tasks using JSON.
"""

import json
import os
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import shutil
from threading import Lock

class TaskStorage:
    """Manage task storage in JSON file."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize storage.
        
        Args:
            data_dir: Custom data directory (defaults to ~/.todo-app)
        """
        if data_dir is None:
            self.data_dir = Path.home() / '.todo-app'
        else:
            self.data_dir = Path(data_dir)
        
        self.tasks_file = self.data_dir / 'tasks.json'
        self.backup_file = self.data_dir / 'tasks.json.backup'
        self.lock = Lock()
        
        # Create directory if needed
        self._ensure_data_dir()
        
        # Initialize with empty tasks if file doesn't exist
        if not self.tasks_file.exists():
            self._write_tasks({'tasks': []})
    
    def _ensure_data_dir(self):
        """Create data directory if it doesn't exist."""
        self.data_dir.mkdir(parents=True, exist_ok=True)
    
    def _read_tasks(self) -> Dict:
        """Read tasks from JSON file with error recovery."""
        try:
            with open(self.tasks_file, 'r') as f:
                data = json.load(f)
                
            # Validate structure
            if 'tasks' not in data:
                raise ValueError("Invalid tasks file structure")
                
            return data
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"⚠ Error reading tasks: {e}")
            
            # Try to restore from backup
            if self.backup_file.exists():
                print("Restoring from backup...")
                try:
                    shutil.copy(self.backup_file, self.tasks_file)
                    with open(self.tasks_file, 'r') as f:
                        return json.load(f)
                except Exception:
                    pass
            
            # Create new file
            print("Creating new tasks file...")
            return {'tasks': []}
    
    def _write_tasks(self, data: Dict):
        """Write tasks to JSON file atomically."""
        # Write to temporary file first
        temp_file = self.tasks_file.with_suffix('.tmp')
        
        with open(temp_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Backup current file
        if self.tasks_file.exists():
            shutil.copy(self.tasks_file, self.backup_file)
        
        # Atomic replace
        temp_file.replace(self.tasks_file)
    
    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks."""
        with self.lock:
            data = self._read_tasks()
            return data['tasks']
    
    def get_task(self, task_id: int) -> Optional[Dict]:
        """Get task by ID."""
        tasks = self.get_all_tasks()
        for task in tasks:
            if task['id'] == task_id:
                return task
        return None
    
    def add_task(self, title: str, description: str = "") -> Dict:
        """Add new task."""
        with self.lock:
            data = self._read_tasks()
            tasks = data['tasks']
            
            # Generate new ID
            if tasks:
                new_id = max(task['id'] for task in tasks) + 1
            else:
                new_id = 1
            
            # Create task
            task = {
                'id': new_id,
                'title': title,
                'description': description,
                'completed': False,
                'created_at': datetime.now().isoformat()
            }
            
            tasks.append(task)
            self._write_tasks(data)
            
            return task
    
    def update_task(self, task_id: int, **kwargs) -> bool:
        """Update task fields."""
        with self.lock:
            data = self._read_tasks()
            tasks = data['tasks']
            
            for task in tasks:
                if task['id'] == task_id:
                    # Update fields
                    for key, value in kwargs.items():
                        if key in task:
                            task[key] = value
                    
                    self._write_tasks(data)
                    return True
            
            return False
    
    def delete_task(self, task_id: int) -> bool:
        """Delete task by ID."""
        with self.lock:
            data = self._read_tasks()
            tasks = data['tasks']
            
            # Find and remove task
            for i, task in enumerate(tasks):
                if task['id'] == task_id:
                    tasks.pop(i)
                    self._write_tasks(data)
                    return True
            
            return False
    
    def mark_complete(self, task_id: int, completed: bool = True) -> bool:
        """Mark task as complete/incomplete."""
        return self.update_task(task_id, completed=completed)
```

### Testing

```python
def test_storage():
    """Test storage module."""
    import tempfile
    
    # Use temporary directory
    with tempfile.TemporaryDirectory() as tmpdir:
        storage = TaskStorage(Path(tmpdir))
        
        # Test add task
        task = storage.add_task("Test task", "Description")
        assert task['id'] == 1
        assert task['title'] == "Test task"
        
        # Test get task
        retrieved = storage.get_task(1)
        assert retrieved is not None
        assert retrieved['title'] == "Test task"
        
        # Test update task
        success = storage.update_task(1, title="Updated")
        assert success is True
        
        updated = storage.get_task(1)
        assert updated['title'] == "Updated"
        
        # Test mark complete
        success = storage.mark_complete(1, True)
        assert success is True
        
        completed = storage.get_task(1)
        assert completed['completed'] is True
        
        # Test delete
        success = storage.delete_task(1)
        assert success is True
        
        deleted = storage.get_task(1)
        assert deleted is None
```

## Integration Testing

Test all modules together:

```python
def test_integration():
    """Test complete voice command flow."""
    voice = VoiceInput()
    parser = CommandParser()
    storage = TaskStorage()
    
    # Simulate voice input
    text = "add test task"
    
    # Parse command
    cmd = parser.parse(text)
    assert cmd.action == 'add'
    
    # Execute command
    if cmd.action == 'add':
        task = storage.add_task(cmd.task_name)
        assert task['id'] > 0
```