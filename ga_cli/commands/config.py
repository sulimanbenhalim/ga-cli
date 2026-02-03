"""Configuration commands"""

import click
import os
from ga_cli.config import ConfigManager
from ga_cli.auth import AuthManager


@click.group()
def config():
    """Manage CLI configuration"""
    pass


@config.command()
@click.option('--credentials', prompt='Path to service account JSON',
              help='Path to Google service account credentials file')
def init(credentials):
    """Initialize GA CLI with credentials"""
    try:
        credentials_path = os.path.expanduser(credentials)

        if not os.path.exists(credentials_path):
            click.echo(f"Error: Credentials file not found at {credentials_path}", err=True)
            raise click.Abort()

        click.echo("Testing credentials...")
        auth = AuthManager(credentials_path)
        client = auth.get_client()

        accounts = list(client.list_accounts())

        if accounts:
            click.echo(f"Credentials valid! Found {len(accounts)} account(s)")

            config_manager = ConfigManager()
            config_manager.set_credentials_path(credentials_path)

            click.echo(f"Configuration saved to {config_manager.config_file}")
            click.echo("\nYou can now use ga-cli commands without specifying credentials")
        else:
            click.echo("Warning: Credentials are valid but no accounts found", err=True)

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@config.command()
def show():
    """Show current configuration"""
    try:
        config_manager = ConfigManager()
        credentials_path = config_manager.get_credentials_path()

        if credentials_path:
            click.echo("Configuration:")
            click.echo(f"  Credentials: {credentials_path}")
            click.echo(f"  Config file: {config_manager.config_file}")
        else:
            click.echo("No configuration found. Run 'ga-cli config init' to set up.")

    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()
