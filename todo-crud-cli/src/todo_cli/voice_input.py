import speech_recognition as sr
import sys
import os
from pathlib import Path
import threading
import time

def listen_for_command_from_file(audio_file_path: str):
    """
    Recognizes speech from an audio file (WAV, AIFF, FLAC).
    Returns the recognized text or None if recognition fails.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.AudioFile(audio_file_path) as source:
            print(f"Processing audio file: {audio_file_path}")
            audio = recognizer.record(source)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            return command.lower()
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}", file=sys.stderr)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio", file=sys.stderr)
    except FileNotFoundError:
        print(f"Audio file not found: {audio_file_path}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred processing the audio file: {e}", file=sys.stderr)

    return None

def listen_for_command():
    """
    Listens for a voice command and returns the recognized text.
    Returns None if no command is detected or an error occurs.

    On WSL2 or environments without microphone access, automatically
    falls back to file-based input if VOICE_INPUT_FILE env var is set.
    """
    # Check for file-based input (useful for WSL2)
    voice_file = os.environ.get("VOICE_INPUT_FILE")
    if voice_file:
        return listen_for_command_from_file(voice_file)

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening (speak now)...")

            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                return None

            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            return command.lower()

    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}", file=sys.stderr)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio", file=sys.stderr)
    except OSError as e:
        if "No Default Input Device Available" in str(e):
            print("\n[WSL2 DETECTED] No microphone access in WSL2.", file=sys.stderr)
            print("WORKAROUND: Record audio on Windows and use:", file=sys.stderr)
            print("  VOICE_INPUT_FILE='/mnt/c/path/to/audio.wav' uv run python -m todo_cli", file=sys.stderr)
            print("\nAlternatively, type your command directly instead of using 'voice' mode.\n", file=sys.stderr)
        else:
            print(f"An error occurred with voice input: {e}", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred with voice input: {e}", file=sys.stderr)

    return None

def listen_continuous(silence_timeout=5):
    """
    Listens continuously until silence timeout (default 5 seconds).
    Returns the recognized text or None if timeout/error occurs.
    """
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = silence_timeout  # Silence timeout

    try:
        with sr.Microphone() as source:
            print("🎤 Voice mode ACTIVE - Speak now...")
            print(f"(Will stop after {silence_timeout} seconds of silence)")

            # Adjust for ambient noise quickly
            recognizer.adjust_for_ambient_noise(source, duration=0.3)

            try:
                # Listen with phrase time limit but allow silence detection
                audio = recognizer.listen(source, timeout=None, phrase_time_limit=30)
                print("🔄 Recognizing...")
                command = recognizer.recognize_google(audio)
                return command.lower()

            except sr.WaitTimeoutError:
                print("⏱️  Silence detected - voice mode disabled")
                return None

    except sr.RequestError as e:
        print(f"❌ Could not request results from Google Speech Recognition service; {e}", file=sys.stderr)
    except sr.UnknownValueError:
        print("❌ Could not understand audio", file=sys.stderr)
    except OSError as e:
        if "No Default Input Device Available" in str(e):
            print("\n⚠️  [WSL2 DETECTED] No microphone access.", file=sys.stderr)
            print("Use typed commands or set VOICE_INPUT_FILE environment variable.\n", file=sys.stderr)
        else:
            print(f"❌ An error occurred: {e}", file=sys.stderr)
    except Exception as e:
        print(f"❌ An error occurred: {e}", file=sys.stderr)

    return None
