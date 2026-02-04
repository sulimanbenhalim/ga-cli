"""Data stream management commands"""

import builtins
import click
from google.analytics.admin_v1alpha.types import DataStream
from ga_cli.decorators import with_client
from ga_cli.formatters.table import format_table
from ga_cli.formatters.json import format_json
from ga_cli.validators import validate_property_id, validate_stream_id, validate_url
from ga_cli.logging_config import logger
from ga_cli.retry import retry_on_transient_error


@click.group()
def datastreams():
    """Manage data streams"""
    pass


@datastreams.command()
@click.argument('property_id', callback=validate_property_id)
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
@with_client
def list(ctx, property_id, format):
    """List data streams for a property"""
    client = ctx.obj['client']
    logger.info(f"Listing data streams for property: {property_id}")

    streams_data = []
    for stream in _list_datastreams_with_retry(client, property_id):
        stream_info = {
            'id': stream.name.split('/')[-1] if '/' in stream.name else stream.name,
            'name': stream.display_name or 'N/A',
            'type': stream.type_.name if stream.type_ else 'N/A',
        }

        # Add stream-type specific data with null checks
        if stream.web_stream_data:
            stream_info['measurement_id'] = stream.web_stream_data.measurement_id or 'N/A'
            stream_info['url'] = stream.web_stream_data.default_uri or 'N/A'
        elif stream.android_app_stream_data:
            stream_info['package_name'] = stream.android_app_stream_data.package_name or 'N/A'
        elif stream.ios_app_stream_data:
            stream_info['bundle_id'] = stream.ios_app_stream_data.bundle_id or 'N/A'

        streams_data.append(stream_info)

    logger.info(f"Found {len(streams_data)} data streams")

    if format == 'json':
        format_json(streams_data)
    else:
        format_table(streams_data, title=f"Data Streams for Property {property_id}")


@datastreams.command()
@click.argument('property_id', callback=validate_property_id)
@click.argument('stream_id', callback=validate_stream_id)
@click.option('--format', type=click.Choice(['table', 'json']), default='table')
@click.pass_context
@with_client
def get(ctx, property_id, stream_id, format):
    """Get data stream details including measurement ID"""
    client = ctx.obj['client']
    logger.info(f"Getting data stream {stream_id} for property: {property_id}")

    stream = _get_datastream_with_retry(client, property_id, stream_id)

    stream_data = {
        'id': stream.name.split('/')[-1] if '/' in stream.name else stream.name,
        'name': stream.display_name or 'N/A',
        'type': stream.type_.name if stream.type_ else 'N/A',
        'create_time': str(stream.create_time).split('.')[0] if stream.create_time else 'N/A',
    }

    # Add web stream specific data with null checks
    if stream.web_stream_data:
        stream_data['measurement_id'] = stream.web_stream_data.measurement_id or 'N/A'
        stream_data['url'] = stream.web_stream_data.default_uri or 'N/A'
        stream_data['firebase_app_id'] = stream.web_stream_data.firebase_app_id or 'N/A'

    logger.info(f"Retrieved data stream: {stream.display_name}")

    if format == 'json':
        format_json(stream_data)
    else:
        format_table([stream_data], title=f"Data Stream: {stream.display_name}")

        if stream.web_stream_data and stream.web_stream_data.measurement_id:
            click.echo(f"\nMeasurement ID: {stream.web_stream_data.measurement_id}")


@datastreams.command()
@click.argument('property_id', callback=validate_property_id)
@click.option('--name', required=True, help='Display name for the data stream')
@click.option('--url', required=True, callback=validate_url, help='Website URL')
@click.pass_context
@with_client
def create(ctx, property_id, name, url):
    """Create a new web data stream"""
    client = ctx.obj['client']
    logger.info(f"Creating data stream '{name}' for property: {property_id}")

    stream = _create_datastream_with_retry(client, property_id, name, url)

    stream_id = stream.name.split('/')[-1] if '/' in stream.name else stream.name
    logger.info(f"Created data stream: {stream_id}")

    click.echo(f"Created data stream: {stream.display_name}")
    click.echo(f"  Stream ID: {stream_id}")
    if stream.web_stream_data:
        if stream.web_stream_data.measurement_id:
            click.echo(f"  Measurement ID: {stream.web_stream_data.measurement_id}")
        if stream.web_stream_data.default_uri:
            click.echo(f"  URL: {stream.web_stream_data.default_uri}")


@retry_on_transient_error()
def _list_datastreams_with_retry(client, property_id):
    """List data streams with retry logic"""
    return builtins.list(client.list_data_streams(parent=f"properties/{property_id}"))


@retry_on_transient_error()
def _get_datastream_with_retry(client, property_id, stream_id):
    """Get data stream with retry logic"""
    return client.get_data_stream(name=f"properties/{property_id}/dataStreams/{stream_id}")


@retry_on_transient_error()
def _create_datastream_with_retry(client, property_id, name, url):
    """Create data stream with retry logic"""
    data_stream = DataStream(
        display_name=name,
        type_=DataStream.DataStreamType.WEB_DATA_STREAM,
    )

    # Safely initialize web_stream_data if not exists
    if data_stream.web_stream_data is None:
        data_stream.web_stream_data = DataStream.WebStreamData()
    data_stream.web_stream_data.default_uri = url

    return client.create_data_stream(
        parent=f"properties/{property_id}",
        data_stream=data_stream
    )
