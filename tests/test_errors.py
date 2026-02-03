"""Tests for error handling module"""

import pytest
from unittest.mock import Mock
from google.api_core import exceptions
from ga_cli.errors import get_friendly_error, ERROR_MESSAGES


class TestGetFriendlyError:
    """Test get_friendly_error function"""

    def test_not_found_exception(self):
        """Test friendly message for NotFound exception"""
        exc = exceptions.NotFound("Resource not found")
        message = get_friendly_error(exc)
        assert message == ERROR_MESSAGES['not_found']
        assert "not found" in message.lower()

    def test_permission_denied_exception(self):
        """Test friendly message for PermissionDenied exception"""
        exc = exceptions.PermissionDenied("Permission denied")
        message = get_friendly_error(exc)
        assert message == ERROR_MESSAGES['permission_denied']
        assert "permission" in message.lower()

    def test_invalid_argument_exception(self):
        """Test friendly message for InvalidArgument exception"""
        exc = exceptions.InvalidArgument("Invalid argument")
        message = get_friendly_error(exc)
        assert message == ERROR_MESSAGES['invalid_argument']
        assert "invalid" in message.lower()

    def test_unauthenticated_exception(self):
        """Test friendly message for Unauthenticated exception"""
        exc = exceptions.Unauthenticated("Authentication failed")
        message = get_friendly_error(exc)
        assert message == ERROR_MESSAGES['unauthenticated']
        assert "authentication" in message.lower()

    def test_resource_exhausted_exception(self):
        """Test friendly message for ResourceExhausted exception"""
        exc = exceptions.ResourceExhausted("Rate limit exceeded")
        message = get_friendly_error(exc)
        assert message == ERROR_MESSAGES['resource_exhausted']
        assert "rate limit" in message.lower()

    def test_internal_server_error_exception(self):
        """Test friendly message for InternalServerError exception"""
        exc = exceptions.InternalServerError("Internal server error")
        message = get_friendly_error(exc)
        assert message == ERROR_MESSAGES['internal']
        assert "internal" in message.lower() or "server" in message.lower()

    def test_service_unavailable_exception(self):
        """Test friendly message for ServiceUnavailable exception"""
        exc = exceptions.ServiceUnavailable("Service unavailable")
        message = get_friendly_error(exc)
        assert message == ERROR_MESSAGES['unavailable']
        assert "unavailable" in message.lower()

    def test_deadline_exceeded_exception(self):
        """Test friendly message for DeadlineExceeded exception"""
        exc = exceptions.DeadlineExceeded("Deadline exceeded")
        message = get_friendly_error(exc)
        assert message == ERROR_MESSAGES['deadline_exceeded']
        assert "timeout" in message.lower() or "deadline" in message.lower()

    def test_unknown_exception(self):
        """Test handling of unknown exception types"""
        exc = Exception("Unknown error")
        message = get_friendly_error(exc)
        assert "An error occurred" in message
        assert "Unknown error" in message
