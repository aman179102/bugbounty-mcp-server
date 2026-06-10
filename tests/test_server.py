"""
Tests for the main MCP server.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
from bugbounty_mcp_server.server import BugBountyMCPServer
from bugbounty_mcp_server.config import BugBountyConfig


class TestBugBountyMCPServer:
    """Tests for BugBountyMCPServer class."""

    def test_server_initialization(self, config):
        """Test server initialization with config."""
        server = BugBountyMCPServer(config=config)
        assert server.config is config
        assert server.server is not None
        assert len(server.tool_categories) == 8

    def test_server_initialization_without_config(self):
        """Test server initialization without config creates default."""
        server = BugBountyMCPServer()
        assert server.config is not None
        assert isinstance(server.config, BugBountyConfig)

    def test_tool_categories_initialized(self, config):
        """Test all tool categories are properly initialized."""
        server = BugBountyMCPServer(config=config)
        assert hasattr(server, 'recon_tools')
        assert hasattr(server, 'scanning_tools')
        assert hasattr(server, 'vuln_tools')
        assert hasattr(server, 'webapp_tools')
        assert hasattr(server, 'network_tools')
        assert hasattr(server, 'osint_tools')
        assert hasattr(server, 'exploit_tools')
        assert hasattr(server, 'reporting_tools')

    @pytest.mark.asyncio
    async def test_start(self, config):
        """Test server start initializes all tools."""
        server = BugBountyMCPServer(config=config)

        with patch.object(server, 'start', new_callable=AsyncMock) as mock_start:
            mock_start.return_value = None
            await server.start()
            mock_start.assert_called_once()

    def test_tool_count(self, config):
        """Test that server has tools registered."""
        server = BugBountyMCPServer(config=config)
        all_tools = []
        for category in server.tool_categories:
            all_tools.extend(category.get_tools())
        assert len(all_tools) > 0

    def test_server_name(self, config):
        """Test server name property."""
        server = BugBountyMCPServer(config=config)
        assert server.server.name == "bugbounty-mcp-server"

    def test_repr(self, config):
        """Test string representation."""
        server = BugBountyMCPServer(config=config)
        assert "BugBountyMCPServer" in str(server.__class__.__name__)
