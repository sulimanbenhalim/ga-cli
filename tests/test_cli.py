"""Tests for CLI entry point"""

from click.testing import CliRunner
from ga_cli.cli import cli


def test_cli_help():
    """Test that CLI help works"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'Google Analytics CLI' in result.output


def test_cli_version():
    """Test that version flag works"""
    runner = CliRunner()
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0
    assert '0.1.0' in result.output


def test_accounts_command_exists():
    """Test that accounts command exists"""
    runner = CliRunner()
    result = runner.invoke(cli, ['accounts', '--help'])
    assert result.exit_code == 0
    assert 'Manage Google Analytics accounts' in result.output


def test_properties_command_exists():
    """Test that properties command exists"""
    runner = CliRunner()
    result = runner.invoke(cli, ['properties', '--help'])
    assert result.exit_code == 0
    assert 'Manage Google Analytics properties' in result.output


def test_datastreams_command_exists():
    """Test that datastreams command exists"""
    runner = CliRunner()
    result = runner.invoke(cli, ['datastreams', '--help'])
    assert result.exit_code == 0
    assert 'Manage data streams' in result.output


def test_config_command_exists():
    """Test that config command exists"""
    runner = CliRunner()
    result = runner.invoke(cli, ['config', '--help'])
    assert result.exit_code == 0
    assert 'Manage CLI configuration' in result.output
