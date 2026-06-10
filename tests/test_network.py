"""
Tests for NetworkTools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bugbounty_mcp_server.tools.network import NetworkTools


class TestNetworkTools:
    """Tests for NetworkTools."""

    def test_initialization(self, config):
        """Test NetworkTools initialization."""
        tools = NetworkTools(config)
        assert tools.config is config

    def test_get_tools_returns_list(self, config):
        """Test get_tools returns a list."""
        tools = NetworkTools(config)
        result = tools.get_tools()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tool_names_are_unique(self, config):
        """Test all tool names are unique."""
        tools = NetworkTools(config)
        names = [t.name for t in tools.get_tools()]
        assert len(names) == len(set(names))

    @pytest.mark.asyncio
    async def test_network_discovery_blocked(self, config):
        """Test network_discovery returns error for blocked."""
        config.blocked_targets = ["evil.com"]
        tools = NetworkTools(config)
        result = await tools.network_discovery("evil.com")
        assert "not allowed" in result.lower()

    @pytest.mark.asyncio
    async def test_cdn_detection_blocked(self, config):
        """Test cdn_detection returns error for blocked."""
        config.blocked_targets = ["evil.com"]
        tools = NetworkTools(config)
        result = await tools.cdn_detection("evil.com")
        assert "not allowed" in result.lower()

    def test_parse_traceroute_output_empty(self, config):
        """Test parsing empty traceroute output."""
        tools = NetworkTools(config)
        result = tools._parse_traceroute_output("")
        assert isinstance(result, list)
        assert len(result) == 0

    def test_parse_traceroute_output_valid(self, config):
        """Test parsing valid traceroute output."""
        tools = NetworkTools(config)
        sample_output = " 1  192.168.1.1  1.234 ms\n 2  10.0.0.1  2.345 ms"
        result = tools._parse_traceroute_output(sample_output)
        assert isinstance(result, list)
