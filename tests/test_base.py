"""
Tests for the base tools class.
"""

import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from bugbounty_mcp_server.tools.base import BaseTools
from bugbounty_mcp_server.config import BugBountyConfig


class TestBaseTools:
    """Tests for BaseTools abstract class."""

    def test_abstract_class(self):
        """Test that BaseTools cannot be instantiated directly."""
        with pytest.raises(TypeError):
            BaseTools(MagicMock())

    def test_concrete_subclass(self, config):
        """Test that a concrete subclass can be instantiated."""

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        assert tools.config is config

    @pytest.mark.asyncio
    async def test_initialize(self, config):
        """Test initialize method."""

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        result = await tools.initialize()
        assert result is None

    def test_check_target_allowed_allowed(self, config):
        """Test check_target_allowed with allowed target."""

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        assert tools.check_target_allowed("example.com") is True

    def test_check_target_allowed_blocked(self, config):
        """Test check_target_allowed with blocked target."""
        config.blocked_targets = ["evil.com"]

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        assert tools.check_target_allowed("evil.com") is False

    @pytest.mark.asyncio
    async def test_rate_limit_called(self, config):
        """Test rate_limit method."""

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        config.rate_limit_enabled = False
        result = await tools.rate_limit()
        assert result is None

    def test_format_result_with_data(self, config):
        """Test format_result with provided data."""

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        result = tools.format_result({"key": "value"}, "Test Title")
        assert "Test Title" in result
        assert "key" in result

    def test_format_result_empty_data(self, config):
        """Test format_result with empty data."""

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        result = tools.format_result({}, "Empty")
        assert isinstance(result, str)

    def test_get_cached_disabled(self, config):
        """Test get_cached when caching is disabled."""
        config.cache_enabled = False

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        assert tools.get_cached("key") is None

    def test_set_cached_disabled(self, config):
        """Test set_cached when caching is disabled."""
        config.cache_enabled = False

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        tools.set_cached("key", "value")

    def test_cache_roundtrip(self, config):
        """Test cache roundtrip when enabled."""
        config.cache_enabled = True
        config.cache_ttl = 3600

        class ConcreteTools(BaseTools):
            def get_tools(self):
                return []

        tools = ConcreteTools(config)
        tools.set_cached("key1", "value1")
        assert tools.get_cached("key1") == "value1"
