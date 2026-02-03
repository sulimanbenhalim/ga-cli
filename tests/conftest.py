"""Pytest fixtures and configuration"""

import pytest
from unittest.mock import Mock, MagicMock
from click.testing import CliRunner


@pytest.fixture
def cli_runner():
    """Provide a Click CLI test runner"""
    return CliRunner()


@pytest.fixture
def mock_client():
    """Mock Analytics Admin API client"""
    client = Mock()
    return client


@pytest.fixture
def mock_account():
    """Mock account object"""
    account = Mock()
    account.name = "accounts/123456"
    account.display_name = "Test Account"
    account.region_code = "US"
    account.create_time = MagicMock()
    account.create_time.__str__ = Mock(return_value="2023-01-01 00:00:00.000000")
    account.update_time = MagicMock()
    account.update_time.__str__ = Mock(return_value="2023-01-02 00:00:00.000000")
    return account


@pytest.fixture
def mock_property():
    """Mock property object"""
    property = Mock()
    property.name = "properties/987654"
    property.display_name = "Test Property"
    property.time_zone = "America/Los_Angeles"
    property.currency_code = "USD"
    property.property_type = Mock()
    property.property_type.name = "PROPERTY_TYPE_ORDINARY"
    property.industry_category = Mock()
    property.industry_category.name = "TECHNOLOGY"
    property.create_time = MagicMock()
    property.create_time.__str__ = Mock(return_value="2023-01-01 00:00:00.000000")
    return property


@pytest.fixture
def mock_datastream():
    """Mock data stream object"""
    stream = Mock()
    stream.name = "properties/987654/dataStreams/123"
    stream.display_name = "Test Stream"
    stream.type_ = Mock()
    stream.type_.name = "WEB_DATA_STREAM"
    stream.create_time = MagicMock()
    stream.create_time.__str__ = Mock(return_value="2023-01-01 00:00:00.000000")

    # Mock web stream data
    stream.web_stream_data = Mock()
    stream.web_stream_data.measurement_id = "G-XXXXXXXXXX"
    stream.web_stream_data.default_uri = "https://example.com"
    stream.web_stream_data.firebase_app_id = "1:123456:web:abc"

    stream.android_app_stream_data = None
    stream.ios_app_stream_data = None

    return stream


@pytest.fixture
def mock_credentials_path(tmp_path):
    """Create a temporary credentials file"""
    creds_file = tmp_path / "credentials.json"
    creds_file.write_text('{"type": "service_account"}')
    return str(creds_file)


@pytest.fixture
def mock_config_manager(mocker, mock_credentials_path):
    """Mock ConfigManager"""
    manager = Mock()
    manager.get_credentials_path.return_value = mock_credentials_path
    manager.get.return_value = mock_credentials_path
    return manager
