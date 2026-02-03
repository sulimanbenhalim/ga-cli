"""Account management commands"""

import click
from ga_cli.decorators import with_client
from ga_cli.formatters.table import format_table
from ga_cli.formatters.json import format_json
from ga_cli.validators import validate_account_id
from ga_cli.logging_config import logger
from ga_cli.retry import retry_on_transient_error


@click.group()
def accounts():
    """Manage Google Analytics accounts"""
    pass


@accounts.command()
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
@with_client
def list(ctx, format):
    """List all accounts"""
    client = ctx.obj['client']
    logger.info("Listing Google Analytics accounts")

    accounts_data = []
    for account in _list_accounts_with_retry(client):
        accounts_data.append({
            'id': account.name.split('/')[-1] if '/' in account.name else account.name,
            'name': account.display_name or 'N/A',
            'region': account.region_code or 'N/A',
            'create_time': str(account.create_time).split('.')[0] if account.create_time else 'N/A',
        })

    logger.info(f"Found {len(accounts_data)} accounts")

    if format == 'json':
        format_json(accounts_data)
    else:
        format_table(accounts_data, title="Google Analytics Accounts")


@accounts.command()
@click.argument('account_id', callback=validate_account_id)
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
@with_client
def get(ctx, account_id, format):
    """Get account details"""
    client = ctx.obj['client']
    logger.info(f"Getting account details for: {account_id}")

    account = _get_account_with_retry(client, account_id)

    account_data = {
        'id': account.name.split('/')[-1] if '/' in account.name else account.name,
        'name': account.display_name or 'N/A',
        'region': account.region_code or 'N/A',
        'create_time': str(account.create_time).split('.')[0] if account.create_time else 'N/A',
        'update_time': str(account.update_time).split('.')[0] if account.update_time else 'N/A',
    }

    logger.info(f"Retrieved account: {account.display_name}")

    if format == 'json':
        format_json(account_data)
    else:
        format_table([account_data], title=f"Account: {account.display_name}")


@retry_on_transient_error()
def _list_accounts_with_retry(client):
    """List accounts with retry logic"""
    return list(client.list_accounts())


@retry_on_transient_error()
def _get_account_with_retry(client, account_id):
    """Get account with retry logic"""
    return client.get_account(name=f"accounts/{account_id}")
