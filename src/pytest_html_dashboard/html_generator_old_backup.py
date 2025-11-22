#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
HTML generation and enhancement for pytest-html-dashboard
Provides Chart.js integration, modern styling, and enhanced visualizations
"""

import os
import re
from typing import Dict, Any, List, Optional
from datetime import datetime


class HTMLGenerator:
    """Generates enhanced HTML content for pytest reports."""

    def __init__(self, config, test_results: Dict[str, Any], error_reporter):
        """Initialize HTML generator with configuration and test data."""
        self.config = config
        self.test_results = test_results
        self.error_reporter = error_reporter

    def generate_custom_css(self) -> str:
        """Generate custom CSS with branding colors."""
        branding = self.config.branding
        return f"""
        <style>
        {branding.to_css_vars()}

        /* Modern Dashboard Styling */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #f5f7fa;
            color: #2c3e50;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }}

        .dashboard-header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}

        .dashboard-header h1 {{
            margin: 0;
            font-size: 2rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .dashboard-logo {{
            max-height: 50px;
            max-width: 150px;
        }}

        .dashboard-summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            padding: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .summary-card {{
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .summary-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
        }}

        .summary-card-header {{
            font-size: 0.875rem;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }}

        .summary-card-value {{
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }}

        .summary-card-footer {{
            font-size: 0.875rem;
            color: #94a3b8;
            margin-top: 0.5rem;
        }}

        .summary-card.passed .summary-card-value {{
            color: var(--success-color);
        }}

        .summary-card.failed .summary-card-value {{
            color: var(--failure-color);
        }}

        .summary-card.skipped .summary-card-value {{
            color: var(--warning-color);
        }}

        .summary-card.total .summary-card-value {{
            color: var(--primary-color);
        }}

        .chart-container {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin: 1.5rem 2rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            max-width: 1400px;
            margin-left: auto;
            margin-right: auto;
        }}

        .chart-title {{
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            color: #1e293b;
        }}

        .chart-wrapper {{
            position: relative;
            height: {self.config.charts.chart_height}px;
            margin-bottom: 2rem;
        }}

        .charts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
            padding: 0 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }}

        .comprehensive-table-container {{
            background: white;
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            overflow-x: auto;
            max-width: 1400px;
            margin-left: auto;
            margin-right: auto;
        }}

        .comprehensive-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 0.9rem;
        }}

        .comprehensive-table thead {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
        }}

        .comprehensive-table th {{
            padding: 1rem;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.75rem;
            letter-spacing: 0.05em;
        }}

        .comprehensive-table td {{
            padding: 0.875rem 1rem;
            border-bottom: 1px solid #e2e8f0;
        }}

        .comprehensive-table tbody tr:hover {{
            background: #f8fafc;
        }}

        .status-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }}

        .status-badge.passed {{
            background: #dcfce7;
            color: #166534;
        }}

        .status-badge.failed {{
            background: #fee2e2;
            color: #991b1b;
        }}

        .status-badge.skipped {{
            background: #fef3c7;
            color: #92400e;
        }}

        .error-category {{
            display: inline-block;
            padding: 0.25rem 0.625rem;
            background: #f1f5f9;
            border-radius: 6px;
            font-size: 0.75rem;
            color: #475569;
            font-family: 'Monaco', 'Courier New', monospace;
        }}

        .error-message {{
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.8rem;
            color: #dc2626;
            background: #fef2f2;
            padding: 0.5rem;
            border-radius: 6px;
            border-left: 3px solid #dc2626;
            max-width: 500px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}

        .duration {{
            font-family: 'Monaco', 'Courier New', monospace;
            font-size: 0.85rem;
            color: #64748b;
        }}

        .section-header {{
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2rem 2rem 1rem;
            color: #1e293b;
            border-bottom: 2px solid var(--primary-color);
            padding-bottom: 0.5rem;
            max-width: 1400px;
            margin-left: auto;
            margin-right: auto;
        }}

        /* Responsive Design */
        @media (max-width: 768px) {{
            .dashboard-summary {{
                grid-template-columns: 1fr;
                padding: 1rem;
            }}

            .charts-grid {{
                grid-template-columns: 1fr;
                padding: 0 1rem;
            }}

            .comprehensive-table-container {{
                margin: 1rem;
                padding: 1rem;
            }}

            .chart-wrapper {{
                height: 250px;
            }}
        }}

        /* Custom scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: #f1f5f9;
        }}

        ::-webkit-scrollbar-thumb {{
            background: #cbd5e1;
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: #94a3b8;
        }}

        /* Print styles */
        @media print {{
            .dashboard-header {{
                background: var(--primary-color) !important;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}

            .summary-card, .chart-container, .comprehensive-table-container {{
                box-shadow: none;
                page-break-inside: avoid;
            }}
        }}
        </style>
        """

    def generate_chartjs_script(self) -> str:
        """Generate Chart.js visualization scripts."""
        if not self.config.charts.enable_charts:
            return ""

        # Calculate test statistics
        stats = self._calculate_test_stats()

        return f"""
        <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            // Chart configuration
            Chart.defaults.font.family = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
            Chart.defaults.color = '#64748b';

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
                                    font: {{
                                        size: 13
                                    }}
                                }}
                            }},
                            title: {{
                                display: false
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

            // Pass Rate Trend Chart
            if (document.getElementById('passRateChart')) {{
                const passRate = {stats['pass_rate']:.1f};
                const passRateCtx = document.getElementById('passRateChart').getContext('2d');

                new Chart(passRateCtx, {{
                    type: 'bar',
                    data: {{
                        labels: ['Pass Rate'],
                        datasets: [{{
                            label: 'Passed',
                            data: [passRate],
                            backgroundColor: 'rgba(76, 175, 80, 0.8)',
                            borderColor: 'rgba(76, 175, 80, 1)',
                            borderWidth: 2
                        }}, {{
                            label: 'Failed',
                            data: [{100 - stats['pass_rate']:.1f}],
                            backgroundColor: 'rgba(244, 67, 54, 0.8)',
                            borderColor: 'rgba(244, 67, 54, 1)',
                            borderWidth: 2
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            y: {{
                                beginAtZero: true,
                                max: 100,
                                ticks: {{
                                    callback: function(value) {{
                                        return value + '%';
                                    }}
                                }},
                                grid: {{
                                    color: 'rgba(0, 0, 0, 0.05)'
                                }}
                            }},
                            x: {{
                                stacked: true,
                                grid: {{
                                    display: false
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                position: 'bottom',
                                labels: {{
                                    padding: 20,
                                    font: {{
                                        size: 13
                                    }}
                                }}
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return context.dataset.label + ': ' + context.parsed.y.toFixed(1) + '%';
                                    }}
                                }}
                            }}
                        }},
                        animation: {{
                            duration: {1000 if self.config.charts.chart_animation else 0}
                        }}
                    }}
                }});
            }}

            // Error Categories Chart
            if (document.getElementById('errorCategoriesChart')) {{
                const errorCategories = {self._get_error_categories_data()};
                const errorCtx = document.getElementById('errorCategoriesChart').getContext('2d');

                new Chart(errorCtx, {{
                    type: 'bar',
                    data: {{
                        labels: errorCategories.labels,
                        datasets: [{{
                            label: 'Error Count',
                            data: errorCategories.values,
                            backgroundColor: 'rgba(244, 67, 54, 0.8)',
                            borderColor: 'rgba(244, 67, 54, 1)',
                            borderWidth: 2
                        }}]
                    }},
                    options: {{
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {{
                            x: {{
                                beginAtZero: true,
                                ticks: {{
                                    precision: 0
                                }},
                                grid: {{
                                    color: 'rgba(0, 0, 0, 0.05)'
                                }}
                            }},
                            y: {{
                                grid: {{
                                    display: false
                                }}
                            }}
                        }},
                        plugins: {{
                            legend: {{
                                display: false
                            }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(context) {{
                                        return 'Count: ' + context.parsed.x;
                                    }}
                                }}
                            }}
                        }},
                        animation: {{
                            duration: {1000 if self.config.charts.chart_animation else 0}
                        }}
                    }}
                }});
            }}
        }});
        </script>
        """

    def generate_dashboard_header(self) -> str:
        """Generate dashboard header with branding."""
        branding = self.config.branding
        logo_html = ""

        if branding.logo_url:
            logo_html = f'<img src="{
                branding.logo_url}" alt="Logo" class="dashboard-logo" />'

        return f"""
        <div class="dashboard-header">
            <h1>
                {logo_html}
                <span>{branding.report_title}</span>
            </h1>
            <p style="margin: 0.5rem 0 0; opacity: 0.9;">{branding.company_name}</p>
        </div>
        """

    def generate_summary_cards(self) -> str:
        """Generate summary statistics cards."""
        stats = self._calculate_test_stats()

        return f"""
        <div class="dashboard-summary">
            <div class="summary-card total">
                <div class="summary-card-header">Total Tests</div>
                <div class="summary-card-value">{stats['total']}</div>
                <div class="summary-card-footer">All executed tests</div>
            </div>
            <div class="summary-card passed">
                <div class="summary-card-header">Passed</div>
                <div class="summary-card-value">{stats['passed']}</div>
                <div class="summary-card-footer">{stats['pass_rate']:.1f}% success rate</div>
            </div>
            <div class="summary-card failed">
                <div class="summary-card-header">Failed</div>
                <div class="summary-card-value">{stats['failed']}</div>
                <div class="summary-card-footer">{stats['fail_rate']:.1f}% failure rate</div>
            </div>
            <div class="summary-card skipped">
                <div class="summary-card-header">Skipped</div>
                <div class="summary-card-value">{stats['skipped']}</div>
                <div class="summary-card-footer">{stats['skip_rate']:.1f}% skipped</div>
            </div>
        </div>
        """

    def generate_charts_section(self) -> str:
        """Generate charts section with Chart.js visualizations."""
        if not self.config.charts.enable_charts:
            return ""

        charts_html = '<h2 class="section-header">📊 Test Analytics</h2>'
        charts_html += '<div class="charts-grid">'

        if self.config.charts.show_status_distribution_chart:
            charts_html += """
            <div class="chart-container">
                <div class="chart-title">Test Status Distribution</div>
                <div class="chart-wrapper">
                    <canvas id="statusChart"></canvas>
                </div>
            </div>
            """

        if self.config.charts.show_pass_rate_chart:
            charts_html += """
            <div class="chart-container">
                <div class="chart-title">Pass Rate Analysis</div>
                <div class="chart-wrapper">
                    <canvas id="passRateChart"></canvas>
                </div>
            </div>
            """

        # Add error categories chart if there are failures
        stats = self._calculate_test_stats()
        if stats['failed'] > 0:
            charts_html += """
            <div class="chart-container" style="grid-column: span 2;">
                <div class="chart-title">Error Categories Breakdown</div>
                <div class="chart-wrapper">
                    <canvas id="errorCategoriesChart"></canvas>
                </div>
            </div>
            """

        charts_html += '</div>'
        return charts_html

    def generate_comprehensive_test_table(self) -> str:
        """Generate comprehensive test results table."""
        if not self.config.report.enable_comprehensive_table:
            return ""

        table_rows = []

        for test_id, result in self.test_results.items():
            outcome = result.get('outcome', 'unknown')
            duration = result.get('duration', 0.0)

            # Get error information if test failed
            error_info = ""
            error_category = "N/A"
            suggested_action = ""

            if outcome == 'failed' and self.error_reporter:
                error_list = self.error_reporter.get_test_errors(test_id)
                if error_list and len(error_list) > 0:
                    error_data = error_list[0]  # Get first error
                    error_category = error_data.error_category
                    error_message = error_data.error_message or ""
                    suggested_action = error_data.suggested_action or ""

                    # Truncate long error messages
                    max_length = self.config.report.max_error_message_length
                    if len(error_message) > max_length:
                        error_message = error_message[:max_length] + "..."

                    error_info = f'<div class="error-message" title="{error_message}">{error_message}</div>'
                    if suggested_action:
                        error_info += f'<div style="font-size: 0.75rem; color: #64748b; margin-top: 0.25rem;">💡 {suggested_action}</div>'

            status_class = outcome.lower()
            table_rows.append(f"""
            <tr>
                <td>{test_id}</td>
                <td><span class="status-badge {status_class}">{outcome.upper()}</span></td>
                <td><span class="duration">{duration:.3f}s</span></td>
                <td><span class="error-category">{error_category}</span></td>
                <td>{error_info}</td>
            </tr>
            """)

        return f"""
        <h2 class="section-header">📋 Detailed Test Results</h2>
        <div class="comprehensive-table-container">
            <table class="comprehensive-table">
                <thead>
                    <tr>
                        <th>Test Case</th>
                        <th>Status</th>
                        <th>Duration</th>
                        <th>Error Category</th>
                        <th>Error Details</th>
                    </tr>
                </thead>
                <tbody>
                    {''.join(table_rows)}
                </tbody>
            </table>
        </div>
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

    def _get_error_categories_data(self) -> str:
        """Get error categories data for chart."""
        if not self.error_reporter:
            return "{ labels: [], values: [] }"

        categories = {}
        for test_id, result in self.test_results.items():
            if result.get('outcome') == 'failed':
                error_list = self.error_reporter.get_test_errors(test_id)
                if error_list and len(error_list) > 0:
                    error_data = error_list[0]  # Get first error
                    category = error_data.error_category
                    categories[category] = categories.get(category, 0) + 1

        labels = list(categories.keys())
        values = list(categories.values())

        return f"{{ labels: {labels}, values: {values} }}"

    def generate_enhanced_html(self) -> str:
        """Generate complete enhanced HTML content."""
        html_parts = []

        # Add custom CSS
        html_parts.append(self.generate_custom_css())

        # Add dashboard header
        html_parts.append(self.generate_dashboard_header())

        # Add summary cards
        html_parts.append(self.generate_summary_cards())

        # Add charts section
        html_parts.append(self.generate_charts_section())

        # Add comprehensive test table
        html_parts.append(self.generate_comprehensive_test_table())

        # Add Chart.js script
        html_parts.append(self.generate_chartjs_script())

        return '\n'.join(html_parts)


def enhance_html_report(html_path: str, config,
                        test_results: Dict[str, Any], error_reporter):
    """
    Enhance existing HTML report file with dashboard features.

    Args:
        html_path: Path to the HTML report file
        config: ReporterConfig instance
        test_results: Dictionary of test results
        error_reporter: EnhancedErrorReporter instance
    """
    if not os.path.exists(html_path):
        raise FileNotFoundError(f"HTML report not found: {html_path}")

    # Read existing HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Generate enhanced content
    generator = HTMLGenerator(config, test_results, error_reporter)
    enhanced_html = generator.generate_enhanced_html()

    # Find insertion point (before </body> tag)
    insertion_point = html_content.rfind('</body>')

    if insertion_point != -1:
        # Insert enhanced content before </body>
        enhanced_content = (
            html_content[:insertion_point] +
            enhanced_html +
            html_content[insertion_point:]
        )
    else:
        # If no </body> tag, append to end
        enhanced_content = html_content + enhanced_html

    # Write enhanced HTML back
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(enhanced_content)


def generate_standalone_report(
        output_path: str, config, test_results: Dict[str, Any], error_reporter):
    """
    Generate a standalone enhanced HTML report.

    Args:
        output_path: Path where the report should be saved
        config: ReporterConfig instance
        test_results: Dictionary of test results
        error_reporter: EnhancedErrorReporter instance
    """
    generator = HTMLGenerator(config, test_results, error_reporter)

    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{config.branding.report_title}</title>
        {generator.generate_custom_css()}
    </head>
    <body>
        {generator.generate_dashboard_header()}
        {generator.generate_summary_cards()}
        {generator.generate_charts_section()}
        {generator.generate_comprehensive_test_table()}
        {generator.generate_chartjs_script()}
    </body>
    </html>
    """

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
