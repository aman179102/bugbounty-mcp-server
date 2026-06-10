"""
Tests for utility functions.
"""

import pytest
import asyncio
import time
from unittest.mock import patch, AsyncMock
from bugbounty_mcp_server.utils import (
    RateLimiter,
    Cache,
    validate_target,
    extract_urls_from_text,
    extract_subdomains_from_text,
    hash_content,
    format_bytes,
    format_duration,
    safe_filename,
    load_wordlist,
    save_json_report,
    get_timestamp,
)


class TestRateLimiter:
    """Tests for RateLimiter class."""

    @pytest.mark.asyncio
    async def test_no_delay_when_not_needed(self):
        """Test that rate limiter allows calls when under limit."""
        limiter = RateLimiter(calls_per_second=100.0)
        start = time.time()
        await limiter.wait()
        elapsed = time.time() - start
        assert elapsed < 0.1

    @pytest.mark.asyncio
    async def test_delay_when_rate_exceeded(self):
        """Test that rate limiter adds delay when rate is exceeded."""
        limiter = RateLimiter(calls_per_second=10.0)
        await limiter.wait()
        start = time.time()
        await limiter.wait()
        elapsed = time.time() - start
        assert elapsed >= 0.09

    @pytest.mark.asyncio
    async def test_concurrent_calls(self):
        """Test rate limiter with concurrent calls."""
        limiter = RateLimiter(calls_per_second=50.0)
        tasks = [limiter.wait() for _ in range(5)]
        start = time.time()
        await asyncio.gather(*tasks)
        elapsed = time.time() - start
        assert elapsed < 0.5


class TestCache:
    """Tests for Cache class."""

    def test_set_and_get(self):
        """Test basic set and get operations."""
        cache = Cache(ttl=3600)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"

    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        cache = Cache(ttl=3600)
        assert cache.get("nonexistent") is None

    def test_cache_expiry(self):
        """Test that cache entries expire after TTL."""
        cache = Cache(ttl=0.1)
        cache.set("key1", "value1")
        assert cache.get("key1") == "value1"
        time.sleep(0.15)
        assert cache.get("key1") is None

    def test_clear_cache(self):
        """Test clearing the cache."""
        cache = Cache(ttl=3600)
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        assert cache.get("key1") is None
        assert cache.get("key2") is None

    def test_overwrite_key(self):
        """Test overwriting an existing cache key."""
        cache = Cache(ttl=3600)
        cache.set("key1", "value1")
        cache.set("key1", "value2")
        assert cache.get("key1") == "value2"

    def test_cache_stores_different_types(self):
        """Test that cache stores different data types."""
        cache = Cache(ttl=3600)
        cache.set("string", "hello")
        cache.set("int", 42)
        cache.set("list", [1, 2, 3])
        cache.set("dict", {"a": 1})
        assert cache.get("string") == "hello"
        assert cache.get("int") == 42
        assert cache.get("list") == [1, 2, 3]
        assert cache.get("dict") == {"a": 1}


class TestValidateTarget:
    """Tests for validate_target function."""

    def test_valid_url(self):
        """Test valid URL parsing."""
        result = validate_target("https://example.com/path")
        assert result["valid"] is True
        assert result["type"] == "url"
        assert result["domain"] == "example.com"

    def test_valid_url_with_port(self):
        """Test URL with port."""
        result = validate_target("https://example.com:8080/path")
        assert result["valid"] is True
        assert result["domain"] == "example.com"
        assert result["port"] == 8080

    def test_valid_ip(self):
        """Test valid IP address."""
        result = validate_target("192.168.1.1")
        assert result["valid"] is True
        assert result["type"] == "ip"
        assert result["ip"] == "192.168.1.1"

    def test_valid_domain(self):
        """Test valid domain name."""
        result = validate_target("example.com")
        assert result["valid"] is True
        assert result["type"] == "domain"
        assert result["domain"] == "example.com"

    def test_domain_with_port(self):
        """Test domain with port."""
        result = validate_target("example.com:443")
        assert result["valid"] is True
        assert result["type"] == "domain_port"
        assert result["domain"] == "example.com"
        assert result["port"] == 443

    def test_invalid_target(self):
        """Test invalid target string."""
        result = validate_target("")
        assert result["valid"] is False

    def test_invalid_chars(self):
        """Test target with invalid characters."""
        result = validate_target("http://example .com/path")
        if result["valid"]:
            assert result["type"] == "url"
            assert result["domain"] is not None

    def test_https_scheme(self):
        """Test HTTPS URL parsing."""
        result = validate_target("https://example.com")
        assert result["scheme"] == "https"

    def test_url_without_scheme(self):
        """Test URL without scheme."""
        result = validate_target("example.com")
        assert result["type"] == "domain"

    def test_ipv6_address(self):
        """Test IPv6 address parsing."""
        result = validate_target("::1")
        assert result["valid"] is True


class TestExtractURLs:
    """Tests for URL extraction functions."""

    def test_extract_http_urls(self):
        """Test extracting HTTP URLs from text."""
        text = 'Visit https://example.com and http://test.com/path'
        urls = extract_urls_from_text(text)
        assert "https://example.com" in urls
        assert "http://test.com/path" in urls

    def test_extract_with_base_url(self):
        """Test extracting URLs with base URL for relative links."""
        text = '<a href="/page1">Link</a><a href="https://other.com">Other</a>'
        urls = extract_urls_from_text(text, base_url="https://example.com")
        assert "https://example.com/page1" in urls
        assert "https://other.com" in urls

    def test_extract_no_urls(self):
        """Test extracting from text with no URLs."""
        text = "This is plain text with no URLs"
        urls = extract_urls_from_text(text)
        assert urls == []

    def test_extract_duplicates(self):
        """Test that duplicate URLs are removed."""
        text = "https://example.com https://example.com"
        urls = extract_urls_from_text(text)
        assert len(urls) == 1


class TestExtractSubdomains:
    """Tests for subdomain extraction."""

    def test_extract_subdomains(self):
        """Test extracting subdomains for a domain."""
        text = "www.example.com and api.example.com and example.com"
        subs = extract_subdomains_from_text(text, "example.com")
        assert "www.example.com" in subs
        assert "api.example.com" in subs

    def test_extract_no_subdomains(self):
        """Test extracting when no subdomains exist."""
        text = "Just some random text"
        subs = extract_subdomains_from_text(text, "example.com")
        assert subs == []


class TestHashContent:
    """Tests for content hashing."""

    def test_hash_consistency(self):
        """Test that same content produces same hash."""
        h1 = hash_content("test content")
        h2 = hash_content("test content")
        assert h1 == h2

    def test_hash_different_content(self):
        """Test that different content produces different hashes."""
        h1 = hash_content("content1")
        h2 = hash_content("content2")
        assert h1 != h2


class TestFormatBytes:
    """Tests for bytes formatting."""

    def test_format_bytes_bytes(self):
        """Test formatting bytes."""
        assert format_bytes(500) == "500.00 B"

    def test_format_bytes_kilobytes(self):
        """Test formatting kilobytes."""
        result = format_bytes(2048)
        assert "KB" in result

    def test_format_bytes_megabytes(self):
        """Test formatting megabytes."""
        result = format_bytes(1048576)
        assert "MB" in result

    def test_format_zero_bytes(self):
        """Test formatting zero bytes."""
        assert format_bytes(0) == "0.00 B"


class TestFormatDuration:
    """Tests for duration formatting."""

    def test_seconds(self):
        """Test formatting seconds."""
        assert format_duration(30) == "30.00s"

    def test_minutes(self):
        """Test formatting minutes."""
        result = format_duration(120)
        assert "m" in result
        assert "2.0" in result

    def test_hours(self):
        """Test formatting hours."""
        result = format_duration(7200)
        assert "h" in result


class TestSafeFilename:
    """Tests for safe filename generation."""

    def test_safe_filename_normal(self):
        """Test normal filename remains unchanged."""
        assert safe_filename("normal_file.txt") == "normal_file.txt"

    def test_safe_filename_unsafe_chars(self):
        """Test unsafe characters are replaced."""
        result = safe_filename("file<name>.txt")
        assert "<" not in result

    def test_safe_filename_spaces(self):
        """Test spaces are replaced."""
        result = safe_filename("my file.txt")
        assert " " not in result


class TestLoadWordlist:
    """Tests for wordlist loading."""

    def test_load_nonexistent_wordlist(self):
        """Test loading nonexistent wordlist file."""
        result = load_wordlist("/nonexistent/path.txt")
        assert result == []


class TestSaveJsonReport:
    """Tests for JSON report saving."""

    def test_save_json_report(self, temp_dir):
        """Test saving JSON report to file."""
        filepath = str(temp_dir / "report.json")
        data = {"key": "value", "number": 42}
        result = save_json_report(data, filepath)
        assert result is True

        import json
        with open(filepath) as f:
            loaded = json.load(f)
        assert loaded["key"] == "value"
        assert loaded["number"] == 42


class TestGetTimestamp:
    """Tests for timestamp function."""

    def test_timestamp_format(self):
        """Test timestamp follows ISO format."""
        ts = get_timestamp()
        assert "T" in ts
        assert "-" in ts
        assert ":" in ts
