# 🎯 Voice-Enabled Todo CLI

A powerful command-line todo application that supports both **typed commands** and **voice input**! Manage your tasks naturally using speech or keyboard - your choice!

## ✨ Features

- 🎤 **Voice Commands** - Speak naturally to manage tasks
- ⌨️ **Typed Commands** - Traditional CLI interface
- 💾 **Persistent Storage** - Tasks saved to `~/.todo-app/tasks.json`
- 🎨 **Rich UI** - Beautiful terminal interface with colors and tables
- 🔄 **CRUD Operations** - Create, Read, Update, Delete tasks
- 🌐 **No LLM Required** - Pure regex-based voice parsing
- 🔁 **Hybrid Mode** - Mix voice and typed commands seamlessly

## 🚀 Quick Start

### Installation

```bash
# Install system dependencies (Linux/WSL)
sudo apt-get update && sudo apt-get install -y portaudio19-dev

# Clone and navigate to project
cd todo-crud-cli

# Sync dependencies
uv sync

# Run the app
uv run python -m todo_cli
```

### First Commands

```bash
# Start the app
uv run python -m todo_cli

# Try these commands:
> add "Buy milk"
> add "Record demo video"
> ls
> done 1
> edit 2 "Create amazing demo"
> rm 2
> help
> exit
```

## 📝 Usage Guide

### Typed Commands

```bash
todo> add "Buy groceries"          # Add a new task
todo> ls                            # List all tasks
todo> ls --status Completed         # Filter by status
todo> done 1                        # Mark task 1 as complete
todo> edit 1 "Buy organic milk"     # Update task description
todo> rm 1                          # Delete task
todo> help                          # Show help
todo> exit                          # Quit
```

### 🎤 Voice Commands

Type `voice` to activate your microphone, then speak naturally:

#### Adding Tasks
```
🗣️ "add buy milk"
🗣️ "create task record the demo video"
🗣️ "new task review pull requests"
🗣️ "please add prepare slides for presentation"
```

#### Listing Tasks
```
🗣️ "list"
🗣️ "show all tasks"
🗣️ "display my todos"
```

#### Completing Tasks
```
🗣️ "done 1"
🗣️ "mark task 2 complete"
🗣️ "complete task number 5"
🗣️ "mark task as complete, id is 3"
```

#### Editing Tasks
```
🗣️ "edit 1 to buy chocolate milk"
🗣️ "update task 3 to finish documentation"
🗣️ "change id 2 with review the code"
```

#### Deleting Tasks
```
🗣️ "delete 1"
🗣️ "remove task 4"
🗣️ "delete task id 7"
```

## 🎬 Demo Workflow

```bash
# Start the app
uv run python -m todo_cli

# Add tasks using voice
todo> voice
Listening (speak now)...
🗣️ "add prepare hackathon demo"
✅ Task added successfully

todo> voice
🗣️ "add record presentation video"
✅ Task added successfully

# List tasks
todo> ls
┌────┬──────────┬─────────────────────────┐
│ ID │  Status  │      Description        │
├────┼──────────┼─────────────────────────┤
│  2 │ Pending  │ record presentation...  │
│  1 │ Pending  │ prepare hackathon demo  │
└────┴──────────┴─────────────────────────┘

# Mark task complete using voice
todo> voice
🗣️ "mark task 1 complete"
✅ Task marked as completed

# Edit using typed command
todo> edit 2 "Create awesome demo video"
✅ Task updated successfully

# Exit
todo> exit
Goodbye!
```

## ⚙️ Requirements

### System Requirements
- **Python**: 3.12+
- **Package Manager**: `uv`
- **OS**: Linux, macOS, Windows (WSL2)
- **Audio**: Microphone access (for voice mode)

### Python Dependencies
- `typer` - CLI framework
- `prompt-toolkit` - Interactive REPL
- `pydantic` - Data validation
- `rich` - Terminal UI
- `SpeechRecognition` - Voice recognition
- `pyaudio` - Audio input
- `pyyaml` - Configuration

All dependencies are automatically installed via `uv sync`.

## 🛠️ WSL2 Setup

WSL2 doesn't have native microphone access. Here are your options:

### Option 1: Use Typed Commands (Recommended)
All features work perfectly with typed commands - no voice needed!

### Option 2: File-Based Voice Input
1. Record audio on Windows (using Voice Recorder app)
2. Save as WAV format to Desktop
3. Run with file:
```bash
VOICE_INPUT_FILE="/mnt/c/Users/YOUR_USERNAME/Desktop/voice.wav" uv run python -m todo_cli
```
4. Type `voice` to process the audio file

### Option 3: PulseAudio Bridge (Advanced)
See `WSL2_VOICE_GUIDE.md` for detailed setup instructions.

## 📊 Project Structure

```
todo-crud-cli/
├── src/todo_cli/
│   ├── __init__.py           # Package init
│   ├── __main__.py           # Entry point
│   ├── app.py                # REPL loop with voice integration
│   ├── commands.py           # Typer command routing
│   ├── models.py             # Pydantic data models
│   ├── repository.py         # Data persistence layer
│   ├── storage.py            # JSON file operations
│   ├── ui.py                 # Rich terminal UI
│   ├── voice_input.py        # Speech recognition
│   └── command_parser.py     # Voice command parsing
├── tests/
│   ├── test_voice_parser.py  # Voice parser tests (47 tests)
│   ├── test_flow.py          # Integration tests
│   └── test_repository.py    # Unit tests
├── pyproject.toml            # Project config
├── README.md                 # This file
├── TESTING_GUIDE.md          # Test documentation
└── WSL2_VOICE_GUIDE.md       # WSL2 voice setup
```

## 🧪 Testing

### Run All Tests
```bash
uv run pytest tests/ -v
```

### Run Voice Parser Tests
```bash
uv run pytest tests/test_voice_parser.py -v
```

**Test Coverage**: 47 voice parser tests - all passing ✅

See `TESTING_GUIDE.md` for detailed testing documentation.

## 🎯 Voice Command Parsing

The app uses **pure regex pattern matching** - no AI/LLM required!

### Supported Patterns

| Command | Patterns | Example |
|---------|----------|---------|
| Add | add, create, new | "add buy milk" |
| List | list, show, display, all | "show all tasks" |
| Complete | done, mark, complete | "mark task 2 complete" |
| Edit | edit, update, change | "edit 1 to new text" |
| Delete | delete, remove, rm | "delete task 3" |
| Help | help | "help" |

### Natural Language Support
- ✅ Case insensitive
- ✅ Polite language ("please add...")
- ✅ Flexible word order
- ✅ Multiple keyword variations
- ✅ Conversational phrasings

## 💾 Data Persistence

Tasks are automatically saved to:
```
~/.todo-app/tasks.json
```

### Verify Persistence
```bash
# Add a task
uv run python -m todo_cli
> add "test persistence"
> exit

# Restart - task is still there!
uv run python -m todo_cli
> ls
```

## 🤝 Contributing

Contributions welcome! Please ensure:
- All tests pass: `uv run pytest tests/ -v`
- Voice parser handles new patterns
- Update documentation for new features

## 📄 License

MIT License - see LICENSE file for details.

## 🙋 Support

### Get Help
```bash
# In the app
todo> help

# View documentation
cat TESTING_GUIDE.md
cat WSL2_VOICE_GUIDE.md
```

### Common Issues

**"No microphone access"**
- WSL2 limitation - use typed commands or file-based voice
- See `WSL2_VOICE_GUIDE.md`

**"Voice recognition fails"**
- Check internet connection (uses Google Speech API)
- Speak clearly and wait for "Listening..." prompt
- Try typed commands as fallback

**"PortAudio not found"**
- Install system dependencies: `sudo apt-get install portaudio19-dev`
- Run `uv sync` again

## 🎉 Features Roadmap

- [x] Voice command support
- [x] JSON persistence
- [x] Rich terminal UI
- [x] Comprehensive tests
- [ ] Task priorities
- [ ] Due dates
- [ ] Tags/categories
- [ ] Search functionality
- [ ] Export to CSV/JSON

## 👏 Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [SpeechRecognition](https://github.com/Uberi/speech_recognition) - Voice input
- [Pydantic](https://docs.pydantic.dev/) - Data validation

---

Made with ❤️ for the Hackathon II - Voice-Enabled Todo CLI Challenge
