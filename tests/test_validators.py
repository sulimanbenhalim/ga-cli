"""Tests for input validators"""

import pytest
import click
from ga_cli.validators import (
    validate_account_id,
    validate_property_id,
    validate_url,
    validate_timezone,
    validate_currency,
    validate_stream_id,
)


class TestValidateAccountId:
    """Test account ID validation"""

    def test_valid_account_id(self):
        """Test validation with valid account ID"""
        result = validate_account_id(None, None, "123456")
        assert result == "123456"

    def test_invalid_account_id_non_numeric(self):
        """Test validation rejects non-numeric account ID"""
        with pytest.raises(click.BadParameter, match="Account ID must be numeric"):
            validate_account_id(None, None, "abc123")

    def test_empty_account_id(self):
        """Test validation with empty value"""
        result = validate_account_id(None, None, None)
        assert result is None


class TestValidatePropertyId:
    """Test property ID validation"""

    def test_valid_property_id(self):
        """Test validation with valid property ID"""
        result = validate_property_id(None, None, "987654")
        assert result == "987654"

    def test_invalid_property_id_non_numeric(self):
        """Test validation rejects non-numeric property ID"""
        with pytest.raises(click.BadParameter, match="Property ID must be numeric"):
            validate_property_id(None, None, "prop-123")


class TestValidateUrl:
    """Test URL validation"""

    def test_valid_https_url(self):
        """Test validation with valid HTTPS URL"""
        result = validate_url(None, None, "https://example.com")
        assert result == "https://example.com"

    def test_valid_http_url(self):
        """Test validation with valid HTTP URL"""
        result = validate_url(None, None, "http://example.com")
        assert result == "http://example.com"

    def test_invalid_url_no_protocol(self):
        """Test validation rejects URL without protocol"""
        with pytest.raises(click.BadParameter, match="URL must start with http:// or https://"):
            validate_url(None, None, "example.com")

    def test_invalid_url_wrong_protocol(self):
        """Test validation rejects URL with wrong protocol"""
        with pytest.raises(click.BadParameter, match="URL must start with http:// or https://"):
            validate_url(None, None, "ftp://example.com")

    def test_empty_url(self):
        """Test validation with empty value"""
        result = validate_url(None, None, None)
        assert result is None


class TestValidateTimezone:
    """Test timezone validation"""

    def test_valid_timezone(self):
        """Test validation with valid timezone"""
        result = validate_timezone(None, None, "America/New_York")
        assert result == "America/New_York"

    def test_valid_timezone_utc(self):
        """Test validation with UTC timezone"""
        result = validate_timezone(None, None, "UTC")
        assert result == "UTC"

    def test_invalid_timezone(self):
        """Test validation rejects invalid timezone"""
        with pytest.raises(click.BadParameter, match="Invalid timezone"):
            validate_timezone(None, None, "Invalid/Timezone")

    def test_empty_timezone(self):
        """Test validation with empty value"""
        result = validate_timezone(None, None, None)
        assert result is None


class TestValidateCurrency:
    """Test currency code validation"""

    def test_valid_currency(self):
        """Test validation with valid currency code"""
        result = validate_currency(None, None, "USD")
        assert result == "USD"

    def test_valid_currency_eur(self):
        """Test validation with EUR currency"""
        result = validate_currency(None, None, "EUR")
        assert result == "EUR"

    def test_invalid_currency_too_short(self):
        """Test validation rejects short currency code"""
        with pytest.raises(click.BadParameter, match="Currency must be 3-letter code"):
            validate_currency(None, None, "US")

    def test_invalid_currency_too_long(self):
        """Test validation rejects long currency code"""
        with pytest.raises(click.BadParameter, match="Currency must be 3-letter code"):
            validate_currency(None, None, "USDD")

    def test_invalid_currency_lowercase(self):
        """Test validation rejects lowercase currency"""
        with pytest.raises(click.BadParameter, match="Currency must be 3-letter code"):
            validate_currency(None, None, "usd")

    def test_empty_currency(self):
        """Test validation with empty value"""
        result = validate_currency(None, None, None)
        assert result is None


class TestValidateStreamId:
    """Test stream ID validation"""

    def test_valid_stream_id(self):
        """Test validation with valid stream ID"""
        result = validate_stream_id(None, None, "123")
        assert result == "123"

    def test_invalid_stream_id_non_numeric(self):
        """Test validation rejects non-numeric stream ID"""
        with pytest.raises(click.BadParameter, match="Stream ID must be numeric"):
            validate_stream_id(None, None, "stream-123")
