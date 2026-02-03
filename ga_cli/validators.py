"""Input validation helpers for CLI commands"""

import re
import click


def validate_account_id(ctx, param, value):
    """Validate account ID format"""
    if value and not value.isdigit():
        raise click.BadParameter("Account ID must be numeric")
    return value


def validate_property_id(ctx, param, value):
    """Validate property ID format"""
    if value and not value.isdigit():
        raise click.BadParameter("Property ID must be numeric")
    return value


def validate_url(ctx, param, value):
    """Validate URL format"""
    if value:
        pattern = re.compile(r'^https?://.+')
        if not pattern.match(value):
            raise click.BadParameter("URL must start with http:// or https://")
    return value


def validate_timezone(ctx, param, value):
    """Validate timezone"""
    if value:
        try:
            import pytz
            pytz.timezone(value)
        except pytz.exceptions.UnknownTimeZoneError:
            raise click.BadParameter(f"Invalid timezone: {value}")
    return value


def validate_currency(ctx, param, value):
    """Validate currency code"""
    if value and not re.match(r'^[A-Z]{3}$', value):
        raise click.BadParameter("Currency must be 3-letter code (e.g., USD)")
    return value


def validate_stream_id(ctx, param, value):
    """Validate stream ID format"""
    if value and not value.isdigit():
        raise click.BadParameter("Stream ID must be numeric")
    return value
