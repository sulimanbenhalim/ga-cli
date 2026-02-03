"""JSON formatter"""

import json
import click


def format_json(data):
    """Format data as JSON"""
    click.echo(json.dumps(data, indent=2))
