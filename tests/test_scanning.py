"""
Tests for ScanningTools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bugbounty_mcp_server.tools.scanning import ScanningTools


class TestScanningTools:
    """Tests for ScanningTools."""

    def test_initialization(self, config):
        """Test ScanningTools initialization."""
        tools = ScanningTools(config)
        assert tools.config is config

    def test_get_tools_returns_list(self, config):
        """Test get_tools returns a list."""
        tools = ScanningTools(config)
        result = tools.get_tools()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tool_names_are_unique(self, config):
        """Test all tool names are unique."""
        tools = ScanningTools(config)
        names = [t.name for t in tools.get_tools()]
        assert len(names) == len(set(names))

    @pytest.mark.asyncio
    async def test_port_scan_blocked(self, config):
        """Test port_scan returns error for blocked target."""
        config.blocked_targets = ["evil.com"]
        tools = ScanningTools(config)
        result = await tools.port_scan("evil.com")
        assert "not allowed" in result.lower()

    @pytest.mark.asyncio
    async def test_web_directory_scan_blocked(self, config):
        """Test web_directory_scan returns error for blocked."""
        config.blocked_targets = ["evil.com"]
        tools = ScanningTools(config)
        result = await tools.web_directory_scan("https://evil.com")
        assert "not allowed" in result.lower()

    @pytest.mark.asyncio
    async def test_nuclei_scan_blocked(self, config):
        """Test nuclei_scan returns error for blocked target."""
        config.blocked_targets = ["evil.com"]
        tools = ScanningTools(config)
        result = await tools.nuclei_scan("evil.com")
        assert "not allowed" in result.lower()

    def test_extract_links_from_html(self, config):
        """Test extracting links from HTML."""
        tools = ScanningTools(config)
        html = '<a href="/page1">Link1</a><a href="https://external.com">External</a>'
        links = tools._extract_links(html, "https://example.com")
        assert isinstance(links, list)

    def test_extract_forms_from_html(self, config):
        """Test extracting forms from HTML."""
        tools = ScanningTools(config)
        html = '<form action="/login"><input name="user"><input name="pass"></form>'
        forms = tools._extract_forms(html, "https://example.com")
        assert isinstance(forms, list)

    def test_extract_js_files(self, config):
        """Test extracting JS files from HTML."""
        tools = ScanningTools(config)
        html = '<script src="/app.js"></script><script src="https://cdn.com/lib.js"></script>'
        js_files = tools._extract_js_files(html, "https://example.com")
        assert isinstance(js_files, list)
