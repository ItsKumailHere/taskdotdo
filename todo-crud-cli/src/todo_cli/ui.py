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
[bold]Available Commands:[/bold]

[green]add[/green] "description"     - Add a new task
[green]ls[/green] [status]          - List tasks (optional: --status Completed/Pending)
[green]done[/green] [id]            - Mark a task as completed
[green]edit[/green] [id] "desc"     - Update task description
[green]rm[/green] [id]              - Delete a task
[green]help[/green]                 - Show this help message
[green]exit[/green]                 - Exit the application

Examples:
  add "Buy groceries"
  ls
  ls --status Completed
  done 1
  edit 1 "Updated description"
  rm 1
  help
""", title="Todo CLI Help"))
