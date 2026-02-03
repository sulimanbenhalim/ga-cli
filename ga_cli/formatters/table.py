"""Table formatter using Rich"""

from rich.console import Console
from rich.table import Table


def format_table(data, title=None):
    """Format list of dicts as a Rich table"""
    console = Console()

    if not data:
        console.print("[yellow]No results found[/yellow]")
        return

    table = Table(show_header=True, header_style="bold magenta", title=title)

    for key in data[0].keys():
        table.add_column(key.replace('_', ' ').title())

    for item in data:
        table.add_row(*[str(v) for v in item.values()])

    console.print(table)
