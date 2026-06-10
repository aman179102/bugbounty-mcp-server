"""
Pytest fixtures and configuration for BugBounty MCP Server tests.
"""

import pytest
import asyncio
from typing import AsyncGenerator, Generator
from pathlib import Path
import tempfile
import os
from unittest.mock import AsyncMock, MagicMock, patch

from bugbounty_mcp_server.config import BugBountyConfig
from bugbounty_mcp_server.utils import RateLimiter, Cache
from bugbounty_mcp_server.server import BugBountyMCPServer


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_dir() -> Generator[Path, None, None]:
    """Create a temporary directory for test outputs."""
    with tempfile.TemporaryDirectory() as tmpdir:
        original_dir = os.getcwd()
        os.chdir(tmpdir)
        yield Path(tmpdir)
        os.chdir(original_dir)


@pytest.fixture
def config(temp_dir: Path) -> BugBountyConfig:
    """Create a test configuration with safe defaults."""
    config = BugBountyConfig(
        log_level="DEBUG",
        data_dir=str(temp_dir / "data"),
        cache_enabled=False,
        rate_limit_enabled=False,
        safe_mode=True,
        allowed_targets=["example.com", "test.com"],
        output={"output_dir": str(temp_dir / "output")},
    )
    return config


@pytest.fixture
def disabled_cache_config(config: BugBountyConfig) -> BugBountyConfig:
    """Configuration with caching disabled."""
    config.cache_enabled = False
    return config


@pytest.fixture
def enabled_cache_config(config: BugBountyConfig) -> BugBountyConfig:
    """Configuration with caching enabled."""
    config.cache_enabled = True
    config.cache_ttl = 3600
    return config


@pytest.fixture
def rate_limiter() -> RateLimiter:
    """Create a rate limiter instance."""
    return RateLimiter(calls_per_second=100.0)


@pytest.fixture
def cache() -> Cache:
    """Create a cache instance."""
    return Cache(ttl=3600)


@pytest.fixture
def server(config: BugBountyConfig) -> BugBountyMCPServer:
    """Create a server instance for testing."""
    return BugBountyMCPServer(config=config)


@pytest.fixture
def mock_aiohttp_session():
    """Create a mock aiohttp ClientSession."""
    with patch("aiohttp.ClientSession") as mock:
        session = AsyncMock()
        mock.return_value.__aenter__.return_value = session
        yield session


@pytest.fixture
def mock_response():
    """Create a standard mock response."""
    response = AsyncMock()
    response.status = 200
    response.headers = {
        "Content-Type": "text/html",
        "Server": "nginx/1.19.0",
        "X-Powered-By": "Express",
    }

    async def mock_text():
        return "<html><body>Test content</body></html>"

    async def mock_json():
        return {"status": "ok"}

    async def mock_read():
        return b"test binary content"

    response.text = mock_text
    response.json = mock_json
    response.read = mock_read

    async def mock_getitem(key):
        return response.headers.get(key)

    response.__getitem__ = mock_getitem

    def mock_get(key, default=None):
        return response.headers.get(key, default)

    response.get = mock_get
    return response


@pytest.fixture
def sample_targets() -> dict:
    """Sample target data for testing."""
    return {
        "url": "https://example.com",
        "domain": "example.com",
        "ip": "93.184.216.34",
        "subdomain": "www.example.com",
        "api_url": "https://api.example.com/v1",
    }
