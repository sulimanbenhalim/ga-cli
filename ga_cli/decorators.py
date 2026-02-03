"""Common decorators for CLI commands"""

import functools
import click
from ga_cli.auth import AuthManager
from ga_cli.logging_config import logger
from ga_cli.errors import get_friendly_error
from google.api_core import exceptions


def with_client(func):
    """Decorator to provide authenticated API client

    This decorator:
    - Retrieves credentials from context or config
    - Creates an authenticated API client
    - Handles common API exceptions with user-friendly messages
    - Adds logging for all operations
    - Injects client into context for use by command

    Usage:
        @accounts.command()
        @click.pass_context
        @with_client
        def list(ctx):
            client = ctx.obj['client']
            # ... rest of logic
    """
    @functools.wraps(func)
    def wrapper(ctx, *args, **kwargs):
        try:
            # Get credentials path
            credentials_path = ctx.obj.get('credentials')
            if not credentials_path:
                from ga_cli.config import ConfigManager
                config_manager = ConfigManager()
                credentials_path = config_manager.get('credentials', 'path')

            if not credentials_path:
                logger.error("No credentials configured")
                raise click.ClickException(
                    "No credentials configured. Run 'ga-cli config init' first."
                )

            logger.debug(f"Using credentials: {credentials_path}")

            # Create authenticated client
            auth = AuthManager(credentials_path)
            client = auth.get_client()

            # Add client to context
            ctx.obj['client'] = client

            # Call the actual command
            logger.info(f"Executing command: {func.__name__}")
            return func(ctx, *args, **kwargs)

        except exceptions.NotFound as e:
            logger.error(f"Resource not found: {str(e)}")
            click.echo(get_friendly_error(e), err=True)
            raise click.Abort()
        except exceptions.PermissionDenied as e:
            logger.error(f"Permission denied: {str(e)}")
            click.echo(get_friendly_error(e), err=True)
            raise click.Abort()
        except exceptions.Unauthenticated as e:
            logger.error(f"Authentication failed: {str(e)}")
            click.echo(get_friendly_error(e), err=True)
            raise click.Abort()
        except exceptions.InvalidArgument as e:
            logger.error(f"Invalid argument: {str(e)}")
            click.echo(get_friendly_error(e), err=True)
            raise click.Abort()
        except exceptions.ResourceExhausted as e:
            logger.error(f"Rate limit exceeded: {str(e)}")
            click.echo(get_friendly_error(e), err=True)
            raise click.Abort()
        except exceptions.GoogleAPIError as e:
            logger.error(f"Google API error: {str(e)}")
            click.echo(get_friendly_error(e), err=True)
            raise click.Abort()
        except click.ClickException:
            # Re-raise Click exceptions as-is
            raise
        except Exception as e:
            logger.exception("Unexpected error")
            click.echo(f"Error: {str(e)}", err=True)
            raise click.Abort()

    return wrapper
