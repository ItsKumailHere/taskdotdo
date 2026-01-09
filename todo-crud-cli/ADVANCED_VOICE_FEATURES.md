# 🚀 Advanced Voice Features Guide

## Overview

The Todo CLI now includes powerful advanced voice features that make voice interaction more natural and efficient:

1. **Hold 'v' Key for Voice Mode** - Press 'v' to activate continuous voice listening
2. **5-Second Silence Timeout** - Automatically stops listening after 5 seconds of silence
3. **Extended Command Synonyms** - Say commands in many different ways
4. **Fuzzy Number Recognition** - "four", "for", "fr" all recognized as 4
5. **Multi-Command Support** - Execute multiple tasks in a single voice command
6. **Batch Operations** - Delete all tasks or only completed tasks

## 🎤 Voice Activation Methods

### Method 1: Hold 'v' Key (New!)
```bash
todo> [Press 'v']
🎤 Voice mode triggered! Speak now...
(Will stop after 5 seconds of silence)
```

### Method 2: Type 'voice'
```bash
todo> voice
🎤 Voice mode activated! Speak now...
```

**Note**: Due to terminal limitations, 'v' triggers on press (not hold). For true hold-to-talk, the implementation could be extended with libraries like `pynput`.

## 🗣️ Extended Command Synonyms

### Delete/Remove Commands
All these words mean "delete":
- **delete**, **remove**, **rm**, **undo**, **destroy**, **erase**, **del**, **trash**, **discard**

```bash
🗣️ "remove task 5"
🗣️ "undo 3"
🗣️ "destroy task 7"
🗣️ "erase 2"
🗣️ "trash task 9"
🗣️ "discard 4"
```

### Complete Commands
All these words mean "mark complete":
- **done**, **complete**, **finish**, **mark**, **tick**, **check**, **accomplish**

```bash
🗣️ "finish task 1"
🗣️ "tick 5"
🗣️ "check task 3"
🗣️ "accomplish 8"
```

### Add Commands
All these words mean "add task":
- **add**, **create**, **new**, **make**, **insert**, **append**

```bash
🗣️ "make task buy groceries"
🗣️ "insert new workout"
🗣️ "append call mom"
```

### Edit Commands
All these words mean "edit task":
- **edit**, **update**, **change**, **modify**, **alter**, **revise**

```bash
🗣️ "modify task 2 to updated text"
🗣️ "alter task 5 to new description"
🗣️ "revise 1 with better text"
```

### List Commands
All these words mean "show tasks":
- **list**, **show**, **display**, **view**, **all**, **see**

```bash
🗣️ "view all tasks"
🗣️ "see my todos"
```

## 🔢 Fuzzy Number Recognition

The app recognizes number words and common voice recognition mistakes:

### Number 4 Variations
- "four" ✅
- "for" ✅
- "fr" ✅
- "fore" ✅

```bash
🗣️ "delete for"        # Deletes task 4
🗣️ "done fr"           # Marks task 4 complete
```

### Number 2 Variations
- "two" ✅
- "to" ✅ (when not used as preposition)
- "too" ✅

```bash
🗣️ "finish too"        # Marks task 2 complete
🗣️ "remove two"        # Deletes task 2
```

### Number 8 Variations
- "eight" ✅
- "ate" ✅

```bash
🗣️ "done ate"          # Marks task 8 complete
```

### All Supported Number Words
- zero (0), one (1), two/to/too (2), three (3), four/for/fr/fore (4)
- five (5), six (6), seven (7), eight/ate (8), nine (9), ten (10)
- eleven (11) through twenty (20)

## ⚡ Multi-Command Support

Execute multiple commands in a single voice input!

### Separators
Use these words to separate commands:
- **and**
- **then**
- **also**
- **plus**

### Examples

#### Two Commands
```bash
🗣️ "add buy milk and delete 5"
✅ Output:
  ⚡ Executing 2 commands...
  ✓ Command 1: Task added successfully
  ✓ Command 2: Task deleted successfully
  Summary: 2/2 commands succeeded
```

#### Three Commands
```bash
🗣️ "add task one and add task two then list"
✅ Executes all three commands sequentially
```

#### Complex Multi-Command
```bash
🗣️ "make homework and finish for then erase completed"
✅ Creates homework task, marks task 4 done, deletes all completed tasks
```

### Error Handling
If some commands fail, the app shows which succeeded and which failed:

```bash
🗣️ "add new task and delete 999"
✅ Output:
  ⚡ Executing 2 commands...
  ✓ Command 1: Task added successfully
  ✗ Command 2 failed: Task not found
  Summary: 1/2 commands succeeded
```

## 🗑️ Batch Operations

### Delete All Tasks
```bash
🗣️ "delete all"
🗣️ "remove all"
🗣️ "erase everything"
🗣️ "destroy all tasks"

✅ Output: "Deleted 5 task(s)"
```

### Delete Completed Tasks Only
```bash
🗣️ "delete completed"
🗣️ "remove finished"
🗣️ "erase done"

✅ Output: "Deleted 3 completed task(s)"
```

## 💡 Usage Tips

### Combine Features
```bash
🗣️ "make task one and finish for then remove completed"
# Creates task, marks task 4 done, deletes all completed
```

### Natural Language
```bash
🗣️ "please add buy groceries and also finish task for"
# Natural phrasing works perfectly!
```

### Context-Aware Number Recognition
```bash
🗣️ "edit task 2 to buy four apples"
# "to" is recognized as preposition (not number 2)
# "four" is kept in description
```

## 🎯 Complete Examples

### Example 1: Morning Routine
```bash
todo> voice
🗣️ "add morning standup and add code review then list"

✅ Output:
  ⚡ Executing 3 commands...
  ✓ Command 1: Task added successfully
  ✓ Command 2: Task added successfully
  ✓ Command 3: Command executed successfully

  [Shows task list]
```

### Example 2: Cleanup
```bash
todo> voice
🗣️ "finish one and finish two then erase completed"

✅ Output:
  ⚡ Executing 3 commands...
  ✓ Command 1: Task marked as completed
  ✓ Command 2: Task marked as completed
  ✓ Command 3: Deleted 2 completed task(s)
```

### Example 3: Using Synonyms
```bash
todo> voice
🗣️ "make homework and tick for then trash ate"

✅ Translates to:
  - add "homework"
  - done 4
  - rm 8
```

## ⏱️ Silence Timeout

Voice mode automatically stops after 5 seconds of silence:

```bash
todo> voice
🎤 Voice mode ACTIVE - Speak now...
(Will stop after 5 seconds of silence)

[5 seconds pass with no speech]

⏱️ Silence detected - voice mode disabled
```

This prevents the microphone from staying active indefinitely.

## 🧪 Testing

All features have comprehensive test coverage:

```bash
# Run advanced voice feature tests
uv run pytest tests/test_advanced_voice.py -v

# Test specific feature
uv run pytest tests/test_advanced_voice.py::TestMultiCommandParsing -v
```

**Test Coverage**: 46 tests covering:
- Number word recognition (5 tests)
- Extended synonyms (18 tests)
- Fuzzy numbers in commands (4 tests)
- Batch operations (7 tests)
- Multi-command parsing (8 tests)
- Advanced edge cases (4 tests)

## 🚨 Troubleshooting

### Voice Mode Not Working
- Check microphone permissions
- Ensure internet connection (uses Google Speech API)
- Try typed commands as fallback

### WSL2 Microphone Issues
- See `WSL2_VOICE_GUIDE.md` for workarounds
- Use file-based audio input
- Or use typed commands

### Multi-Command Not Separating
- Use clear separators: "and", "then", "also"
- Add natural pauses between commands
- Fallback: Execute commands individually

## 📊 Feature Comparison

| Feature | Basic Voice | Advanced Voice |
|---------|-------------|----------------|
| Single commands | ✅ | ✅ |
| Multi-commands | ❌ | ✅ |
| Synonym support | Limited | Extensive |
| Number recognition | Digits only | Fuzzy + words |
| Batch operations | ❌ | ✅ |
| Silence timeout | ❌ | ✅ 5s |
| Hold key activation | ❌ | ✅ 'v' key |

## 🎓 Learn More

- **Basic Usage**: `README.md`
- **Testing Guide**: `TESTING_GUIDE.md`
- **Quick Reference**: `QUICK_REFERENCE.md`
- **WSL2 Setup**: `WSL2_VOICE_GUIDE.md`

---

**Ready to try it?**
```bash
uv run python -m todo_cli
todo> voice
🗣️ "make task one and finish for then remove completed"
```

Enjoy the most advanced voice-controlled todo CLI! 🎉
