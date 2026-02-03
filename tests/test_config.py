"""Tests for configuration module"""

import pytest
import os
import stat
from pathlib import Path
from unittest.mock import Mock, patch
import tempfile
import click
from ga_cli.config import ConfigManager


class TestConfigManager:
    """Test ConfigManager class"""

    def test_init_creates_paths(self):
        """Test initialization creates config paths"""
        manager = ConfigManager()
        assert manager.config_dir == Path.home() / '.ga-cli'
        assert manager.config_file == manager.config_dir / 'config.ini'

    def test_ensure_config_dir_creates_directory(self):
        """Test ensure_config_dir creates directory"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ConfigManager()
            manager.config_dir = Path(tmpdir) / '.ga-cli'
            manager.config_file = manager.config_dir / 'config.ini'

            manager.ensure_config_dir()

            assert manager.config_dir.exists()
            # Check directory permissions are restrictive (700)
            assert oct(os.stat(manager.config_dir).st_mode)[-3:] == '700'

    def test_save_creates_secure_file(self):
        """Test save creates config file with secure permissions"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ConfigManager()
            manager.config_dir = Path(tmpdir)
            manager.config_file = manager.config_dir / 'config.ini'

            manager.config['test'] = {'key': 'value'}
            manager.save()

            assert manager.config_file.exists()
            # Check file permissions are restrictive (600)
            assert oct(os.stat(manager.config_file).st_mode)[-3:] == '600'

    def test_load_reads_existing_config(self):
        """Test load reads existing configuration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ConfigManager()
            manager.config_dir = Path(tmpdir)
            manager.config_file = manager.config_dir / 'config.ini'

            # Create config file
            manager.config['section'] = {'key': 'value'}
            manager.save()

            # Load in new instance
            manager2 = ConfigManager()
            manager2.config_dir = Path(tmpdir)
            manager2.config_file = manager2.config_dir / 'config.ini'
            manager2.load()

            assert manager2.config.get('section', 'key') == 'value'

    def test_get_credentials_path(self):
        """Test get_credentials_path retrieves stored path"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a test credentials file
            creds_file = Path(tmpdir) / 'creds.json'
            creds_file.write_text('{}')

            manager = ConfigManager()
            manager.config_dir = Path(tmpdir)
            manager.config_file = manager.config_dir / 'config.ini'

            manager.config['auth'] = {'credentials_path': str(creds_file)}
            manager.save()

            path = manager.get_credentials_path()
            assert path == str(creds_file)

    def test_get_credentials_path_returns_none_when_missing(self):
        """Test get_credentials_path returns None when not configured"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ConfigManager()
            manager.config_dir = Path(tmpdir)
            manager.config_file = manager.config_dir / 'config.ini'

            path = manager.get_credentials_path()
            assert path is None

    def test_set_credentials_path_validates_file(self):
        """Test set_credentials_path validates file exists"""
        with tempfile.TemporaryDirectory() as tmpdir:
            creds_file = Path(tmpdir) / 'creds.json'
            creds_file.write_text('{}')

            manager = ConfigManager()
            manager.config_dir = Path(tmpdir)
            manager.config_file = manager.config_dir / 'config.ini'

            manager.set_credentials_path(str(creds_file))

            assert manager.config.get('auth', 'credentials_path') == str(creds_file)

    def test_set_credentials_path_rejects_missing_file(self):
        """Test set_credentials_path rejects non-existent file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ConfigManager()
            manager.config_dir = Path(tmpdir)
            manager.config_file = manager.config_dir / 'config.ini'

            with pytest.raises(click.ClickException, match="Invalid or insecure credentials file"):
                manager.set_credentials_path('/nonexistent/creds.json')

    def test_get_method(self):
        """Test generic get method"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ConfigManager()
            manager.config_dir = Path(tmpdir)
            manager.config_file = manager.config_dir / 'config.ini'

            manager.config['section'] = {'key': 'value'}
            manager.save()

            value = manager.get('section', 'key')
            assert value == 'value'

    def test_get_method_with_fallback(self):
        """Test get method returns fallback for missing key"""
        with tempfile.TemporaryDirectory() as tmpdir:
            manager = ConfigManager()
            manager.config_dir = Path(tmpdir)
            manager.config_file = manager.config_dir / 'config.ini'

            value = manager.get('missing', 'key', fallback='default')
            assert value == 'default'
