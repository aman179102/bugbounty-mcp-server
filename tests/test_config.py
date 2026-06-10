"""
Tests for the configuration module.
"""

import pytest
import os
from pathlib import Path
from bugbounty_mcp_server.config import (
    BugBountyConfig,
    APIKeys,
    ToolConfig,
    ScanConfig,
    OutputConfig,
)


class TestAPIKeys:
    """Tests for APIKeys configuration."""

    def test_default_values(self):
        """Test that API keys default to None."""
        keys = APIKeys()
        assert keys.shodan is None
        assert keys.censys_id is None
        assert keys.censys_secret is None
        assert keys.virustotal is None
        assert keys.github is None
        assert keys.securitytrails is None
        assert keys.hunter_io is None
        assert keys.binaryedge is None
        assert keys.whoisxml is None
        assert keys.fofa is None

    def test_custom_values(self):
        """Test setting custom API key values."""
        keys = APIKeys(shodan="test_key", github="gh_token")
        assert keys.shodan == "test_key"
        assert keys.github == "gh_token"
        assert keys.censys_id is None


class TestToolConfig:
    """Tests for ToolConfig."""

    def test_default_paths(self):
        """Test default tool binary paths."""
        config = ToolConfig()
        assert config.nmap_path == "nmap"
        assert config.masscan_path == "masscan"
        assert config.nuclei_path == "nuclei"
        assert config.gobuster_path == "gobuster"
        assert config.headless_browser is True

    def test_custom_paths(self):
        """Test custom tool binary paths."""
        config = ToolConfig(nmap_path="/custom/nmap", max_concurrent_scans=20)
        assert config.nmap_path == "/custom/nmap"
        assert config.max_concurrent_scans == 20


class TestScanConfig:
    """Tests for ScanConfig."""

    def test_default_ports(self):
        """Test default ports list."""
        config = ScanConfig()
        assert "80" in config.default_ports
        assert "443" in config.default_ports
        assert "22" in config.default_ports
        assert len(config.default_ports) > 0

    def test_top_ports_default(self):
        """Test default number of top ports."""
        config = ScanConfig()
        assert config.top_ports == 1000

    def test_crawl_settings(self):
        """Test crawl configuration defaults."""
        config = ScanConfig()
        assert config.max_crawl_depth == 3
        assert config.max_pages_to_crawl == 100


class TestOutputConfig:
    """Tests for OutputConfig."""

    def test_default_values(self):
        """Test default output configuration."""
        config = OutputConfig()
        assert config.output_dir == "output"
        assert config.report_format == "json"
        assert config.save_raw_output is True
        assert config.create_html_report is True
        assert config.create_pdf_report is False

    def test_custom_output_dir(self):
        """Test custom output directory."""
        config = OutputConfig(output_dir="/custom/output")
        assert config.output_dir == "/custom/output"


class TestBugBountyConfig:
    """Tests for main BugBountyConfig."""

    def test_default_initialization(self, temp_dir):
        """Test default configuration initialization."""
        config = BugBountyConfig()
        assert config.log_level == "INFO"
        assert config.cache_enabled is True
        assert config.cache_ttl == 3600
        assert config.rate_limit_enabled is True
        assert config.requests_per_second == 10.0
        assert config.safe_mode is True

    def test_nested_configs(self):
        """Test nested configuration objects."""
        config = BugBountyConfig()
        assert isinstance(config.api_keys, APIKeys)
        assert isinstance(config.tools, ToolConfig)
        assert isinstance(config.scanning, ScanConfig)
        assert isinstance(config.output, OutputConfig)

    def test_safe_mode_target_check(self):
        """Test target validation in safe mode."""
        config = BugBountyConfig(
            safe_mode=True,
            allowed_targets=["example.com"]
        )
        assert config.is_target_allowed("example.com") is True
        assert config.is_target_allowed("sub.example.com") is True
        assert config.is_target_allowed("evil.com") is False

    def test_blocked_targets(self):
        """Test blocked targets functionality."""
        config = BugBountyConfig(
            safe_mode=False,
            blocked_targets=["blocked.com"]
        )
        assert config.is_target_allowed("example.com") is True
        assert config.is_target_allowed("blocked.com") is False
        assert config.is_target_allowed("sub.blocked.com") is False

    def test_empty_allowed_targets(self):
        """Test when allowed_targets list is empty in safe mode."""
        config = BugBountyConfig(safe_mode=True, allowed_targets=[])
        assert config.is_target_allowed("example.com") is True

    def test_env_variable_loading(self):
        """Test loading config from environment variables."""
        os.environ["SHODAN_API_KEY"] = "env_shodan_key"
        os.environ["LOG_LEVEL"] = "DEBUG"

        config = BugBountyConfig()
        assert config.api_keys.shodan == "env_shodan_key"
        assert config.log_level == "DEBUG"

        del os.environ["SHODAN_API_KEY"]
        del os.environ["LOG_LEVEL"]

    def test_api_key_retrieval(self):
        """Test get_api_key method."""
        config = BugBountyConfig()
        assert config.get_api_key("nonexistent") is None

        config.api_keys.shodan = "test_shodan"
        assert config.get_api_key("shodan") == "test_shodan"

    def test_directory_creation(self, temp_dir):
        """Test that required directories are created."""
        config = BugBountyConfig(
            data_dir=str(temp_dir / "test_data"),
        )
        assert Path(temp_dir / "test_data").exists()

    def test_pydantic_validation(self):
        """Test that pydantic validation works."""
        config = BugBountyConfig(log_level="INFO")
        assert config.log_level == "INFO"
