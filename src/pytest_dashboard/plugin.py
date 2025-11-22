#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pytest-dashboard plugin
Pytest hooks for dashboard-style HTML reports
"""

import pytest
from typing import Dict, Any
from .config import ReporterConfig
from .error_reporting import ErrorClassifier, EnhancedErrorReporter


def pytest_addoption(parser):
    """Add command-line options for pytest-dashboard."""
    group = parser.getgroup("dashboard", "Dashboard HTML Report")
    
    # Branding options
    group.addoption(
        "--dashboard-company-name",
        action="store",
        dest="dashboard_company_name",
        default="Test Automation Framework",
        help="Company name for dashboard branding"
    )
    group.addoption(
        "--dashboard-report-title",
        action="store",
        dest="dashboard_report_title",
        default="Test Execution Dashboard",
        help="Report title for dashboard"
    )
    group.addoption(
        "--dashboard-logo-url",
        action="store",
        dest="dashboard_logo_url",
        default=None,
        help="Logo URL or base64 encoded image"
    )
    
    # Chart options
    group.addoption(
        "--dashboard-charts",
        action="store_true",
        dest="dashboard_charts",
        default=True,
        help="Enable chart visualizations"
    )
    group.addoption(
        "--no-dashboard-charts",
        action="store_false",
        dest="dashboard_charts",
        help="Disable chart visualizations"
    )
    
    # Report options
    group.addoption(
        "--dashboard-error-classification",
        action="store_true",
        dest="dashboard_error_classification",
        default=True,
        help="Enable intelligent error classification"
    )
    group.addoption(
        "--dashboard-config",
        action="store",
        dest="dashboard_config",
        default="pytest_dashboard.yaml",
        help="Path to dashboard configuration YAML file"
    )


def pytest_configure(config):
    """Configure pytest-dashboard plugin."""
    # Load configuration
    config_file = config.getoption("dashboard_config")
    reporter_config = ReporterConfig.from_yaml(config_file)
    
    # Store configuration in pytest config for access by other hooks
    config._dashboard_config = reporter_config
    config._dashboard_error_reporter = EnhancedErrorReporter()
    
    # Add metadata for pytest-html integration
    if hasattr(config, '_metadata'):
        config._metadata['Dashboard'] = 'pytest-dashboard v1.0.0'


def pytest_html_report_title(report):
    """Customize the HTML report title."""
    if hasattr(report.config, '_dashboard_config'):
        config = report.config._dashboard_config
        report.title = config.branding.report_title


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results and error information."""
    outcome = yield
    report = outcome.get_result()
    
    if hasattr(item.config, '_dashboard_error_reporter'):
        error_reporter = item.config._dashboard_error_reporter
        
        if report.failed and call.excinfo:
            # Capture error information
            error_info = error_reporter.capture_test_error(
                test_id=item.nodeid,
                log_content=str(call.excinfo.getrepr()),
                exception=call.excinfo.value
            )
            
            # Attach error classification to report
            if error_info:
                report.dashboard_error_category = error_info.error_category
                report.dashboard_error_type = error_info.error_type
                report.dashboard_suggested_action = error_info.suggested_action


def pytest_html_results_table_header(cells):
    """Add custom columns to results table."""
    cells.insert(2, '<th>Error Category</th>')
    cells.insert(3, '<th>Error Type</th>')


def pytest_html_results_table_row(report, cells):
    """Add custom data to results table rows."""
    # Add error category
    if hasattr(report, 'dashboard_error_category'):
        cells.insert(2, f'<td>{report.dashboard_error_category}</td>')
    else:
        cells.insert(2, '<td>N/A</td>')
    
    # Add error type
    if hasattr(report, 'dashboard_error_type'):
        cells.insert(3, f'<td>{report.dashboard_error_type}</td>')
    else:
        cells.insert(3, '<td>N/A</td>')


def pytest_html_results_summary(prefix, summary, postfix):
    """Add dashboard summary information."""
    prefix.extend([
        '<div class="dashboard-summary">',
        '<h2>Dashboard Analytics</h2>',
        '<p>Enhanced by pytest-dashboard</p>',
        '</div>'
    ])


__all__ = [
    'pytest_addoption',
    'pytest_configure',
    'pytest_html_report_title',
    'pytest_runtest_makereport',
    'pytest_html_results_table_header',
    'pytest_html_results_table_row',
    'pytest_html_results_summary',
]
