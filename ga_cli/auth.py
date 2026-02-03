"""Authentication manager for Google Analytics Admin API"""

from google.analytics.admin import AnalyticsAdminServiceClient
from google.oauth2 import service_account
import os


class AuthManager:
    """Manages authentication for Google Analytics Admin API

    This class supports context manager protocol for proper resource cleanup.

    Usage:
        # Standard usage
        auth = AuthManager(credentials_path)
        client = auth.get_client()

        # With context manager
        with AuthManager(credentials_path) as client:
            # Use client
            pass
    """

    def __init__(self, credentials_path=None):
        self.credentials_path = credentials_path or os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
        self._client = None

    def __enter__(self):
        """Context manager entry"""
        return self.get_client()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit - clean up client resources"""
        if self._client:
            # Close client connection
            self._client = None
        return False

    def get_client(self, timeout=30):
        """Get authenticated Analytics Admin API client

        Args:
            timeout: Request timeout in seconds (default: 30)

        Returns:
            AnalyticsAdminServiceClient: Authenticated client instance
        """
        if self._client is None:
            if self.credentials_path:
                credentials = service_account.Credentials.from_service_account_file(
                    self.credentials_path
                )
                self._client = AnalyticsAdminServiceClient(
                    credentials=credentials,
                    client_options={'api_endpoint': 'analyticsadmin.googleapis.com'}
                )
            else:
                self._client = AnalyticsAdminServiceClient()
        return self._client
