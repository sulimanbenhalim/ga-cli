"""User-friendly error messages for ga-cli"""

from google.api_core import exceptions


ERROR_MESSAGES = {
    'not_found': 'Resource not found. Please check the ID and try again.',
    'permission_denied': 'Permission denied. Ensure your service account has the required permissions.',
    'invalid_argument': 'Invalid argument provided. Please check your input.',
    'unauthenticated': 'Authentication failed. Run "ga-cli config init" to configure credentials.',
    'resource_exhausted': 'Rate limit exceeded. Please wait a moment and try again.',
    'internal': 'Internal server error. Please try again later.',
    'unavailable': 'Service temporarily unavailable. Please try again later.',
    'deadline_exceeded': 'Request timeout. Please try again.',
}


def get_friendly_error(exception):
    """Map API exceptions to user-friendly messages"""
    error_map = {
        exceptions.NotFound: ERROR_MESSAGES['not_found'],
        exceptions.PermissionDenied: ERROR_MESSAGES['permission_denied'],
        exceptions.InvalidArgument: ERROR_MESSAGES['invalid_argument'],
        exceptions.Unauthenticated: ERROR_MESSAGES['unauthenticated'],
        exceptions.ResourceExhausted: ERROR_MESSAGES['resource_exhausted'],
        exceptions.InternalServerError: ERROR_MESSAGES['internal'],
        exceptions.ServiceUnavailable: ERROR_MESSAGES['unavailable'],
        exceptions.DeadlineExceeded: ERROR_MESSAGES['deadline_exceeded'],
    }

    for exc_type, message in error_map.items():
        if isinstance(exception, exc_type):
            return message

    return f"An error occurred: {str(exception)}"
