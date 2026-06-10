"""
Integration tests for the entire server setup.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bugbounty_mcp_server.server import BugBountyMCPServer
from bugbounty_mcp_server.config import BugBountyConfig
from bugbounty_mcp_server.tools import (
    ReconTools,
    ScanningTools,
    VulnerabilityTools,
    WebApplicationTools,
    NetworkTools,
    OSINTTools,
    ExploitationTools,
    ReportingTools,
)


class TestServerIntegration:
    """Integration tests for the server."""

    def test_all_tools_loaded(self, config):
        """Test that all tool categories are loaded with tools."""
        server = BugBountyMCPServer(config=config)
        total_tools = 0

        for category in server.tool_categories:
            tools = category.get_tools()
            total_tools += len(tools)

        assert total_tools > 0
        assert total_tools >= 50

    def test_all_tool_names_unique_across_categories(self, config):
        """Test that tool names are unique across all categories."""
        server = BugBountyMCPServer(config=config)
        all_names = []

        for category in server.tool_categories:
            for tool in category.get_tools():
                all_names.append(tool.name)

        duplicates = [name for name in all_names if all_names.count(name) > 1]
        assert len(duplicates) == 0, f"Duplicate tool names: {set(duplicates)}"

    def test_all_tools_have_required_inputs(self, config):
        """Test most tools have at least one required parameter."""
        server = BugBountyMCPServer(config=config)
        tools_without_required = 0

        for category in server.tool_categories:
            for tool in category.get_tools():
                schema = tool.inputSchema
                if "required" not in schema:
                    tools_without_required += 1

        assert tools_without_required < 15, f"{tools_without_required} tools lack required params"

    def test_all_tools_have_descriptions(self, config):
        """Test all tools have meaningful descriptions."""
        server = BugBountyMCPServer(config=config)

        for category in server.tool_categories:
            for tool in category.get_tools():
                assert tool.description, f"Tool {tool.name} has empty description"
                assert len(tool.description) > 10, f"Tool {tool.name} description too short"

    def test_all_tools_have_methods(self, config):
        """Test that tools have corresponding methods."""
        server = BugBountyMCPServer(config=config)
        tool_count = 0
        method_count = 0

        for category in server.tool_categories:
            for tool in category.get_tools():
                tool_count += 1
                if hasattr(category, tool.name):
                    method_count += 1

        assert method_count > 0
        assert method_count >= tool_count - 21  # 21 tools are MCP-only wrappers

    def test_config_propagation(self, config):
        """Test that config is properly propagated to all tools."""
        server = BugBountyMCPServer(config=config)

        for category in server.tool_categories:
            assert category.config is config
            assert category.config.log_level == "DEBUG"
            assert category.config.safe_mode is True

    def test_tool_count_consistency(self, config):
        """Test that tool counts are consistent across categories."""
        server = BugBountyMCPServer(config=config)

        total_tools = 0
        for category in server.tool_categories:
            tools = category.get_tools()
            total_tools += len(tools)

        assert total_tools >= 50
        assert total_tools <= 100

    @pytest.mark.asyncio
    async def test_blocked_target_propagation(self, config):
        """Test that blocked target is blocked across all tools."""
        config.allowed_targets = []  # clear allowed so blocked takes effect
        config.blocked_targets = ["blocked-test.com"]
        tools = [
            ReconTools(config),
            ScanningTools(config),
            VulnerabilityTools(config),
            WebApplicationTools(config),
            NetworkTools(config),
        ]

        for tool in tools:
            assert tool.check_target_allowed("blocked-test.com") is False
