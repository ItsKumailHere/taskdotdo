# 🎯 Quick Reference Card - Voice-Enabled Todo CLI

## 🚀 Getting Started

```bash
# Install & run
sudo apt-get install portaudio19-dev  # One-time setup
uv sync                                # Install dependencies
uv run python -m todo_cli              # Start the app
```

## ⌨️ Typed Commands Cheat Sheet

| Command | Syntax | Example |
|---------|--------|---------|
| **Add** | `add "description"` | `add "Buy milk"` |
| **List All** | `ls` | `ls` |
| **List Filtered** | `ls --status Status` | `ls --status Completed` |
| **Complete** | `done <id>` | `done 1` |
| **Edit** | `edit <id> "new text"` | `edit 1 "Buy organic milk"` |
| **Delete** | `rm <id>` | `rm 1` |
| **Voice Mode** | `voice` | `voice` |
| **Help** | `help` | `help` |
| **Exit** | `exit` or `quit` | `exit` |

## 🎤 Voice Commands Cheat Sheet

### How to Use Voice
1. Type `voice` and press Enter
2. Wait for "Listening (speak now)..."
3. Speak your command clearly
4. Wait for recognition and execution

### Voice Patterns

#### ➕ Adding Tasks
```
✅ "add buy milk"
✅ "create task record demo"
✅ "new task review code"
✅ "please add finish report"
```

#### 📋 Listing Tasks
```
✅ "list"
✅ "show all tasks"
✅ "display tasks"
✅ "show me all"
```

#### ✔️ Completing Tasks
```
✅ "done 1"
✅ "mark task 2 complete"
✅ "complete task number 5"
✅ "mark task as complete, id is 3"
```

#### ✏️ Editing Tasks
```
✅ "edit 1 to buy chocolate"
✅ "update task 3 to new description"
✅ "change id 2 with finish homework"
```

#### ❌ Deleting Tasks
```
✅ "delete 1"
✅ "remove task 4"
✅ "delete task id 7"
```

#### ❓ Getting Help
```
✅ "help"
```

## 🎯 Common Workflows

### Workflow 1: Quick Task Management
```bash
todo> add "Morning standup meeting"
todo> add "Code review PR #123"
todo> add "Update documentation"
todo> ls
todo> done 1
todo> exit
```

### Workflow 2: Voice-First Approach
```bash
todo> voice
🗣️ "add prepare presentation"

todo> voice
🗣️ "add send email to team"

todo> voice
🗣️ "list"

todo> voice
🗣️ "mark task 1 complete"

todo> exit
```

### Workflow 3: Hybrid Mode
```bash
todo> voice
🗣️ "add three tasks"

todo> add "Task via typing"
todo> ls
todo> voice
🗣️ "done 1"

todo> edit 2 "Updated via typing"
todo> exit
```

## 💡 Pro Tips

### Voice Tips
- ✅ **Speak clearly** - Enunciate your words
- ✅ **Be specific** - Include task IDs for edit/delete/complete
- ✅ **Natural language** - "please add" works fine
- ✅ **Wait for prompt** - Let "Listening..." appear first
- ✅ **Internet required** - Uses Google Speech API

### Efficiency Tips
- 🚀 **Use shortcuts** - `ls` is faster than `list`
- 🚀 **Tab completion** - Tab key completes commands
- 🚀 **Ctrl+C** - Cancel current input (doesn't exit)
- 🚀 **Ctrl+D or EOF** - Quick exit
- 🚀 **Mix modes** - Use voice for adds, type for edits

### Persistence Tips
- 💾 Tasks save automatically to `~/.todo-app/tasks.json`
- 💾 Backup: `cp ~/.todo-app/tasks.json ~/backup.json`
- 💾 Restore: `cp ~/backup.json ~/.todo-app/tasks.json`
- 💾 View raw data: `cat ~/.todo-app/tasks.json`

## ⚠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| **No microphone** | Use typed commands or file-based voice |
| **Voice not recognized** | Check internet, speak louder/clearer |
| **PortAudio error** | `sudo apt-get install portaudio19-dev` |
| **Task not saved** | Check `~/.todo-app/` directory exists |
| **WSL2 mic issues** | See `WSL2_VOICE_GUIDE.md` |

## 🎬 Demo Script (For Presentations)

```bash
# 1. Start the app
uv run python -m todo_cli

# 2. Show help
todo> help

# 3. Add tasks via voice
todo> voice
🗣️ "add prepare demo slides"

todo> voice
🗣️ "add practice presentation"

todo> voice
🗣️ "add test all features"

# 4. List tasks
todo> ls

# 5. Complete a task via voice
todo> voice
🗣️ "mark task 1 complete"

# 6. Edit via typing
todo> edit 2 "Master the presentation"

# 7. Show final list
todo> ls

# 8. Exit
todo> exit
```

## 📊 Task Status Values

- **Pending** - New/incomplete task (yellow)
- **Completed** - Finished task (green)

## 🔗 More Information

- Full guide: `README.md`
- Testing: `TESTING_GUIDE.md`
- WSL2 setup: `WSL2_VOICE_GUIDE.md`
- In-app help: Type `help` in the CLI

---

**Quick Start One-Liner:**
```bash
sudo apt-get install -y portaudio19-dev && uv sync && uv run python -m todo_cli
```

💡 **Remember**: Type `help` anytime for in-app guidance!
