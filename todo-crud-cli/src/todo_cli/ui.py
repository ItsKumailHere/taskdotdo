# UI helpers for Rich formatting
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from .models import Task
from typing import List

console = Console()

def display_tasks(tasks: List[Task]):
    if not tasks:
        console.print(Panel("[yellow]No tasks found.[/yellow]", expand=False))
        return

    table = Table(title="Todo List", expand=True, show_header=True, header_style="bold magenta")
    table.add_column("ID", justify="right", style="cyan", no_wrap=True)
    table.add_column("Status", style="magenta")
    table.add_column("Description", style="white")

    for task in tasks:
        status_style = "green" if task.status == "Completed" else "yellow"
        status_text = f"[{status_style}]{task.status}[/]"
        description_text = f"[white]{task.description}[/]"
        table.add_row(str(task.id), status_text, description_text)

    console.print(table)

def show_message(text: str, style: str = "green"):
    console.print(Panel(f"[{style}]{text}[/]", expand=False))

def show_error(text: str):
    console.print(Panel(f"[red]❌ Error: {text}[/]", expand=False, border_style="red"))

def show_help():
    """Display help information for all available commands."""
    console.print(Panel("""
[bold cyan]📝 TYPED COMMANDS[/bold cyan]

[green]add[/green] "description"     - Add a new task
[green]ls[/green] [status]          - List tasks (optional: --status Completed/Pending)
[green]done[/green] [id]            - Mark a task as completed
[green]edit[/green] [id] "desc"     - Update task description
[green]rm[/green] [id]              - Delete a task
[green]voice[/green]                - Enter voice command mode
[green]help[/green]                 - Show this help message
[green]exit[/green]                 - Exit the application

[bold yellow]Typed Examples:[/bold yellow]
  add "Buy groceries"
  ls
  ls --status Completed
  done 1
  edit 1 "Buy organic milk"
  rm 1

[bold cyan]🎤 VOICE COMMANDS[/bold cyan]

Type [green]voice[/green] to activate microphone, then speak naturally!

[bold yellow]Voice Examples:[/bold yellow]

[magenta]Adding Tasks:[/magenta]
  🗣️  "add buy milk"
  🗣️  "create task record the demo video"
  🗣️  "new task review pull requests"
  🗣️  "please add prepare slides for presentation"

[magenta]Listing Tasks:[/magenta]
  🗣️  "list"
  🗣️  "show all tasks"
  🗣️  "display my todos"

[magenta]Completing Tasks:[/magenta]
  🗣️  "done 1"
  🗣️  "mark task 2 complete"
  🗣️  "complete task number 5"
  🗣️  "mark task as complete, id is 3"

[magenta]Editing Tasks:[/magenta]
  🗣️  "edit 1 to buy chocolate milk"
  🗣️  "update task 3 to finish documentation"
  🗣️  "change id 2 with review the code"

[magenta]Deleting Tasks:[/magenta]
  🗣️  "delete 1"
  🗣️  "remove task 4"
  🗣️  "delete task id 7"

[magenta]Help:[/magenta]
  🗣️  "help"

[bold red]⚠️  WSL2 Users:[/bold red]
If voice fails (No microphone access), use typed commands or:
  VOICE_INPUT_FILE="/path/to/audio.wav" uv run python -m todo_cli

[bold green]💡 Tips:[/bold green]
• Speak clearly and naturally
• Include task ID for edit/delete/done commands
• Voice commands are case-insensitive
• You can mix voice and typed commands!
""", title="🎯 Todo CLI - Voice & Text Help", border_style="cyan"))
