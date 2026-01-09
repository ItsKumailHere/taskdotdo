# WSL2 Voice Input Guide

## Problem
WSL2 does not have native microphone access, which causes these errors:
```
Cannot connect to server socket err = No such file or directory
jack server is not running or cannot be started
No Default Input Device Available
```

## Solutions

### Option 1: File-Based Audio Input (Easiest)
Record audio on Windows and pass it to the app:

1. **Record audio on Windows** using Voice Recorder or any tool (save as WAV format)
2. **Save to an accessible location**, e.g., `C:\Users\DELL\Desktop\voice_command.wav`
3. **Run the app with the file**:
   ```bash
   VOICE_INPUT_FILE="/mnt/c/Users/DELL/Desktop/voice_command.wav" uv run python -m todo_cli
   ```
4. **Type `voice`** in the REPL to process the audio file

**Example**:
```bash
# Record "add buy milk" and save as voice_command.wav on Windows Desktop
VOICE_INPUT_FILE="/mnt/c/Users/DELL/Desktop/voice_command.wav" uv run python -m todo_cli
> voice  # This will process the audio file
```

### Option 2: Use PulseAudio Bridge (Advanced)
Set up PulseAudio to bridge Windows audio to WSL2:

1. **Install PulseAudio on Windows**: Download from [PulseAudio Windows](https://www.freedesktop.org/wiki/Software/PulseAudio/Ports/Windows/Support/)
2. **Configure WSL2 to use Windows PulseAudio**:
   ```bash
   echo "export PULSE_SERVER=tcp:$(grep nameserver /etc/resolv.conf | awk '{print $2}')" >> ~/.bashrc
   source ~/.bashrc
   ```
3. **Install PulseAudio in WSL2**:
   ```bash
   sudo apt-get install -y pulseaudio
   ```

### Option 3: Use Native Linux (No WSL2)
Run the app on native Linux (Ubuntu, Fedora, etc.) or a Linux VM where microphone access works natively.

### Option 4: Type Commands Directly (No Voice)
The app fully supports typed commands without voice:
```bash
uv run python -m todo_cli
> add buy milk
> ls
> done 1
> exit
```

## Testing Without Voice

You can test all features without voice mode:

```bash
# Start the app
uv run python -m todo_cli

# Add tasks
> add buy milk
> add record video
> add review code

# List tasks
> ls

# Mark task as done
> done 1

# Edit task
> edit 2 make tutorial video

# Delete task
> rm 3

# Exit
> exit
```

## Persistence Verification

Tasks are saved to `~/.todo-app/tasks.json`. You can verify persistence:

```bash
# Add a task
uv run python -m todo_cli
> add test persistence
> exit

# Restart and check if task is still there
uv run python -m todo_cli
> ls
```

## Recommended Approach for WSL2

Since WSL2 microphone setup is complex, we recommend:
1. **Use typed commands** for daily usage (no voice needed)
2. **Use file-based audio** for occasional voice input demos
3. **Deploy to native Linux** if voice is a critical feature
