"""Main CLI entry point"""

import click
from ga_cli import __version__
from ga_cli.commands.accounts import accounts
from ga_cli.commands.properties import properties
from ga_cli.commands.datastreams import datastreams
from ga_cli.commands.config import config
from ga_cli.config import ConfigManager


@click.group()
@click.version_option(version=__version__)
@click.option('--credentials', envvar='GOOGLE_APPLICATION_CREDENTIALS',
              help='Path to service account credentials file')
@click.pass_context
def cli(ctx, credentials):
    """Google Analytics CLI - Manage GA4 from the command line"""
    ctx.ensure_object(dict)

    if not credentials:
        config_manager = ConfigManager()
        credentials = config_manager.get_credentials_path()

    ctx.obj['credentials'] = credentials


cli.add_command(accounts)
cli.add_command(properties)
cli.add_command(datastreams)
cli.add_command(config)


if __name__ == '__main__':
    cli()
