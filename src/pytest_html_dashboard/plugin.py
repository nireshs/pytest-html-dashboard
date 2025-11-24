#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pytest-dashboard plugin
Pytest hooks for dashboard-style HTML reports
"""

import pytest
import os
import time
from typing import Dict, Any, Optional
from .config import ReporterConfig
from .error_reporting import ErrorClassifier, EnhancedErrorReporter
from .html_generator import enhance_html_report_dashboard
from .history import TestHistory

# Global state for collecting test results
_test_results = {}
_history_tracker: Optional[TestHistory] = None


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
        "--dashboard-reporting",
        action="store_true",
        dest="dashboard_reporting",
        default=True,
        help="Enable enhanced dashboard reporting"
    )
    group.addoption(
        "--no-dashboard-reporting",
        action="store_false",
        dest="dashboard_reporting",
        help="Disable enhanced dashboard reporting"
    )
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

    # v1.2.0 Feature options
    group.addoption(
        "--enable-history",
        action="store_true",
        dest="enable_history",
        default=None,
        help="Enable historical test tracking (v1.2.0)"
    )
    group.addoption(
        "--disable-history",
        action="store_true",
        dest="disable_history",
        default=False,
        help="Disable historical test tracking"
    )
    group.addoption(
        "--history-db",
        action="store",
        dest="history_db",
        default=None,
        help="Path to history database file (default: test-history.db)"
    )
    group.addoption(
        "--realtime-dashboard",
        action="store_true",
        dest="realtime_dashboard",
        default=False,
        help="Enable real-time WebSocket dashboard (v1.2.0)"
    )
    group.addoption(
        "--realtime-port",
        action="store",
        dest="realtime_port",
        type=int,
        default=8888,
        help="WebSocket server port for real-time dashboard (default: 8888)"
    )
    group.addoption(
        "--ai-provider",
        action="store",
        dest="ai_provider",
        default=None,
        help="AI provider: 'local', 'openai', or 'anthropic' (v1.2.0)"
    )
    group.addoption(
        "--ai-api-key",
        action="store",
        dest="ai_api_key",
        default=None,
        help="API key for AI-powered error analysis (v1.2.0)"
    )


def pytest_configure(config):
    """Configure pytest-dashboard plugin."""
    # Load configuration
    config_file = config.getoption("dashboard_config")
    reporter_config = ReporterConfig.from_yaml(config_file)

    # Override with command-line options if provided
    if config.getoption(
            "dashboard_company_name") != "Test Automation Framework":
        reporter_config.branding.company_name = config.getoption(
            "dashboard_company_name")
    if config.getoption(
            "dashboard_report_title") != "Test Execution Dashboard":
        reporter_config.branding.report_title = config.getoption(
            "dashboard_report_title")
    if config.getoption("dashboard_logo_url"):
        reporter_config.branding.logo_url = config.getoption(
            "dashboard_logo_url")

    reporter_config.charts.enable_charts = config.getoption("dashboard_charts")
    reporter_config.report.enable_error_classification = config.getoption(
        "dashboard_error_classification")

    # Override v1.2.0 feature options from CLI
    if config.getoption("enable_history"):
        reporter_config.historical.enable_tracking = True
    elif config.getoption("disable_history"):
        reporter_config.historical.enable_tracking = False

    if config.getoption("history_db"):
        reporter_config.historical.database_path = config.getoption("history_db")

    if config.getoption("realtime_dashboard"):
        reporter_config.realtime.enable_realtime = True
        reporter_config.realtime.websocket_port = config.getoption("realtime_port")

    if config.getoption("ai_provider"):
        reporter_config.ai.provider = config.getoption("ai_provider")

    if config.getoption("ai_api_key"):
        reporter_config.ai.api_key = config.getoption("ai_api_key")

    # Store configuration in pytest config for access by other hooks
    config._dashboard_config = reporter_config
    config._dashboard_error_reporter = EnhancedErrorReporter()

    # Initialize history tracker if enabled
    global _history_tracker
    if reporter_config.historical.enable_tracking:
        try:
            _history_tracker = TestHistory(
                db_path=reporter_config.historical.database_path
            )
            config._dashboard_history_tracker = _history_tracker
        except Exception as e:
            print(f"Warning: Failed to initialize history tracker: {e}")
            _history_tracker = None

    # Initialize real-time dashboard if enabled
    if reporter_config.realtime.enable_realtime:
        try:
            from .realtime import RealtimeDashboard
            realtime_server = RealtimeDashboard(
                port=reporter_config.realtime.websocket_port
            )
            realtime_server.start()
            config._dashboard_realtime = realtime_server
            print(f"[Real-time Dashboard] WebSocket server started on port {reporter_config.realtime.websocket_port}")
        except Exception as e:
            print(f"Warning: Failed to start real-time server: {e}")
            config._dashboard_realtime = None

    # Add metadata for pytest-html integration
    if hasattr(config, '_metadata'):
        config._metadata['Dashboard'] = 'pytest-html-dashboard v1.2.0'


def pytest_html_report_title(report):
    """Customize the HTML report title."""
    if hasattr(report.config, '_dashboard_config'):
        config = report.config._dashboard_config
        report.title = config.branding.report_title


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture test results and error information."""
    global _history_tracker
    outcome = yield
    report = outcome.get_result()

    if hasattr(item.config, '_dashboard_error_reporter'):
        error_reporter = item.config._dashboard_error_reporter
        realtime_server = getattr(item.config, '_dashboard_realtime', None)

        # Store test result globally for HTML generation
        test_id = item.nodeid

        if call.when == "call":
            _test_results[test_id] = {
                'nodeid': test_id,
                'outcome': report.outcome,
                'duration': getattr(report, 'duration', 0.0),
                'failed': report.failed,
                'passed': report.passed,
                'skipped': report.skipped,
            }

            # Emit real-time event if enabled
            if realtime_server:
                try:
                    realtime_server.emit_test_result({
                        'test_id': test_id,
                        'outcome': report.outcome,
                        'duration': getattr(report, 'duration', 0.0),
                    })
                except Exception as e:
                    pass  # Don't fail tests if real-time emission fails

            # Save to history database if enabled
            if _history_tracker:
                try:
                    _history_tracker.save_test_result({
                        'test_id': test_id,
                        'outcome': report.outcome,
                        'duration': getattr(report, 'duration', 0.0),
                        'timestamp': time.time(),
                    })
                except Exception as e:
                    pass  # Don't fail tests if history tracking fails

        if report.failed and call.excinfo:
            # Capture error information
            error_info = error_reporter.capture_test_error(
                test_id=test_id,
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


def pytest_sessionstart(session):
    """Emit session start event for real-time dashboard."""
    try:
        realtime_server = getattr(session.config, '_dashboard_realtime', None)
        if realtime_server:
            realtime_server.emit_event('session_start', {
                'timestamp': time.time(),
                'message': 'Test session started'
            })
    except Exception as e:
        # Don't fail tests if real-time fails
        pass


def pytest_sessionfinish(session, exitstatus):
    """Save historical data, cleanup real-time server and emit session finish event."""
    global _history_tracker

    # Save test run to history database
    if _history_tracker and _test_results:
        try:
            # Calculate test statistics
            passed = sum(1 for r in _test_results.values() if r.get('outcome') == 'passed')
            failed = sum(1 for r in _test_results.values() if r.get('outcome') == 'failed')
            skipped = sum(1 for r in _test_results.values() if r.get('outcome') == 'skipped')
            errors = sum(1 for r in _test_results.values() if r.get('outcome') == 'error')
            total_duration = sum(r.get('duration', 0) for r in _test_results.values())

            # Convert test results dict to list format expected by save_test_run
            tests_list = []
            for test_id, result in _test_results.items():
                tests_list.append({
                    'name': result.get('nodeid', test_id),
                    'outcome': result.get('outcome', 'unknown'),
                    'duration': result.get('duration', 0),
                    'error_message': result.get('error_message', ''),
                    'error_type': result.get('error_type', '')
                })

            # Prepare results dict for save_test_run
            results = {
                'summary': {
                    'total': len(_test_results),
                    'passed': passed,
                    'failed': failed,
                    'skipped': skipped,
                    'errors': errors,
                    'duration': total_duration
                },
                'tests': tests_list
            }

            # Save test run
            run_id = _history_tracker.save_test_run(results)
            print(f"\n[Historical Tracking] Saved test run #{run_id} with {len(tests_list)} tests to database")

        except Exception as e:
            print(f"\nWarning: Failed to save historical data: {e}")
            import traceback
            traceback.print_exc()

    # Cleanup real-time server
    try:
        realtime_server = getattr(session.config, '_dashboard_realtime', None)
        if realtime_server:
            # Emit finish event
            realtime_server.emit_event('session_finish', {
                'timestamp': time.time(),
                'exitstatus': exitstatus,
                'message': 'Test session finished'
            })
            # Give clients time to receive final events
            time.sleep(0.5)
            # Stop server
            realtime_server.stop()
            print("[Real-time Dashboard] WebSocket server stopped")
    except Exception as e:
        # Don't fail tests if cleanup fails
        pass


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """
    Post-process HTML report after ALL pytest operations complete.
    This runs after pytest-html finishes writing, ensuring we don't get overwritten.
    """
    # Get HTML file path from pytest-html
    html_path = getattr(config.option, 'htmlpath', None)

    if html_path and os.path.exists(html_path):
        # Give pytest-html time to finish writing the file
        time.sleep(0.5)

        try:
            # Get configuration and error reporter
            reporter_config = getattr(config, '_dashboard_config', None)
            error_reporter = getattr(config, '_dashboard_error_reporter', None)

            if reporter_config and reporter_config.report.enable_enhanced_reporting:
                # Enhance the HTML report with dashboard features
                enhance_html_report_dashboard(
                    html_path=html_path,
                    config=reporter_config,
                    test_results=_test_results,
                    error_reporter=error_reporter
                )
                print(
                    f"\n[SUCCESS] Enhanced dashboard report generated: {html_path}")
            else:
                print(
                    f"\n[WARNING] Enhanced reporting disabled. Basic report generated: {html_path}")

        except Exception as e:
            print(f"\n[WARNING] Could not enhance HTML report: {e}")
            import traceback
            traceback.print_exc()
    elif html_path:
        print(f"\n[WARNING] HTML report file not found at: {html_path}")


__all__ = [
    'pytest_addoption',
    'pytest_configure',
    'pytest_html_report_title',
    'pytest_runtest_makereport',
    'pytest_html_results_table_header',
    'pytest_html_results_table_row',
    'pytest_html_results_summary',
    'pytest_terminal_summary',
]
