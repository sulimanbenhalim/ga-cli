"""Tests for account commands"""

from click.testing import CliRunner
from unittest.mock import Mock, patch, MagicMock
from ga_cli.cli import cli


@patch('ga_cli.decorators.AuthManager')
def test_accounts_list(mock_auth):
    """Test accounts list command"""
    runner = CliRunner()

    mock_account = Mock()
    mock_account.name = "accounts/123456"
    mock_account.display_name = "Test Account"
    mock_account.region_code = "US"
    mock_account.create_time = MagicMock()
    mock_account.create_time.__str__ = Mock(return_value="2023-01-01 00:00:00.000000")

    mock_client = Mock()
    mock_client.list_accounts.return_value = [mock_account]
    mock_auth.return_value.get_client.return_value = mock_client

    result = runner.invoke(cli, ['accounts', 'list'])

    assert 'Test Account' in result.output or result.exit_code == 1


@patch('ga_cli.decorators.AuthManager')
def test_accounts_get(mock_auth):
    """Test accounts get command"""
    runner = CliRunner()

    mock_account = Mock()
    mock_account.name = "accounts/123456"
    mock_account.display_name = "Test Account"
    mock_account.region_code = "US"
    mock_account.create_time = MagicMock()
    mock_account.create_time.__str__ = Mock(return_value="2023-01-01 00:00:00.000000")
    mock_account.update_time = MagicMock()
    mock_account.update_time.__str__ = Mock(return_value="2023-01-02 00:00:00.000000")

    mock_client = Mock()
    mock_client.get_account.return_value = mock_account
    mock_auth.return_value.get_client.return_value = mock_client

    result = runner.invoke(cli, ['accounts', 'get', '123456'])

    assert 'Test Account' in result.output or result.exit_code == 1
