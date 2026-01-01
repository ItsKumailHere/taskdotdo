# REPL loop for interactive mode
import sys
import shlex
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.completion import WordCompleter
from .commands import cli
from .ui import console, show_error

def main():
    session = PromptSession(history=InMemoryHistory())
    commands = ["add", "ls", "done", "edit", "rm", "exit", "help"]
    completer = WordCompleter(commands, ignore_case=True)

    console.print("[bold blue]Welcome to the Todo CRUD CLI![/bold blue]")
    console.print("Type [green]'help'[/green] for commands or [red]'exit'[/red] to quit.")

    while True:
        try:
            user_input = session.prompt("todo> ", completer=completer).strip()

            if not user_input:
                continue

            if user_input.lower() in ["exit", "quit"]:
                console.print("[yellow]Goodbye![/yellow]")
                break

            # Handle commands using Typer
            args = shlex.split(user_input)
            try:
                cli(args, standalone_mode=False)
            except Exception as e:
                # Typer can raise SystemExit or other errors if usage is wrong
                if not isinstance(e, SystemExit):
                    show_error(str(e))

        except KeyboardInterrupt:
            continue
        except EOFError:
            break

if __name__ == "__main__":
    main()
