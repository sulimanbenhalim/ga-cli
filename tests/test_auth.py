"""Tests for authentication module"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from ga_cli.auth import AuthManager


class TestAuthManager:
    """Test AuthManager class"""

    def test_init_with_credentials_path(self):
        """Test initialization with credentials path"""
        auth = AuthManager(credentials_path="/path/to/creds.json")
        assert auth.credentials_path == "/path/to/creds.json"

    def test_init_without_credentials_uses_env(self, monkeypatch):
        """Test initialization falls back to environment variable"""
        monkeypatch.setenv("GOOGLE_APPLICATION_CREDENTIALS", "/env/creds.json")
        auth = AuthManager()
        assert auth.credentials_path == "/env/creds.json"

    @patch('ga_cli.auth.service_account')
    @patch('ga_cli.auth.AnalyticsAdminServiceClient')
    def test_get_client_with_credentials(self, mock_client_class, mock_service_account):
        """Test get_client creates client with credentials"""
        mock_credentials = Mock()
        mock_service_account.Credentials.from_service_account_file.return_value = mock_credentials

        auth = AuthManager(credentials_path="/path/to/creds.json")
        client = auth.get_client()

        mock_service_account.Credentials.from_service_account_file.assert_called_once_with(
            "/path/to/creds.json"
        )
        mock_client_class.assert_called_once()
        assert client is not None

    @patch('ga_cli.auth.AnalyticsAdminServiceClient')
    def test_get_client_caches_instance(self, mock_client_class):
        """Test get_client returns cached client instance"""
        auth = AuthManager()
        client1 = auth.get_client()
        client2 = auth.get_client()

        # Should only create client once
        assert mock_client_class.call_count == 1
        assert client1 is client2

    @patch('ga_cli.auth.service_account')
    @patch('ga_cli.auth.AnalyticsAdminServiceClient')
    def test_context_manager(self, mock_client_class, mock_service_account):
        """Test AuthManager as context manager"""
        mock_credentials = Mock()
        mock_service_account.Credentials.from_service_account_file.return_value = mock_credentials

        auth = AuthManager(credentials_path="/path/to/creds.json")

        with auth as client:
            assert client is not None

        # After exit, client should be cleared
        assert auth._client is None

    @patch('ga_cli.auth.service_account')
    @patch('ga_cli.auth.AnalyticsAdminServiceClient')
    def test_get_client_with_timeout(self, mock_client_class, mock_service_account):
        """Test get_client accepts timeout parameter"""
        mock_credentials = Mock()
        mock_service_account.Credentials.from_service_account_file.return_value = mock_credentials

        auth = AuthManager(credentials_path="/path/to/creds.json")
        client = auth.get_client(timeout=60)

        assert client is not None
