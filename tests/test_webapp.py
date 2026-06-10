"""
Tests for WebApplicationTools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch, PropertyMock
from bugbounty_mcp_server.tools.webapp import WebApplicationTools


class TestWebApplicationTools:
    """Tests for WebApplicationTools."""

    def test_initialization(self, config):
        """Test WebApplicationTools initialization."""
        tools = WebApplicationTools(config)
        assert tools.config is config

    def test_get_tools_returns_list(self, config):
        """Test get_tools returns a list of Tool objects."""
        tools = WebApplicationTools(config)
        result = tools.get_tools()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tool_names_are_unique(self, config):
        """Test all tool names are unique."""
        tools = WebApplicationTools(config)
        tool_list = tools.get_tools()
        names = [t.name for t in tool_list]
        assert len(names) == len(set(names))

    def test_analyze_security_headers_missing(self, config):
        """Test analyzing missing security headers."""
        tools = WebApplicationTools(config)
        headers = {
            "Content-Type": "text/html",
            "Server": "nginx",
        }
        issues = tools._analyze_security_headers(headers)
        assert len(issues) >= 4
        header_types = [i["header"] for i in issues]
        assert "strict-transport-security" in header_types
        assert "content-security-policy" in header_types

    def test_analyze_security_headers_present(self, config):
        """Test analyzing when security headers are present."""
        tools = WebApplicationTools(config)
        headers = {
            "Strict-Transport-Security": "max-age=31536000",
            "Content-Security-Policy": "default-src 'self'",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
        }
        issues = tools._analyze_security_headers(headers)
        missing = [i for i in issues if "Missing" in i["type"]]
        assert len(missing) == 0

    def test_analyze_security_headers_disclosure(self, config):
        """Test detecting information disclosure headers."""
        tools = WebApplicationTools(config)
        headers = {
            "Server": "Apache/2.4.41",
            "X-Powered-By": "PHP/7.4",
        }
        issues = tools._analyze_security_headers(headers)
        disclosure = [i for i in issues if i["type"] == "Information Disclosure"]
        assert len(disclosure) >= 2

    @pytest.mark.asyncio
    async def test_broken_access_control_blocked(self, config):
        """Test broken_access_control returns error for blocked target."""
        config.blocked_targets = ["evil.com"]
        tools = WebApplicationTools(config)
        result = await tools.broken_access_control_test("https://evil.com")
        assert "not allowed" in result.lower()

    @pytest.mark.asyncio
    async def test_api_security_test_blocked(self, config):
        """Test api_security_test returns error for blocked target."""
        config.blocked_targets = ["evil.com"]
        tools = WebApplicationTools(config)
        result = await tools.api_security_test("https://api.evil.com")
        assert "not allowed" in result.lower()

    def test_analyze_content_sensitivity(self, config):
        """Test content sensitivity scoring."""
        tools = WebApplicationTools(config)
        content = "password = secret123"
        score = tools._analyze_content_sensitivity(content)
        assert score > 0

    def test_analyze_content_sensitivity_clean(self, config):
        """Test content sensitivity scoring for clean content."""
        tools = WebApplicationTools(config)
        content = "Hello, this is normal text"
        score = tools._analyze_content_sensitivity(content)
        assert score == 0
