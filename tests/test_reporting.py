"""
Tests for ReportingTools.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from bugbounty_mcp_server.tools.reporting import ReportingTools


class TestReportingTools:
    """Tests for ReportingTools."""

    def test_initialization(self, config):
        """Test ReportingTools initialization."""
        tools = ReportingTools(config)
        assert tools.config is config

    def test_get_tools_returns_list(self, config):
        """Test get_tools returns a list."""
        tools = ReportingTools(config)
        result = tools.get_tools()
        assert isinstance(result, list)
        assert len(result) > 0

    def test_tool_names_are_unique(self, config):
        """Test all tool names are unique."""
        tools = ReportingTools(config)
        names = [t.name for t in tools.get_tools()]
        assert len(names) == len(set(names))

    def test_analyze_scan_data_empty(self, config):
        """Test analyzing empty scan data."""
        tools = ReportingTools(config)
        result = tools._analyze_scan_data({})
        assert isinstance(result, dict)

    def test_generate_vulnerability_summary(self, config):
        """Test vulnerability summary generation."""
        tools = ReportingTools(config)
        scan_results = {
            "vulnerabilities": [
                {"severity": "High", "type": "SQL Injection"},
                {"severity": "Medium", "type": "XSS"},
            ]
        }
        summary = tools._generate_vulnerability_summary(scan_results, None)
        assert isinstance(summary, dict)

    def test_calculate_kpis(self, config):
        """Test KPI calculation."""
        tools = ReportingTools(config)
        data = {
            "total_scan_time": 3600,
            "total_findings": 10,
            "critical_findings": 2,
            "high_findings": 3,
            "resolved_findings": 5,
        }
        kpis = tools._calculate_kpis(data)
        assert isinstance(kpis, dict)

    def test_prioritize_vulnerabilities(self, config):
        """Test vulnerability prioritization."""
        tools = ReportingTools(config)
        vulns = [
            {"severity": "Low", "name": "Info leak"},
            {"severity": "Critical", "name": "RCE"},
            {"severity": "Medium", "name": "XSS"},
        ]
        prioritized = tools._prioritize_vulnerabilities(vulns, None, None)
        assert len(prioritized) > 0
