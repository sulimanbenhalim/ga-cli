"""Output helper functions for consistent formatting"""

import click
import json
from rich.console import Console

console = Console()


def success_message(message: str, format_type: str = 'text'):
    """Display success message

    Args:
        message: Success message to display
        format_type: Output format ('text' or 'json')
    """
    if format_type == 'json':
        click.echo(json.dumps({"success": True, "message": message}))
    else:
        console.print(f"[green]{message}[/green]")


def error_message(message: str, format_type: str = 'text'):
    """Display error message

    Args:
        message: Error message to display
        format_type: Output format ('text' or 'json')
    """
    if format_type == 'json':
        click.echo(json.dumps({"success": False, "error": message}))
    else:
        console.print(f"[red]{message}[/red]", err=True)


def info_message(message: str, format_type: str = 'text'):
    """Display info message

    Args:
        message: Info message to display
        format_type: Output format ('text' or 'json')
    """
    if format_type == 'json':
        click.echo(json.dumps({"info": message}))
    else:
        console.print(f"[blue]{message}[/blue]")


def warning_message(message: str, format_type: str = 'text'):
    """Display warning message

    Args:
        message: Warning message to display
        format_type: Output format ('text' or 'json')
    """
    if format_type == 'json':
        click.echo(json.dumps({"warning": message}))
    else:
        console.print(f"[yellow]{message}[/yellow]")
