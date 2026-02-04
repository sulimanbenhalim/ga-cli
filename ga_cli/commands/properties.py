"""Property management commands"""

import builtins
import click
from google.analytics.admin_v1alpha.types import Property
from ga_cli.decorators import with_client
from ga_cli.formatters.table import format_table
from ga_cli.formatters.json import format_json
from ga_cli.validators import validate_account_id, validate_property_id, validate_timezone, validate_currency
from ga_cli.logging_config import logger
from ga_cli.retry import retry_on_transient_error


@click.group()
def properties():
    """Manage Google Analytics properties"""
    pass


@properties.command()
@click.argument('account_id', callback=validate_account_id)
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
@with_client
def list(ctx, account_id, format):
    """List properties for an account"""
    client = ctx.obj['client']
    logger.info(f"Listing properties for account: {account_id}")

    properties_data = []
    request = {"filter": f"ancestor:accounts/{account_id}"}
    for property in _list_properties_with_retry(client, request):
        properties_data.append({
            'id': property.name.split('/')[-1] if '/' in property.name else property.name,
            'name': property.display_name or 'N/A',
            'type': property.property_type.name if property.property_type else 'N/A',
            'timezone': property.time_zone or 'N/A',
            'currency': property.currency_code or 'N/A',
        })

    logger.info(f"Found {len(properties_data)} properties")

    if format == 'json':
        format_json(properties_data)
    else:
        format_table(properties_data, title=f"Properties for Account {account_id}")


@properties.command()
@click.argument('property_id', callback=validate_property_id)
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
@with_client
def get(ctx, property_id, format):
    """Get property details"""
    client = ctx.obj['client']
    logger.info(f"Getting property details for: {property_id}")

    property = _get_property_with_retry(client, property_id)

    property_data = {
        'id': property.name.split('/')[-1] if '/' in property.name else property.name,
        'name': property.display_name or 'N/A',
        'type': property.property_type.name if property.property_type else 'N/A',
        'timezone': property.time_zone or 'N/A',
        'currency': property.currency_code or 'N/A',
        'industry': property.industry_category.name if property.industry_category else 'N/A',
        'create_time': str(property.create_time).split('.')[0] if property.create_time else 'N/A',
    }

    logger.info(f"Retrieved property: {property.display_name}")

    if format == 'json':
        format_json(property_data)
    else:
        format_table([property_data], title=f"Property: {property.display_name}")


@properties.command()
@click.argument('account_id', callback=validate_account_id)
@click.option('--name', required=True, help='Display name for the property')
@click.option('--timezone', default='America/Los_Angeles', callback=validate_timezone,
              help='Property timezone')
@click.option('--currency', default='USD', callback=validate_currency,
              help='Property currency code (e.g., USD, EUR)')
@click.option('--industry', default='OTHER', help='Industry category')
@click.pass_context
@with_client
def create(ctx, account_id, name, timezone, currency, industry):
    """Create a new GA4 property"""
    client = ctx.obj['client']
    logger.info(f"Creating property '{name}' for account: {account_id}")

    property = _create_property_with_retry(
        client, account_id, name, timezone, currency, industry
    )

    property_id = property.name.split('/')[-1] if '/' in property.name else property.name
    logger.info(f"Created property: {property_id}")

    click.echo(f"Created property: {property.display_name}")
    click.echo(f"  Property ID: {property_id}")
    click.echo(f"  Timezone: {property.time_zone}")
    click.echo(f"  Currency: {property.currency_code}")


@properties.command()
@click.argument('property_id', callback=validate_property_id)
@click.confirmation_option(prompt='Are you sure you want to delete this property?')
@click.pass_context
@with_client
def delete(ctx, property_id):
    """Delete a property"""
    client = ctx.obj['client']
    logger.info(f"Deleting property: {property_id}")

    _delete_property_with_retry(client, property_id)

    logger.info(f"Deleted property: {property_id}")
    click.echo(f"Property {property_id} deleted successfully")


@retry_on_transient_error()
def _list_properties_with_retry(client, request):
    """List properties with retry logic"""
    return builtins.list(client.list_properties(request=request))


@retry_on_transient_error()
def _get_property_with_retry(client, property_id):
    """Get property with retry logic"""
    return client.get_property(name=f"properties/{property_id}")


@retry_on_transient_error()
def _create_property_with_retry(client, account_id, name, timezone, currency, industry):
    """Create property with retry logic"""
    return client.create_property(
        property=Property(
            parent=f"accounts/{account_id}",
            display_name=name,
            time_zone=timezone,
            currency_code=currency,
            industry_category=industry,
        )
    )


@retry_on_transient_error()
def _delete_property_with_retry(client, property_id):
    """Delete property with retry logic"""
    return client.delete_property(name=f"properties/{property_id}")
