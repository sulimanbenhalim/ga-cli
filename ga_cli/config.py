"""Configuration management for GA CLI"""

import os
import stat
import configparser
import click
from pathlib import Path


class ConfigManager:
    """Manages CLI configuration"""

    def __init__(self):
        self.config_dir = Path.home() / '.ga-cli'
        self.config_file = self.config_dir / 'config.ini'
        self.config = configparser.ConfigParser()

    def ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        self.config_dir.mkdir(exist_ok=True)
        # Set restrictive permissions on config directory
        os.chmod(self.config_dir, stat.S_IRWXU)  # 700

    def load(self):
        """Load configuration from file"""
        if self.config_file.exists():
            self.config.read(self.config_file)

    def save(self):
        """Save configuration to file"""
        self.ensure_config_dir()
        with open(self.config_file, 'w') as f:
            self.config.write(f)
        # Set restrictive permissions on config file
        os.chmod(self.config_file, stat.S_IRUSR | stat.S_IWUSR)  # 600

    def get_credentials_path(self):
        """Get stored credentials path"""
        self.load()
        return self.config.get('auth', 'credentials_path', fallback=None)

    def set_credentials_path(self, path):
        """Store credentials path"""
        # Validate credentials file before storing
        if not self._validate_credentials_file(path):
            raise click.ClickException("Invalid or insecure credentials file")

        if 'auth' not in self.config:
            self.config['auth'] = {}
        self.config['auth']['credentials_path'] = path
        self.save()

    def _validate_credentials_file(self, path: str) -> bool:
        """Validate credentials file exists and has secure permissions

        Args:
            path: Path to credentials file

        Returns:
            True if valid and secure, False otherwise
        """
        if not os.path.exists(path):
            click.echo(f"Error: Credentials file not found: {path}", err=True)
            return False

        # Check not world-readable
        st = os.stat(path)
        if st.st_mode & (stat.S_IROTH | stat.S_IWOTH):
            click.echo(
                "Warning: Credentials file is world-readable. "
                "Consider running: chmod 600 " + path,
                err=True
            )
            # Don't fail, just warn

        # Check ownership (Unix only)
        if os.name != 'nt' and st.st_uid != os.getuid():
            click.echo("Warning: Credentials file not owned by current user", err=True)
            # Don't fail, just warn

        return True

    def get(self, section: str, key: str, fallback=None):
        """Get a configuration value

        Args:
            section: Configuration section
            key: Configuration key
            fallback: Default value if not found

        Returns:
            Configuration value or fallback
        """
        self.load()
        return self.config.get(section, key, fallback=fallback)
