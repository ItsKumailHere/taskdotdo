# REPL loop for interactive mode
import sys
import shlex
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from .commands import cli
from .ui import console, show_error, show_message
from .voice_input import listen_for_command, listen_continuous
from .command_parser import parse_voice_command, parse_multi_command
from .repository import TodoRepository

# Global flag for voice mode
voice_mode_active = False

def execute_command(cmd_dict):
    """Execute a single parsed command dict. Returns (success, message)."""
    try:
        action = cmd_dict.get("action")

        if action == "delete_all":
            repo = TodoRepository()
            count = repo.delete_all_tasks()
            return (True, f"Deleted {count} task(s)")

        elif action == "delete_completed":
            repo = TodoRepository()
            count = repo.delete_completed_tasks()
            return (True, f"Deleted {count} completed task(s)")

        else:
            # Build Typer args from parsed dict
            args = [action]
            for key, value in cmd_dict.items():
                if key != "action":
                    if key == "id":
                        args.append(str(value))
                    elif key == "description":
                        args.append(value)

            # Execute via Typer
            cli(args, standalone_mode=False)
            return (True, "Command executed successfully")

    except SystemExit:
        return (True, "Command completed")
    except Exception as e:
        return (False, str(e))

def main():
    session = PromptSession(history=InMemoryHistory())
    commands = ["add", "ls", "done", "edit", "rm", "exit", "help", "voice"]
    completer = WordCompleter(commands, ignore_case=True)

    console.print("[bold blue]🎤 Welcome to the Advanced Voice-Enabled Todo CLI![/bold blue]")
    console.print("Type [green]'help'[/green] for commands")
    console.print("Hold [green]'v'[/green] key for continuous voice mode (stops after 5s silence)")
    console.print("Type [green]'voice'[/green] for single voice command")
    console.print("Type [red]'exit'[/red] to quit\n")

    # Key bindings for hold 'v' functionality
    kb = KeyBindings()

    @kb.add('v', eager=True)
    def _(event):
        """Trigger voice mode when 'v' is pressed."""
        # Note: prompt_toolkit doesn't support hold-to-talk natively
        # This triggers on 'v' press. For true hold functionality,
        # would need lower-level keyboard library like pynput
        console.print("\n[cyan]🎤 Voice mode triggered! Speak now...[/cyan]")
        voice_text = listen_continuous(silence_timeout=5)

        if voice_text:
            console.print(f"[blue]📝 Recognized:[/blue] {voice_text}\n")

            # Try multi-command parsing first
            commands_list = parse_multi_command(voice_text)

            if commands_list and len(commands_list) > 1:
                # Multi-command execution
                console.print(f"[yellow]⚡ Executing {len(commands_list)} commands...[/yellow]")
                results = []

                for i, cmd in enumerate(commands_list, 1):
                    success, message = execute_command(cmd)
                    results.append((cmd, success, message))

                    if success:
                        console.print(f"[green]✓ Command {i}/{len(commands_list)}: {message}[/green]")
                    else:
                        console.print(f"[red]✗ Command {i}/{len(commands_list)} failed: {message}[/red]")

                # Summary
                successes = sum(1 for _, s, _ in results if s)
                console.print(f"\n[bold]Summary: {successes}/{len(commands_list)} commands succeeded[/bold]\n")

            elif commands_list and len(commands_list) == 1:
                # Single command
                success, message = execute_command(commands_list[0])
                if success:
                    show_message(message, "green")
                else:
                    show_error(message)
            else:
                # Fallback to single parse
                parsed = parse_voice_command(voice_text)
                if parsed:
                    success, message = execute_command(parsed)
                    if success:
                        show_message(message, "green")
                    else:
                        show_error(message)
                else:
                    show_error(f"Could not parse: '{voice_text}'")
        else:
            console.print("[yellow]⏱️  Voice mode timed out or failed[/yellow]\n")

    while True:
        try:
            user_input = session.prompt("todo> ", completer=completer, key_bindings=kb).strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break

            if user_input.lower() == "voice":
                console.print("[cyan]🎤 Voice mode activated! Speak now...[/cyan]")
                voice_text = listen_continuous(silence_timeout=5)

                if voice_text:
                    console.print(f"[blue]📝 Recognized:[/blue] {voice_text}\n")

                    # Try multi-command parsing
                    commands_list = parse_multi_command(voice_text)

                    if commands_list and len(commands_list) > 1:
                        console.print(f"[yellow]⚡ Executing {len(commands_list)} commands...[/yellow]")
                        results = []

                        for i, cmd in enumerate(commands_list, 1):
                            success, message = execute_command(cmd)
                            results.append((cmd, success, message))

                            if success:
                                console.print(f"[green]✓ Command {i}: {message}[/green]")
                            else:
                                console.print(f"[red]✗ Command {i} failed: {message}[/red]")

                        successes = sum(1 for _, s, _ in results if s)
                        console.print(f"\n[bold]Summary: {successes}/{len(commands_list)} commands succeeded[/bold]\n")

                    elif commands_list and len(commands_list) == 1:
                        success, message = execute_command(commands_list[0])
                        if success:
                            show_message(message, "green")
                        else:
                            show_error(message)
                    else:
                        parsed = parse_voice_command(voice_text)
                        if parsed:
                            success, message = execute_command(parsed)
                            if success:
                                show_message(message, "green")
                            else:
                                show_error(message)
                        else:
                            show_error(f"Could not parse: '{voice_text}'")
                else:
                    show_error("Voice input failed or timed out")
                continue

            # Handle typed commands using Typer
            args = shlex.split(user_input)
            try:
                cli(args, standalone_mode=False)
            except Exception as e:
                if not isinstance(e, SystemExit):
                    show_error(str(e))

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

if __name__ == "__main__":
    main()
