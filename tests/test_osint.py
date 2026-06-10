"""
Tests for OSINTTools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bugbounty_mcp_server.tools.osint import OSINTTools


class TestOSINTTools:
    """Tests for OSINTTools."""

    def test_initialization(self, config):
        """Test OSINTTools initialization."""
        tools = OSINTTools(config)
        assert tools.config is config

    def test_get_tools_returns_list(self, config):
        """Test get_tools returns a list."""
        tools = OSINTTools(config)
        result = tools.get_tools()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tool_names_are_unique(self, config):
        """Test all tool names are unique."""
        tools = OSINTTools(config)
        names = [t.name for t in tools.get_tools()]
        assert len(names) == len(set(names))

    def test_detect_indicator_type_ip(self, config):
        """Test indicator type detection for IP."""
        tools = OSINTTools(config)
        assert tools._detect_indicator_type("192.168.1.1") == "ip"

    def test_detect_indicator_type_domain(self, config):
        """Test indicator type detection for domain."""
        tools = OSINTTools(config)
        assert tools._detect_indicator_type("example.com") == "domain"

    def test_detect_indicator_type_url(self, config):
        """Test indicator type detection for URL."""
        tools = OSINTTools(config)
        result = tools._detect_indicator_type("https://example.com/path")
        assert result in ("url", "domain")

    def test_detect_indicator_type_hash(self, config):
        """Test indicator type detection for hash."""
        tools = OSINTTools(config)
        md5_hash = "d41d8cd98f00b204e9800998ecf8427e"
        assert tools._detect_indicator_type(md5_hash) == "hash"

    def test_detect_indicator_type_unknown(self, config):
        """Test indicator type detection for unknown."""
        tools = OSINTTools(config)
        assert tools._detect_indicator_type("some_random_text") == "unknown"

    def test_assess_threat_level(self, config):
        """Test threat level assessment."""
        tools = OSINTTools(config)
        results = {
            "malicious": True,
            "reported_attacks": 5,
            "confidence": "high",
        }
        assessment = tools._assess_threat_level(results)
        assert isinstance(assessment, dict)
