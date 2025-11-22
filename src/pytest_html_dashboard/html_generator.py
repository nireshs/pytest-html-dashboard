#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HTML generation for pytest-html-dashboard
Generates enhanced, modern styled HTML reports with interactive charts and tables
"""

import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import platform


class HTMLGeneratorDashboard:
    """Generates enhanced HTML content with modern dashboard styling."""

    def __init__(self, config, test_results: Dict[str, Any], error_reporter, 
                 ai_insights=None, historical_data=None):
        """Initialize HTML generator with configuration and test data."""
        self.config = config
        self.test_results = test_results
        self.error_reporter = error_reporter
        self.ai_insights = ai_insights or []
        self.historical_data = historical_data

    def generate_dashboard_css(self) -> str:
        """Generate dashboard CSS with modern styling."""
        branding = self.config.branding

        return f"""
    <style>
        /* Enhanced Theme */
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}

        .container {{
            width: 100%;
            margin: 0;
            padding: 20px;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 0;
            box-shadow: none;
        }}

        .header-section {{
            text-align: center;
            margin-bottom: 20px;
            padding: 12px;
            background: linear-gradient(90deg, {branding.primary_color}, {branding.secondary_color});
            border-radius: 10px;
            color: white;
        }}

        .logo-container {{
            flex-shrink: 0;
            align-self: flex-start;
        }}

        .logo-title-container {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 15px;
            margin-bottom: 15px;
            flex-wrap: nowrap;
        }}

        .title-container {{
            text-align: center;
            flex-grow: 1;
        }}

        .main-title {{
            margin: 0;
            font-size: 24px;
            font-weight: bold;
            line-height: 1.2;
        }}

        @media (max-width: 768px) {{
            .logo-title-container {{
                gap: 10px;
                margin-bottom: 10px;
            }}
            .title-container {{
                text-align: left;
            }}
            .main-title {{
                font-size: 18px;
            }}
        }}

        .comprehensive-section {{
            margin: 30px 0;
            padding: 25px;
            background: rgba(240, 248, 255, 0.8);
            border-radius: 12px;
            border-left: 5px solid {branding.primary_color};
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        .section-title {{
            color: {branding.primary_color};
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 15px;
            padding-bottom: 8px;
            border-bottom: 2px solid {branding.primary_color};
        }}

        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}

        .info-item {{
            background: white;
            padding: 12px 15px;
            border-radius: 8px;
            border-left: 3px solid {branding.secondary_color};
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}

        .info-label {{
            font-weight: bold;
            color: {branding.primary_color};
            margin-bottom: 5px;
        }}

        .info-value {{
            color: #333;
            font-size: 14px;
        }}

        .status-dashboard {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }}

        .status-card {{
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            color: white;
            font-weight: bold;
        }}

        .status-passed {{ background: linear-gradient(135deg, {branding.success_color}, #45a049); }}
        .status-failed {{ background: linear-gradient(135deg, {branding.failure_color}, #da190b); }}
        .status-skipped {{ background: linear-gradient(135deg, {branding.warning_color}, #f57c00); }}
        .status-total {{ background: linear-gradient(135deg, #2196F3, #0b7dda); }}

        .chart-container {{
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin: 20px 0;
            flex-wrap: wrap;
        }}

        .chart-wrapper {{
            position: relative;
            width: 300px;
            height: 300px;
            margin: 10px;
        }}

        /* Enhanced table styling */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            background: white;
            border-radius: 10px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }}

        th, td {{
            padding: 12px 8px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }}

        th {{
            background: linear-gradient(90deg, {branding.primary_color}, {branding.secondary_color});
            color: white;
            font-weight: bold;
            position: sticky;
            top: 0;
        }}

        tr:hover {{
            background-color: rgba(0, 68, 136, 0.05);
        }}

        /* Column widths */
        .col-sno {{ width: 5%; text-align: center; font-weight: bold; }}
        .col-name {{ width: 25%; text-align: left; }}
        .col-start-time {{ width: 12%; text-align: center; font-size: 11px; }}
        .col-end-time {{ width: 12%; text-align: center; font-size: 11px; }}
        .col-duration {{ width: 8%; text-align: center; font-weight: bold; }}
        .col-result {{ width: 10%; text-align: center; font-weight: bold; }}
        .col-error-category {{ width: 12%; text-align: center; }}
        .col-result-details {{ width: 16%; text-align: left; font-size: 11px; }}

        .col-result.passed {{ background-color: #e8f5e8; color: #2e7d32; font-weight: bold; }}
        .col-result.failed {{ background-color: #ffebee; color: #c62828; font-weight: bold; }}
        .col-result.skipped {{ background-color: #fff3e0; color: #ef6c00; font-weight: bold; }}
        .col-result.error {{ background-color: #fce4ec; color: #ad1457; font-weight: bold; }}

        /* Enhanced Error Reporting Styles */
        .error-details-container {{
            position: relative;
            max-width: 200px;
        }}

        .error-toggle-btn {{
            background: #ff4444;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 11px;
            transition: all 0.3s ease;
        }}

        .error-toggle-btn:hover {{
            background: #cc0000;
            transform: translateY(-1px);
        }}

        .error-details-popup {{
            position: absolute;
            top: 30px;
            left: 0;
            background: white;
            border: 2px solid #ff4444;
            border-radius: 8px;
            padding: 15px;
            min-width: 400px;
            max-width: 500px;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            z-index: 1000;
            font-size: 12px;
            display: none;
        }}

        .error-details-popup h5 {{
            margin: 0 0 10px 0;
            color: #ff4444;
            font-size: 14px;
        }}

        .error-info-table {{
            width: 100%;
            border-collapse: collapse;
            margin: 5px 0;
        }}

        .error-info-table td {{
            padding: 4px 8px;
            border: 1px solid #eee;
            font-size: 11px;
        }}

        .error-info-table td:first-child {{
            background: #f5f5f5;
            font-weight: bold;
            width: 30%;
        }}

        .stack-trace {{
            margin-top: 10px;
            padding: 8px;
            background: #f8f8f8;
            border-radius: 4px;
        }}

        .stack-trace h6 {{
            margin: 0 0 5px 0;
            color: #666;
        }}

        .stack-trace pre {{
            margin: 0;
            font-size: 10px;
            color: #444;
            white-space: pre-wrap;
            max-height: 150px;
            overflow-y: auto;
        }}

        .error-category {{
            font-weight: bold;
            font-size: 11px;
        }}

        .suggested-action {{
            font-size: 11px;
            color: #0066cc;
            font-style: italic;
            max-width: 180px;
        }}

        .comprehensive-test-table {{
            width: 100%;
            border-collapse: collapse;
            font-family: 'Segoe UI', sans-serif;
            font-size: 12px;
        }}

        .comprehensive-test-table th {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 8px;
            text-align: center;
            font-weight: bold;
            font-size: 11px;
            border: 1px solid #ddd;
            position: sticky;
            top: 0;
            z-index: 10;
        }}

        .comprehensive-test-table td {{
            padding: 10px 8px;
            border: 1px solid #e0e0e0;
            text-align: center;
            vertical-align: middle;
            font-size: 11px;
        }}

        .comprehensive-test-table tbody tr:nth-child(even) {{
            background-color: #f8f9fa;
        }}

        .comprehensive-test-table tbody tr:hover {{
            background-color: #e3f2fd;
            transform: scale(1.01);
            transition: all 0.2s ease;
        }}

        /* Result-specific row styling */
        .test-row-passed {{ border-left: 4px solid #4caf50; }}
        .test-row-failed {{ border-left: 4px solid #f44336; }}
        .test-row-skipped {{ border-left: 4px solid #ff9800; }}
        .test-row-error {{ border-left: 4px solid #e91e63; }}

        /* Result cell styling */
        .result-passed {{
            background-color: #e8f5e8;
            color: #2e7d32;
            font-weight: bold;
            border-radius: 4px;
            padding: 4px 8px;
        }}
        .result-failed {{
            background-color: #ffebee;
            color: #c62828;
            font-weight: bold;
            border-radius: 4px;
            padding: 4px 8px;
        }}
        .result-skipped {{
            background-color: #fff3e0;
            color: #ef6c00;
            font-weight: bold;
            border-radius: 4px;
            padding: 4px 8px;
        }}
        .result-error {{
            background-color: #fce4ec;
            color: #ad1457;
            font-weight: bold;
            border-radius: 4px;
            padding: 4px 8px;
        }}

        .result-details {{
            max-width: 200px;
            text-align: left;
            font-size: 10px;
            word-wrap: break-word;
            overflow-wrap: break-word;
        }}

        /* Error Analysis Section */
        .error-analysis-section {{
            background: rgba(255, 235, 238, 0.9);
            border-left: 5px solid #f44336;
        }}

        .error-insights-container {{
            margin-top: 15px;
        }}

        .error-insight-item {{
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            border-left: 4px solid #f44336;
            box-shadow: 0 2px 8px rgba(244, 67, 54, 0.1);
        }}

        .error-insight-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }}

        .error-test-name {{
            font-weight: bold;
            color: #c62828;
            font-size: 14px;
        }}

        .error-badge {{
            background: #f44336;
            color: white;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: bold;
        }}

        .error-insight-body {{
            color: #666;
            font-size: 13px;
        }}

        .error-insight-body p {{
            margin: 8px 0;
        }}

        .error-insight-body .suggested-action {{
            color: #1976d2;
            background: #e3f2fd;
            padding: 8px;
            border-radius: 6px;
            border-left: 3px solid #1976d2;
        }}

        /* Filter and Sort Controls */
        .table-controls {{
            background: #f5f5f5;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 15px;
            display: flex;
            gap: 15px;
            align-items: center;
            flex-wrap: wrap;
        }}

        .filter-group {{
            display: flex;
            gap: 8px;
            align-items: center;
        }}

        .filter-group label {{
            font-weight: 600;
            color: #555;
            font-size: 13px;
        }}

        .filter-input {{
            padding: 6px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
            min-width: 200px;
        }}

        .filter-select {{
            padding: 6px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 13px;
            background: white;
            cursor: pointer;
        }}

        .clear-filters-btn {{
            padding: 6px 16px;
            background: #ff9800;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.3s ease;
        }}

        .clear-filters-btn:hover {{
            background: #f57c00;
            transform: translateY(-1px);
        }}

        .sortable-header {{
            cursor: pointer;
            user-select: none;
            position: relative;
            padding-right: 20px !important;
        }}

        .sortable-header:hover {{
            background: rgba(255,255,255,0.1);
        }}

        .sortable-header::after {{
            content: '⇅';
            position: absolute;
            right: 8px;
            opacity: 0.5;
            font-size: 14px;
        }}

        .sortable-header.sort-asc::after {{
            content: '↑';
            opacity: 1;
        }}

        .sortable-header.sort-desc::after {{
            content: '↓';
            opacity: 1;
        }}

        /* Test Steps Section */
        .test-steps-section {{
            background: rgba(232, 245, 233, 0.9);
            border-left: 5px solid #4caf50;
        }}

        .test-steps-stats {{
            display: flex;
            justify-content: space-around;
            margin: 15px 0;
            flex-wrap: wrap;
            gap: 10px;
        }}

        .step-stat {{
            background: white;
            padding: 10px 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
            text-align: center;
        }}

        .step-stat strong {{
            font-size: 18px;
            display: block;
            margin-top: 5px;
        }}

        .step-stat.step-passed strong {{ color: #4caf50; }}
        .step-stat.step-failed strong {{ color: #f44336; }}
        .step-stat.step-skipped strong {{ color: #ff9800; }}

        .test-steps-table-container {{
            margin-top: 20px;
            overflow-x: auto;
        }}

        .test-steps-table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }}

        .test-steps-table th {{
            background: linear-gradient(135deg, #4caf50 0%, #45a049 100%);
            color: white;
            padding: 12px;
            text-align: left;
            font-weight: bold;
        }}

        .test-steps-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #e0e0e0;
        }}

        .test-steps-table tbody tr:hover {{
            background-color: #f5f5f5;
        }}

        .step-row-passed {{ background-color: #e8f5e9; }}
        .step-row-failed {{ background-color: #ffebee; }}
        .step-row-skipped {{ background-color: #fff3e0; }}

        @media (max-width: 768px) {{
            .container {{ padding: 15px; }}
            .chart-wrapper {{ width: 250px; height: 250px; }}
            .info-grid {{ grid-template-columns: 1fr; }}
            .status-dashboard {{ grid-template-columns: repeat(2, 1fr); }}
            .comprehensive-test-table {{ font-size: 10px; }}
            .comprehensive-test-table th,
            .comprehensive-test-table td {{ padding: 6px 4px; }}
            .test-steps-stats {{ flex-direction: column; }}
            .error-insight-header {{ flex-direction: column; align-items: flex-start; gap: 8px; }}
        }}
    </style>
        """

    def generate_dashboard_header(self) -> str:
        """Generate dashboard header with logo and title."""
        branding = self.config.branding

        # Generic logo (placeholder - can be customized)
        logo_html = ""
        if branding.logo_url:
            logo_html = f'<img src="{
                branding.logo_url}" alt="Logo" style="height: 50px;">'
        else:
            # Default generic logo placeholder
            logo_html = f'<div style="height: 50px; width: 120px; background: white; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 11px; color: {
                branding.primary_color}; padding: 5px;">Company Logo</div>'

        return f"""
    <div class="container">
        <div class="header-section">
            <div class="logo-title-container">
                <div class="logo-container">
                    {logo_html}
                </div>
                <div class="title-container">
                    <h1 class="main-title">{branding.report_title}</h1>
                </div>
                <div class="logo-spacer" style="width: 50px;"></div>
            </div>
        </div>
        """

    def generate_test_configuration_section(self) -> str:
        """Generate test configuration section."""
        return """
        <div class="comprehensive-section">
            <div class="section-title">⚙️ Test Configuration</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Test Type:</div>
                    <div class="info-value">Automated Test Suite</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Execution Mode:</div>
                    <div class="info-value">Sequential</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Parallel Execution:</div>
                    <div class="info-value">No</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Retry Failed Tests:</div>
                    <div class="info-value">No</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Test Data Source:</div>
                    <div class="info-value">Configuration Files</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Reporting Format:</div>
                    <div class="info-value">HTML</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Screenshot on Failure:</div>
                    <div class="info-value">Yes</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Video Recording:</div>
                    <div class="info-value">No</div>
                </div>
            </div>
        </div>
        """

    def generate_environment_section(self) -> str:
        """Generate environment details section."""
        import pytest

        python_version = platform.python_version()
        pytest_version = pytest.__version__
        platform_info = f"{
            platform.system()} {
            platform.release()} ({
            platform.machine()})"

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stats = self._calculate_test_stats()
        total_duration = sum(r.get('duration', 0.0)
                             for r in self.test_results.values())

        return f"""
        <div class="comprehensive-section">
            <div class="section-title">🌍 Environment Details</div>
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Python Version:</div>
                    <div class="info-value">{python_version}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Pytest Version:</div>
                    <div class="info-value">{pytest_version}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Platform:</div>
                    <div class="info-value">{platform_info}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Test Runner:</div>
                    <div class="info-value">{self.config.branding.company_name}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Test Start Time:</div>
                    <div class="info-value">{current_time}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Total Duration:</div>
                    <div class="info-value">{total_duration:.2f} seconds</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Report Generated:</div>
                    <div class="info-value">{current_time}</div>
                </div>
            </div>
        </div>
        """

    def generate_summary_section(self) -> str:
        """Generate test execution summary with status cards and charts."""
        stats = self._calculate_test_stats()

        return f"""
        <div class="comprehensive-section">
            <div class="section-title">📊 Test Execution Summary</div>
            <div class="status-dashboard">
                <div class="status-card status-total">
                    <div style="font-size: 24px;">📝 {stats['total']}</div>
                    <div>Total Tests</div>
                </div>
                <div class="status-card status-passed">
                    <div style="font-size: 24px;">✅ {stats['passed']}</div>
                    <div>Passed</div>
                </div>
                <div class="status-card status-failed">
                    <div style="font-size: 24px;">❌ {stats['failed']}</div>
                    <div>Failed</div>
                </div>
                <div class="status-card status-skipped">
                    <div style="font-size: 24px;">⏭️ {stats['skipped']}</div>
                    <div>Skipped</div>
                </div>
            </div>

            <div class="chart-container">
                <div class="chart-wrapper">
                    <canvas id="statusChart"></canvas>
                </div>
                <div class="chart-wrapper">
                    <canvas id="passRateChart"></canvas>
                </div>
            </div>
        </div>
    </div>
        """

    def generate_error_analysis_section(self) -> str:
        """Generate ERROR ANALYSIS & INSIGHTS section."""
        failed_tests = {
            tid: result for tid,
            result in self.test_results.items() if result.get('outcome') == 'failed'}

        if not failed_tests:
            return ""

        error_insights = []
        for test_id, result in failed_tests.items():
            if self.error_reporter:
                error_list = self.error_reporter.get_test_errors(test_id)
                if error_list:
                    error_data = error_list[0]
                    error_insights.append(f"""
                        <div class="error-insight-item">
                            <div class="error-insight-header">
                                <span class="error-test-name">🔴 {test_id}</span>
                                <span class="error-badge">{error_data.error_category}</span>
                            </div>
                            <div class="error-insight-body">
                                <p><strong>Error Type:</strong> {error_data.error_type}</p>
                                <p><strong>Message:</strong> {error_data.error_message[:200] if error_data.error_message else 'N/A'}</p>
                                <p class="suggested-action"><strong>💡 Suggested Action:</strong> {error_data.suggested_action or 'Review test logs for details'}</p>
                            </div>
                        </div>
                    """)

        return f"""
        <div class="comprehensive-section error-analysis-section">
            <div class="section-header">
                <h3>🚨 ERROR ANALYSIS & INSIGHTS</h3>
            </div>
            <div class="error-insights-container">
                {''.join(error_insights)}
            </div>
        </div>
        """

    def generate_test_steps_section(self) -> str:
        """Generate Detailed Step Execution Results section with enhanced formatting."""
        # Count test steps from results
        total_steps = len(self.test_results)
        passed_steps = sum(1 for r in self.test_results.values()
                           if r.get('outcome') == 'passed')
        failed_steps = sum(1 for r in self.test_results.values()
                           if r.get('outcome') == 'failed')
        skipped_steps = sum(
            1 for r in self.test_results.values() if r.get('outcome') == 'skipped')

        # Calculate percentages for the donut chart
        pass_percentage = (
            passed_steps /
            total_steps *
            100) if total_steps > 0 else 0
        fail_percentage = (
            failed_steps /
            total_steps *
            100) if total_steps > 0 else 0

        step_rows = []
        step_number = 1
        for test_id, result in self.test_results.items():
            outcome = result.get('outcome', 'unknown')
            duration = result.get('duration', 0.0)

            # Extract just the test name from the full path
            test_name = test_id.split('::')[-1] if '::' in test_id else test_id

            # Extract test case ID (class name)
            test_case = 'TC-1000'  # Default
            if '::' in test_id:
                parts = test_id.split('::')
                if len(parts) >= 2:
                    test_case = parts[1] if parts[1].startswith(
                        'Test') else 'TC-1000'

            status_badge = '<span class="status-badge status-pass">PASS</span>' if outcome == 'passed' else \
                '<span class="status-badge status-fail">FAIL</span>' if outcome == 'failed' else \
                '<span class="status-badge status-skip">SKIP</span>'

            status_class = outcome.lower()

            # Get error details if failed
            error_details = 'N/A'
            if outcome == 'failed' and self.error_reporter:
                error_list = self.error_reporter.get_test_errors(test_id)
                if error_list:
                    error_data = error_list[0]
                    error_details = f'{
                        error_data.error_type}: {
                        error_data.error_message[
                            :50]}...' if error_data.error_message else 'AssertionError'

            step_rows.append(f"""
                <tr class="step-row-{status_class}">
                    <td style="text-align: center; font-weight: 600;">{test_case}</td>
                    <td style="text-align: left; padding-left: 15px;">{step_number}. {test_name}</td>
                    <td style="text-align: center;">{status_badge}</td>
                    <td style="text-align: center; color: #999;">N/A</td>
                    <td style="text-align: left; color: #d32f2f; font-size: 12px;">{error_details}</td>
                </tr>
            """)
            step_number += 1

        return f"""
        <div class="comprehensive-section test-steps-section" style="background: #f8f9fa; border-left: 5px solid #2196F3;">
            <div class="section-header" style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
                <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #42a5f5, #1976d2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-size: 20px;">
                    📊
                </div>
                <h3 style="margin: 0; color: #1976d2; font-size: 18px;">Detailed Step Execution Results</h3>
            </div>

            <div style="display: flex; gap: 20px; margin-bottom: 20px;">
                <div style="flex: 1;">
                    <div style="background: #e3f2fd; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
                        <p style="margin: 0; color: #1976d2; font-size: 13px;">
                            <strong>📋 Overview:</strong> This section provides comprehensive details for each individual test step across all test cases.
                            Use the interactive features to explore step execution patterns and identify potential issues.
                        </p>
                    </div>
                    <div style="background: white; padding: 12px; border-radius: 6px; border-left: 3px solid #42a5f5;">
                        <p style="margin: 0; color: #666; font-size: 12px;">
                            <strong style="color: #1976d2;">[TIP]</strong> Click headers to sort &nbsp;
                            <strong style="color: #1976d2;">🔍</strong> Hover for tooltips &nbsp;
                            <strong style="color: #1976d2;">📊</strong> Interactive charts
                        </p>
                    </div>
                </div>
                <div style="width: 250px;">
                    <div style="text-align: center; margin-bottom: 10px;">
                        <h4 style="margin: 0 0 10px 0; color: #666; font-size: 14px;">Step Status Overview</h4>
                    </div>
                    <div style="position: relative; width: 200px; height: 200px; margin: 0 auto;">
                        <canvas id="stepStatusChart"></canvas>
                    </div>
                </div>
            </div>

            <div class="test-steps-table-container" style="background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <table class="test-steps-table" style="width: 100%; border-collapse: collapse;">
                    <thead>
                        <tr style="background: linear-gradient(135deg, #1976d2, #1565c0);">
                            <th class="sortable-header" onclick="sortStepsTable(0)" style="padding: 12px; text-align: center; color: white; font-weight: 600; border-right: 1px solid rgba(255,255,255,0.2); cursor: pointer;">
                                🎯 Test Case
                            </th>
                            <th class="sortable-header" onclick="sortStepsTable(1)" style="padding: 12px; text-align: left; color: white; font-weight: 600; border-right: 1px solid rgba(255,255,255,0.2); cursor: pointer;">
                                📝 Step Name
                            </th>
                            <th class="sortable-header" onclick="sortStepsTable(2)" style="padding: 12px; text-align: center; color: white; font-weight: 600; border-right: 1px solid rgba(255,255,255,0.2); cursor: pointer;">
                                ⚡ Status
                            </th>
                            <th style="padding: 12px; text-align: center; color: white; font-weight: 600; border-right: 1px solid rgba(255,255,255,0.2);">
                                📷 Screenshot
                            </th>
                            <th style="padding: 12px; text-align: left; color: white; font-weight: 600;">
                                ⚠️ Error Details
                            </th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(step_rows)}
                    </tbody>
                </table>
            </div>
        </div>
        """

    def generate_comprehensive_test_table(self) -> str:
        """Generate comprehensive test results table with enhanced styling."""
        if not self.config.report.enable_comprehensive_table:
            return ""

        table_rows = []
        test_number = 1

        for test_id, result in self.test_results.items():
            outcome = result.get('outcome', 'unknown')
            duration = result.get('duration', 0.0)

            # Get error information if test failed
            error_category = "N/A"
            error_details = ""
            suggested_action = ""
            error_popup_html = ""

            if outcome == 'failed' and self.error_reporter:
                error_list = self.error_reporter.get_test_errors(test_id)
                if error_list and len(error_list) > 0:
                    error_data = error_list[0]
                    error_category = error_data.error_category
                    error_message = error_data.error_message or ""
                    suggested_action = error_data.suggested_action or ""
                    stack_trace = error_data.stack_trace or ""

                    # Create error popup HTML
                    error_popup_html = f'''
                        <div class="error-details-popup" id="error-{test_number}">
                            <h5>🚫 Error Details</h5>
                            <table class="error-info-table">
                                <tr><td><strong>Type:</strong></td><td>{error_data.error_type}</td></tr>
                                <tr><td><strong>Category:</strong></td><td>{error_category}</td></tr>
                                <tr><td><strong>Message:</strong></td><td>{error_message[:200]}</td></tr>
                                <tr><td><strong>Suggested Action:</strong></td><td class="suggested-action">{suggested_action}</td></tr>
                            </table>
                            {f'<div class="stack-trace"><h6>Stack Trace:</h6><pre>{stack_trace[:500]}</pre></div>' if stack_trace else ''}
                        </div>
                    '''

                    # Truncate for display
                    max_length = self.config.report.max_error_message_length
                    if len(error_message) > max_length:
                        error_details = error_message[:max_length] + "..."
                    else:
                        error_details = error_message

                    if suggested_action:
                        error_details += f'<br/><span class="suggested-action">💡 {suggested_action[:80]}</span>'

            # Row styling based on result
            row_class = f"test-row-{outcome.lower()}"
            result_class = f"result-{outcome.lower()}"

            # Format timestamps
            current_time = datetime.now()
            start_time = current_time.strftime("%H:%M:%S")
            end_time = (current_time).strftime("%H:%M:%S")

            table_rows.append(f"""
                <tr class="{row_class}">
                    <td class="col-sno">{test_number}</td>
                    <td class="col-name">{test_id}</td>
                    <td class="col-start-time">{start_time}</td>
                    <td class="col-end-time">{end_time}</td>
                    <td class="col-duration">{duration:.3f}s</td>
                    <td class="col-result {outcome.lower()}"><span class="{result_class}">{outcome.upper()}</span></td>
                    <td class="col-error-category"><span class="error-category">{error_category}</span></td>
                    <td class="col-result-details">
                        {f'<div class="error-details-container"><button class="error-toggle-btn" onclick="toggleError({test_number}, event)">View Error</button>{error_popup_html}</div>' if outcome == 'failed' else error_details}
                    </td>
                </tr>
            """)
            test_number += 1

        return f"""
        <div class="comprehensive-section">
            <div class="section-header">
                <h3>📊 COMPREHENSIVE TEST RESULTS</h3>
            </div>
            <div class="table-controls">
                <div class="filter-group">
                    <label>🔍 Search:</label>
                    <input type="text" id="testSearchInput" class="filter-input" placeholder="Search by test name..." onkeyup="filterTests()">
                </div>
                <div class="filter-group">
                    <label>📊 Status:</label>
                    <select id="statusFilter" class="filter-select" onchange="filterTests()">
                        <option value="all">All</option>
                        <option value="passed">Passed</option>
                        <option value="failed">Failed</option>
                        <option value="skipped">Skipped</option>
                    </select>
                </div>
                <div class="filter-group">
                    <label>⚠️ Error Category:</label>
                    <select id="categoryFilter" class="filter-select" onchange="filterTests()">
                        <option value="all">All</option>
                        <option value="assertion">Assertion</option>
                        <option value="runtime">Runtime</option>
                        <option value="setup">Setup/Teardown</option>
                    </select>
                </div>
                <button class="clear-filters-btn" onclick="clearFilters()">🔄 Clear Filters</button>
            </div>
            <div class="test-table-container">
                <table class="comprehensive-test-table" id="comprehensiveTestTable">
                    <thead>
                        <tr>
                            <th class="col-sno sortable-header" onclick="sortTable(0)">S.No</th>
                            <th class="col-name sortable-header" onclick="sortTable(1)">Test Case</th>
                            <th class="col-start-time sortable-header" onclick="sortTable(2)">Start Time</th>
                            <th class="col-end-time sortable-header" onclick="sortTable(3)">End Time</th>
                            <th class="col-duration sortable-header" onclick="sortTable(4)">Duration</th>
                            <th class="col-result sortable-header" onclick="sortTable(5)">Result</th>
                            <th class="col-error-category sortable-header" onclick="sortTable(6)">Error Category</th>
                            <th class="col-result-details">Result Details</th>
                        </tr>
                    </thead>
                    <tbody>
                        {''.join(table_rows)}
                    </tbody>
                </table>
            </div>
        </div>
        """

    def generate_chartjs_script(self) -> str:
        """Generate Chart.js visualization scripts for dashboard."""
        if not self.config.charts.enable_charts:
            return ""

        stats = self._calculate_test_stats()

        return f"""
        <script>
        // Error toggle functionality
        function toggleError(id, event) {{
            if (event) {{
                event.stopPropagation();
            }}
            const popup = document.getElementById('error-' + id);
            if (!popup) {{
                console.error('Error popup not found:', 'error-' + id);
                return;
            }}
            if (popup.style.display === 'none' || popup.style.display === '') {{
                // Hide all other popups
                document.querySelectorAll('.error-details-popup').forEach(p => p.style.display = 'none');
                popup.style.display = 'block';
            }} else {{
                popup.style.display = 'none';
            }}
        }}

        // Close popups when clicking outside
        document.addEventListener('click', function(event) {{
            if (!event.target.classList.contains('error-toggle-btn')) {{
                document.querySelectorAll('.error-details-popup').forEach(p => p.style.display = 'none');
            }}
        }});

        // Filter and Sort Functions
        function filterTests() {{
            try {{
                const searchInput = document.getElementById('testSearchInput').value.toLowerCase();
                const statusFilter = document.getElementById('statusFilter').value;
                const categoryFilter = document.getElementById('categoryFilter').value;
                const table = document.getElementById('comprehensiveTestTable');
                if (!table) {{
                    console.error('Table not found: comprehensiveTestTable');
                    return;
                }}
                const tbody = table.getElementsByTagName('tbody')[0];
                if (!tbody) {{
                    console.error('Table body not found');
                    return;
                }}
                const rows = tbody.getElementsByTagName('tr');

                console.log('Filter called - Status:', statusFilter, 'Category:', categoryFilter, 'Search:', searchInput);

            for (let i = 0; i < rows.length; i++) {{
                const row = rows[i];
                if (!row.cells || row.cells.length < 7) continue; // Skip rows without enough cells

                const testName = row.cells[1].textContent.toLowerCase();
                const status = row.classList.contains('test-row-passed') ? 'passed' :
                              row.classList.contains('test-row-failed') ? 'failed' :
                              row.classList.contains('test-row-skipped') ? 'skipped' : '';
                const category = row.cells[6].textContent.toLowerCase();

                let show = true;

                // Search filter
                if (searchInput && !testName.includes(searchInput)) {{
                    show = false;
                }}

                // Status filter
                if (statusFilter !== 'all' && status !== statusFilter) {{
                    show = false;
                }}

                // Category filter
                if (categoryFilter !== 'all' && !category.includes(categoryFilter)) {{
                    show = false;
                }}

                row.style.display = show ? '' : 'none';
            }}
            }} catch (error) {{
                console.error('Error in filterTests:', error);
            }}
        }}

        function clearFilters() {{
            document.getElementById('testSearchInput').value = '';
            document.getElementById('statusFilter').value = 'all';
            document.getElementById('categoryFilter').value = 'all';
            filterTests();
        }}

        function sortTable(columnIndex) {{
            const table = document.getElementById('comprehensiveTestTable');
            const tbody = table.getElementsByTagName('tbody')[0];
            const rows = Array.from(tbody.getElementsByTagName('tr'));
            const header = table.getElementsByTagName('th')[columnIndex];

            // Toggle sort direction
            const isAsc = header.classList.contains('sort-asc');

            // Remove sort classes from all headers
            table.querySelectorAll('th').forEach(th => {{
                th.classList.remove('sort-asc', 'sort-desc');
            }});

            // Add sort class to current header
            header.classList.add(isAsc ? 'sort-desc' : 'sort-asc');

            // Sort rows
            rows.sort((a, b) => {{
                let aValue = a.cells[columnIndex].textContent.trim();
                let bValue = b.cells[columnIndex].textContent.trim();

                // Handle numeric columns (S.No, Duration)
                if (columnIndex === 0 || columnIndex === 4) {{
                    aValue = parseFloat(aValue);
                    bValue = parseFloat(bValue);
                }}

                if (aValue < bValue) return isAsc ? 1 : -1;
                if (aValue > bValue) return isAsc ? -1 : 1;
                return 0;
            }});

            // Reorder rows in table
            rows.forEach(row => tbody.appendChild(row));
        }}

        function filterSteps() {{
            try {{
                const searchInput = document.getElementById('stepSearchInput').value.toLowerCase();
                const statusFilter = document.getElementById('stepStatusFilter').value;
                const table = document.getElementById('testStepsTable');
                if (!table) {{
                    console.error('Table not found: testStepsTable');
                    return;
                }}
                const tbody = table.getElementsByTagName('tbody')[0];
                if (!tbody) {{
                    console.error('Table body not found');
                    return;
                }}
                const rows = tbody.getElementsByTagName('tr');

            for (let i = 0; i < rows.length; i++) {{
                const row = rows[i];
                if (!row.cells || row.cells.length < 3) continue; // Skip rows without enough cells

                const stepName = row.cells[1].textContent.toLowerCase();
                const statusBadge = row.cells[2].querySelector('.status-badge');
                const status = statusBadge ? statusBadge.textContent.toLowerCase() : '';

                let show = true;

                // Search filter
                if (searchInput && !stepName.includes(searchInput)) {{
                    show = false;
                }}

                // Status filter
                if (statusFilter !== 'all' && !status.includes(statusFilter)) {{
                    show = false;
                }}

                row.style.display = show ? '' : 'none';
                }}
            }} catch (error) {{
                console.error('Error in filterSteps:', error);
            }}
        }}

        function clearStepFilters() {{
            document.getElementById('stepSearchInput').value = '';
            document.getElementById('stepStatusFilter').value = 'all';
            filterSteps();
        }}

        function sortStepsTable(columnIndex) {{
            const table = document.getElementById('testStepsTable');
            const tbody = table.getElementsByTagName('tbody')[0];
            const rows = Array.from(tbody.getElementsByTagName('tr'));
            const header = table.getElementsByTagName('th')[columnIndex];

            // Toggle sort direction
            const isAsc = header.classList.contains('sort-asc');

            // Remove sort classes from all headers
            table.querySelectorAll('th').forEach(th => {{
                th.classList.remove('sort-asc', 'sort-desc');
            }});

            // Add sort class to current header
            header.classList.add(isAsc ? 'sort-desc' : 'sort-asc');

            // Sort rows
            rows.sort((a, b) => {{
                let aValue = a.cells[columnIndex].textContent.trim();
                let bValue = b.cells[columnIndex].textContent.trim();

                if (aValue < bValue) return isAsc ? 1 : -1;
                if (aValue > bValue) return isAsc ? -1 : 1;
                return 0;
            }});

            // Reorder rows in table
            rows.forEach(row => tbody.appendChild(row));
        }}

        // Chart.js visualizations
        document.addEventListener('DOMContentLoaded', function() {{
            try {{
                Chart.defaults.font.family = "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif";
                Chart.defaults.color = '#64748b';

                // Register datalabels plugin if available
                if (typeof ChartDataLabels !== 'undefined') {{
                    Chart.register(ChartDataLabels);
                }}

                // Test Status Distribution Chart
                if (document.getElementById('statusChart')) {{
                    const statusCtx = document.getElementById('statusChart').getContext('2d');
                    new Chart(statusCtx, {{
                        type: 'doughnut',
                        data: {{
                            labels: ['Passed', 'Failed', 'Skipped'],
                            datasets: [{{
                                data: [{stats['passed']}, {stats['failed']}, {stats['skipped']}],
                                backgroundColor: [
                                    'rgba(76, 175, 80, 0.8)',
                                    'rgba(244, 67, 54, 0.8)',
                                    'rgba(255, 152, 0, 0.8)'
                                ],
                                borderColor: [
                                    'rgba(76, 175, 80, 1)',
                                    'rgba(244, 67, 54, 1)',
                                    'rgba(255, 152, 0, 1)'
                                ],
                                borderWidth: 2
                            }}]
                        }},
                        options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'bottom',
                                labels: {{
                                    padding: 20,
                                    font: {{ size: 13 }}
                                }}
                            }},
                            title: {{
                                display: true,
                                text: 'Test Status Distribution',
                                font: {{ size: 16, weight: 'bold' }}
                            }},
                            datalabels: {{
                                color: '#fff',
                                font: {{
                                    weight: 'bold',
                                    size: 14
                                }},
                                formatter: function(value, context) {{
                                    const total = {stats['total']};
                                    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                    return value + '\\n(' + percentage + '%)';
                                }}
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        const label = context.label || '';
                                        const value = context.parsed || 0;
                                        const total = {stats['total']};
                                        const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                            return label + ': ' + value + ' (' + percentage + '%)';
                                        }}
                                    }}
                                }}
                            }},
                            animation: {{
                                animateRotate: {str(self.config.charts.chart_animation).lower()},
                                animateScale: {str(self.config.charts.chart_animation).lower()}
                            }}
                        }}
                    }});
                }}

            // Step Status Overview Chart (for test steps section)
            if (document.getElementById('stepStatusChart')) {{
                const stepCtx = document.getElementById('stepStatusChart').getContext('2d');
                new Chart(stepCtx, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['Passed', 'Failed'],
                        datasets: [{{
                            data: [{stats['passed']}, {stats['failed']}],
                            backgroundColor: [
                                '#4caf50',
                                '#f44336'
                            ],
                            borderWidth: 0
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: true,
                        cutout: '70%',
                        plugins: {{
                            legend: {{
                                display: true,
                                position: 'bottom',
                                labels: {{
                                    font: {{ size: 11 }},
                                    padding: 10
                                }}
                            }},
                            title: {{
                                display: false
                            }},
                            datalabels: {{
                                display: true,
                                color: '#fff',
                                font: {{
                                    weight: 'bold',
                                    size: 16
                                }},
                                formatter: function(value) {{
                                    return value;
                                }}
                            }},
                            tooltip: {{
                                enabled: true
                            }}
                        }}
                    }},
                    plugins: [{{
                        id: 'centerText',
                        afterDraw: function(chart) {{
                            const ctx = chart.ctx;
                            const width = chart.width;
                            const height = chart.height;
                            const total = {stats['total']};
                            const passed = {stats['passed']};

                            ctx.restore();
                            const fontSize = (height / 80).toFixed(2);
                            ctx.font = 'bold ' + fontSize + 'em sans-serif';
                            ctx.textBaseline = 'middle';
                            ctx.fillStyle = '#4caf50';

                            const text = passed;
                            const textX = Math.round((width - ctx.measureText(text).width) / 2);
                            const textY = height / 2 - 10;

                            ctx.fillText(text, textX, textY);

                            ctx.font = fontSize * 0.4 + 'em sans-serif';
                            ctx.fillStyle = '#666';
                            const percentText = '(' + ((passed / total * 100).toFixed(0)) + '%)';
                            const percentX = Math.round((width - ctx.measureText(percentText).width) / 2);
                            ctx.fillText(percentText, percentX, textY + 20);

                            ctx.save();
                        }}
                    }}]
                }});
            }}

            // Pass/Fail/Skip & Error Rate Distribution Chart (Pie Chart)
            if (document.getElementById('passRateChart')) {{
                const passRate = {stats['pass_rate']:.1f};
                const failRate = {stats['failed']} > 0 ? (({stats['failed']} / {stats['total']}) * 100).toFixed(1) : 0;
                const skipRate = {stats['skipped']} > 0 ? (({stats['skipped']} / {stats['total']}) * 100).toFixed(1) : 0;
                const errorRate = 0; // Can be calculated based on error analysis
                const passRateCtx = document.getElementById('passRateChart').getContext('2d');

                new Chart(passRateCtx, {{
                    type: 'pie',
                    data: {{
                        labels: ['Passed', 'Failed', 'Skipped'],
                        datasets: [{{
                            data: [{stats['passed']}, {stats['failed']}, {stats['skipped']}],
                            backgroundColor: [
                                'rgba(76, 175, 80, 0.8)',
                                'rgba(244, 67, 54, 0.8)',
                                'rgba(255, 152, 0, 0.8)'
                            ],
                            borderColor: [
                                'rgba(76, 175, 80, 1)',
                                'rgba(244, 67, 54, 1)',
                                'rgba(255, 152, 0, 1)'
                            ],
                            borderWidth: 2
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{
                                position: 'bottom',
                                labels: {{
                                    padding: 20,
                                    font: {{ size: 13 }}
                                }}
                            }},
                            title: {{
                                display: true,
                                text: 'PASS / FAIL / SKIP & Error Rate Distribution',
                                font: {{ size: 16, weight: 'bold' }}
                            }},
                            datalabels: {{
                                color: '#fff',
                                font: {{
                                    weight: 'bold',
                                    size: 14
                                }},
                                formatter: function(value, context) {{
                                    const total = {stats['total']};
                                    const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                    return value + '\\n(' + percentage + '%)';
                                }}
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        const label = context.label || '';
                                        const value = context.parsed || 0;
                                        const total = {stats['total']};
                                        const percentage = total > 0 ? ((value / total) * 100).toFixed(1) : 0;
                                        return label + ': ' + value + ' (' + percentage + '%)';
                                    }}
                                }}
                            }}
                        }},
                        animation: {{ duration: {1000 if self.config.charts.chart_animation else 0} }}
                    }}
                }});
            }}
            }} catch (error) {{
                console.error('Error initializing charts:', error);
                console.log('Chart object available:', typeof Chart !== 'undefined');
                console.log('ChartDataLabels available:', typeof ChartDataLabels !== 'undefined');
            }}
        }});
        </script>
        """

    def _calculate_test_stats(self) -> Dict[str, Any]:
        """Calculate test statistics."""
        total = len(self.test_results)
        passed = sum(1 for r in self.test_results.values()
                     if r.get('outcome') == 'passed')
        failed = sum(1 for r in self.test_results.values()
                     if r.get('outcome') == 'failed')
        skipped = sum(1 for r in self.test_results.values()
                      if r.get('outcome') == 'skipped')

        pass_rate = (passed / total * 100) if total > 0 else 0
        fail_rate = (failed / total * 100) if total > 0 else 0
        skip_rate = (skipped / total * 100) if total > 0 else 0

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'skipped': skipped,
            'pass_rate': pass_rate,
            'fail_rate': fail_rate,
            'skip_rate': skip_rate
        }

    def generate_historical_trends_section(self) -> str:
        """Generate historical trends section showing test result trends over time (v1.2.0)."""
        if self.historical_data:
            # Real data from database
            trends = self.historical_data
            total_runs = trends.get('total_runs', 1)
            pass_rate_change = trends.get('pass_rate_change', 0.0)
            flaky_count = trends.get('flaky_tests', 0)
            avg_duration = trends.get('avg_duration', 0.0)
            
            pass_rate_display = f"+{pass_rate_change:.1f}%" if pass_rate_change > 0 else f"{pass_rate_change:.1f}%"
            pass_rate_color = "#4CAF50" if pass_rate_change >= 0 else "#f44336"
            
            return f"""
        <div class="comprehensive-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <div class="section-title" style="color: white;">📊 Historical Trends</div>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px;">
                    <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                        <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">📈 Pass Rate Trend</div>
                        <div style="font-size: 32px; font-weight: bold; color: {pass_rate_color};">{pass_rate_display}</div>
                        <div style="font-size: 12px; opacity: 0.8;">vs. last 7 days</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                        <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">🔄 Flaky Tests Detected</div>
                        <div style="font-size: 32px; font-weight: bold;">{flaky_count}</div>
                        <div style="font-size: 12px; opacity: 0.8;">passed sometimes, failed others</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                        <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">⚡ Avg Execution Time</div>
                        <div style="font-size: 32px; font-weight: bold;">{avg_duration:.2f}s</div>
                        <div style="font-size: 12px; opacity: 0.8;">average per test</div>
                    </div>
                    <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                        <div style="font-size: 14px; opacity: 0.9; margin-bottom: 8px;">📅 Total Runs Tracked</div>
                        <div style="font-size: 32px; font-weight: bold;">{total_runs}</div>
                        <div style="font-size: 12px; opacity: 0.8;">test execution runs</div>
                    </div>
                </div>
            </div>
        </div>
        """
        else:
            # Placeholder when no historical data
            return """
        <div class="comprehensive-section" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <div class="section-title" style="color: white;">📊 Historical Trends</div>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                <div style="text-align: center; padding: 40px 20px;">
                    <div style="font-size: 48px; margin-bottom: 15px;">📈</div>
                    <div style="font-size: 20px; font-weight: bold; margin-bottom: 10px;">Historical Tracking Enabled</div>
                    <div style="font-size: 14px; opacity: 0.9; line-height: 1.6;">
                        Test results are being saved to <code style="background: rgba(255,255,255,0.2); padding: 2px 6px; border-radius: 3px;">test-history.db</code><br>
                        Run tests multiple times to see trends, flaky test detection, and performance metrics.
                    </div>
                </div>
            </div>
        </div>
        """

    def generate_ai_error_insights_section(self) -> str:
        """Generate AI-powered error analysis section (v1.2.0)."""
        if self.ai_insights and len(self.ai_insights) > 0:
            # Real AI insights
            insights_html = []
            for insight in self.ai_insights[:3]:  # Show top 3
                pattern = insight.get('pattern', 'Error Pattern')
                count = insight.get('count', 0)
                suggestion = insight.get('suggestion', 'Review the error details')
                quick_fix = insight.get('quick_fix', 'Check documentation')
                
                insights_html.append(f"""
                    <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                            <span style="font-size: 24px;">🎯</span>
                            <div>
                                <div style="font-weight: bold; font-size: 16px;">{pattern}</div>
                                <div style="font-size: 12px; opacity: 0.8;">Found in {count} test(s)</div>
                            </div>
                        </div>
                        <div style="font-size: 14px; line-height: 1.6;">
                            <strong>AI Suggestion:</strong> {suggestion}
                        </div>
                        <div style="margin-top: 10px; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; font-size: 13px;">
                            <strong>Quick Fix:</strong> {quick_fix}
                        </div>
                    </div>
                """)
            
            return f"""
        <div class="comprehensive-section" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
            <div class="section-title" style="color: white;">🤖 AI Error Analysis</div>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                <div style="display: grid; gap: 15px;">
                    {''.join(insights_html)}
                </div>
            </div>
        </div>
        """
        else:
            # Pattern-based analysis (local, no API needed)
            failed_tests = [r for r in self.test_results.values() if r.get('failed')]
            failed_count = len(failed_tests)
            
            if failed_count == 0:
                return """
        <div class="comprehensive-section" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
            <div class="section-title" style="color: white;">🤖 AI Error Analysis</div>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                <div style="text-align: center; padding: 40px 20px;">
                    <div style="font-size: 48px; margin-bottom: 15px;">✅</div>
                    <div style="font-size: 20px; font-weight: bold; margin-bottom: 10px;">All Tests Passed!</div>
                    <div style="font-size: 14px; opacity: 0.9;">No errors to analyze. Great job!</div>
                </div>
            </div>
        </div>
        """
            
            return f"""
        <div class="comprehensive-section" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
            <div class="section-title" style="color: white;">🤖 AI Error Analysis</div>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                <div style="display: grid; gap: 15px;">
                    <div style="background: rgba(255,255,255,0.15); padding: 15px; border-radius: 8px;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 10px;">
                            <span style="font-size: 24px;">🎯</span>
                            <div>
                                <div style="font-weight: bold; font-size: 16px;">Pattern-Based Analysis</div>
                                <div style="font-size: 12px; opacity: 0.8;">Analyzing {failed_count} failed test(s)</div>
                            </div>
                        </div>
                        <div style="font-size: 14px; line-height: 1.6;">
                            <strong>Analysis:</strong> Error patterns detected in test failures. 
                            For AI-powered suggestions with OpenAI/Claude, configure API keys in your settings.
                        </div>
                        <div style="margin-top: 10px; padding: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; font-size: 13px;">
                            <strong>Quick Fix:</strong> Review the Error Analysis section below for detailed error classifications and suggested actions.
                        </div>
                    </div>
                    <div style="margin-top: 10px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; border-left: 4px solid #ffd700;">
                        <strong>🔌 Enable AI Analysis:</strong> Set <code>ai.enable_ai_analysis: true</code> and configure 
                        <code>ai.provider</code> and <code>ai.api_key</code> in pytest_html_dashboard.yaml for enhanced AI insights.
                    </div>
                </div>
            </div>
        </div>
        """

    def generate_realtime_status_section(self) -> str:
        """Generate real-time dashboard status section (v1.2.0)."""
        return """
        <div class="comprehensive-section" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
            <div class="section-title" style="color: white;">⚡ Real-Time Dashboard (New in v1.2.0)</div>
            <div style="background: rgba(255,255,255,0.1); padding: 20px; border-radius: 10px; margin-top: 15px;">
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px;">
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 48px; margin-bottom: 10px;">📊</div>
                        <div style="font-size: 16px; font-weight: bold;">Live Updates</div>
                        <div style="font-size: 13px; opacity: 0.8;">WebSocket connection ready</div>
                    </div>
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 48px; margin-bottom: 10px;">🔔</div>
                        <div style="font-size: 16px; font-weight: bold;">Notifications</div>
                        <div style="font-size: 13px; opacity: 0.8;">Browser alerts enabled</div>
                    </div>
                    <div style="text-align: center; padding: 15px;">
                        <div style="font-size: 48px; margin-bottom: 10px;">⏱️</div>
                        <div style="font-size: 16px; font-weight: bold;">Test Progress</div>
                        <div style="font-size: 13px; opacity: 0.8;">100% Complete</div>
                    </div>
                </div>
                <div style="margin-top: 20px; padding: 15px; background: rgba(255,255,255,0.1); border-radius: 8px; border-left: 4px solid #ffd700;">
                    <strong>🚀 To Enable:</strong> Run pytest with <code>--realtime-dashboard</code> flag to start WebSocket server.
                    Watch tests execute live in your browser at <code>http://localhost:8765</code> while tests are running!
                </div>
                <div style="margin-top: 10px; padding: 15px; background: rgba(255,255,255,0.15); border-radius: 8px;">
                    <div style="font-size: 14px; margin-bottom: 8px;"><strong>Current Session:</strong></div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; font-size: 13px;">
                        <div>Started: <strong>{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</strong></div>
                        <div>Duration: <strong>2.48 seconds</strong></div>
                        <div>Mode: <strong>Post-execution view</strong></div>
                        <div>Updates: <strong>Static report</strong></div>
                    </div>
                </div>
            </div>
        </div>
        """

    def generate_enhanced_html(self) -> str:
        """Generate complete enhanced HTML content with dashboard styling."""
        html_parts = []

        # Add CSS
        html_parts.append(self.generate_dashboard_css())

        # Add header
        html_parts.append(self.generate_dashboard_header())

        # Add test configuration
        html_parts.append(self.generate_test_configuration_section())

        # Add environment details
        html_parts.append(self.generate_environment_section())

        # Add summary with charts
        html_parts.append(self.generate_summary_section())

        # 🆕 AI Error Analysis section (v1.2.0) - Works without database
        if self.config.ai.enable_ai_analysis:
            html_parts.append(self.generate_ai_error_insights_section())

        # Add ERROR ANALYSIS section
        html_parts.append(self.generate_error_analysis_section())

        # Add comprehensive test table (BEFORE Test Steps)
        html_parts.append(self.generate_comprehensive_test_table())

        # Add Test Step Execution section (AFTER Comprehensive Results)
        html_parts.append(self.generate_test_steps_section())

        # 🆕 Historical Trends section (v1.2.0) - MOVED TO END, requires database
        if self.config.historical.enable_tracking:
            html_parts.append(self.generate_historical_trends_section())

        # Add Chart.js script
        html_parts.append(self.generate_chartjs_script())

        return '\n'.join(html_parts)


def enhance_html_report_dashboard(
        html_path: str, config, test_results: Dict[str, Any], error_reporter):
    """Generate standalone dashboard-style HTML report (replacing pytest-html default)."""
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML report not found: {html_path}")

    # Collect AI insights if enabled
    ai_insights = None
    if config.ai.enable_ai_analysis:
        try:
            from .ai_analyzer import AIErrorAnalyzer
            analyzer = AIErrorAnalyzer(config.ai)
            
            # Collect failed tests
            failures = [
                {
                    'test_id': test_id,
                    'error_info': error_reporter.get_error_info(test_id)
                }
                for test_id, result in test_results.items()
                if result.get('failed', False)
            ]
            
            if failures:
                ai_insights = analyzer.analyze_errors(failures)
        except Exception as e:
            print(f"Warning: AI analysis failed: {e}")
            ai_insights = None

    # Collect historical data if enabled
    historical_data = None
    if config.historical.enable_tracking:
        try:
            from .history import TestHistory
            history = TestHistory(config.historical.database_path)
            historical_data = history.get_trends(days=7)
        except Exception as e:
            print(f"Warning: Failed to load historical data: {e}")
            historical_data = None

    # Generate complete standalone dashboard HTML
    generator = HTMLGeneratorDashboard(
        config, test_results, error_reporter, ai_insights, historical_data
    )
    dashboard_content = generator.generate_enhanced_html()

    # Create complete standalone HTML document
    standalone_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{config.branding.report_title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chartjs-plugin-datalabels@2.2.0/dist/chartjs-plugin-datalabels.min.js"></script>
</head>
<body>
    <div class="container">
        {dashboard_content}
    </div>
</body>
</html>
    """

    # Write standalone HTML
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(standalone_html)
