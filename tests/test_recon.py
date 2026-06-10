"""
Tests for ReconTools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
from bugbounty_mcp_server.tools.recon import ReconTools


class TestReconTools:
    """Tests for ReconTools."""

    def test_initialization(self, config):
        """Test ReconTools initialization."""
        tools = ReconTools(config)
        assert tools.config is config

    def test_get_tools_returns_list(self, config):
        """Test get_tools returns a list of Tool objects."""
        tools = ReconTools(config)
        result = tools.get_tools()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tool_names_are_unique(self, config):
        """Test all tool names are unique."""
        tools = ReconTools(config)
        tool_list = tools.get_tools()
        names = [t.name for t in tool_list]
        assert len(names) == len(set(names))

    @pytest.mark.asyncio
    async def test_whois_lookup_blocked_target(self, config):
        """Test whois_lookup returns error for blocked target."""
        config.blocked_targets = ["evil.com"]
        tools = ReconTools(config)
        result = await tools.whois_lookup("evil.com")
        assert "not allowed" in result.lower()

    @pytest.mark.asyncio
    async def test_dns_enumeration_blocked_target(self, config):
        """Test dns_enumeration returns error for blocked target."""
        config.blocked_targets = ["evil.com"]
        tools = ReconTools(config)
        result = await tools.dns_enumeration("evil.com")
        assert "not allowed" in result.lower()

    @pytest.mark.asyncio
    async def test_certificate_transparency_blocked(self, config):
        """Test certificate_transparency returns error for blocked."""
        config.blocked_targets = ["evil.com"]
        tools = ReconTools(config)
        result = await tools.certificate_transparency("evil.com")
        assert "not allowed" in result.lower()

    def test_tools_have_descriptions(self, config):
        """Test all tools have non-empty descriptions."""
        tools = ReconTools(config)
        tool_list = tools.get_tools()
        for t in tool_list:
            assert t.description, f"Tool {t.name} has no description"

    def test_tools_have_input_schema(self, config):
        """Test all tools have input schema."""
        tools = ReconTools(config)
        tool_list = tools.get_tools()
        for t in tool_list:
            assert t.inputSchema is not None
            assert "type" in t.inputSchema
            assert t.inputSchema["type"] == "object"
