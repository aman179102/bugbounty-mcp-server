"""
Tests for the CLI interface.
"""

import pytest
from unittest.mock import patch, MagicMock
from click.testing import CliRunner
from bugbounty_mcp_server.cli import cli


class TestCLI:
    """Tests for the CLI interface."""

    def test_cli_help(self):
        """Test that CLI shows help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "Usage" in result.output

    def test_cli_serve_help(self):
        """Test that CLI serve subcommand shows help."""
        runner = CliRunner()
        result = runner.invoke(cli, ["serve", "--help"])
        assert result.exit_code == 0

    def test_cli_no_args(self):
        """Test CLI with no arguments."""
        runner = CliRunner()
        result = runner.invoke(cli)
        assert result.exit_code == 0

    def test_cli_invalid_option(self):
        """Test CLI with invalid option."""
        runner = CliRunner()
        result = runner.invoke(cli, ["--invalid-option"])
        assert result.exit_code != 0
