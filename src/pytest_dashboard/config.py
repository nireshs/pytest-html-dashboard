#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Configuration module for pytest-dashboard
Provides flexible configuration system for dashboard report customization
"""

import os
import yaml
from typing import Dict, Optional, Any
from dataclasses import dataclass, field, asdict


@dataclass
class BrandingConfig:
    """Branding configuration for report customization."""
    company_name: str = "Test Automation Framework"
    report_title: str = "Enhanced Test Execution Report"
    logo_url: Optional[str] = None  # Base64 encoded logo or URL
    primary_color: str = "#004488"
    secondary_color: str = "#0066CC"
    success_color: str = "#4CAF50"
    failure_color: str = "#f44336"
    warning_color: str = "#ff9800"

    def to_css_vars(self) -> str:
        """Convert colors to CSS variables."""
        return f"""
        :root {{
            --primary-color: {self.primary_color};
            --secondary-color: {self.secondary_color};
            --success-color: {self.success_color};
            --failure-color: {self.failure_color};
            --warning-color: {self.warning_color};
        }}
        """


@dataclass
class ChartConfig:
    """Chart configuration for report visualizations."""
    enable_charts: bool = True
    chart_height: int = 300
    show_pass_rate_chart: bool = True
    show_status_distribution_chart: bool = True
    chart_animation: bool = True


@dataclass
class ReportConfig:
    """Report behavior configuration."""
    enable_enhanced_reporting: bool = True
    enable_error_classification: bool = True
    enable_comprehensive_table: bool = True
    enable_test_steps: bool = True
    max_error_message_length: int = 100
    show_timestamps: bool = True
    show_duration: bool = True
    auto_refresh: bool = False
    refresh_interval: int = 30  # seconds


@dataclass
class ReporterConfig:
    """Main configuration class for pytest-dashboard."""
    branding: BrandingConfig = field(default_factory=BrandingConfig)
    charts: ChartConfig = field(default_factory=ChartConfig)
    report: ReportConfig = field(default_factory=ReportConfig)
    custom_css: Optional[str] = None
    custom_js: Optional[str] = None

    @classmethod
    def from_dict(cls, config_dict: Dict[str, Any]) -> 'ReporterConfig':
        """Create configuration from dictionary."""
        branding_dict = config_dict.get('branding', {})
        charts_dict = config_dict.get('charts', {})
        report_dict = config_dict.get('report', {})

        return cls(
            branding=BrandingConfig(**branding_dict),
            charts=ChartConfig(**charts_dict),
            report=ReportConfig(**report_dict),
            custom_css=config_dict.get('custom_css'),
            custom_js=config_dict.get('custom_js'),
        )

    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'ReporterConfig':
        """Load configuration from YAML file."""
        if not os.path.exists(yaml_path):
            return cls()  # Return default configuration

        try:
            with open(yaml_path, 'r', encoding='utf-8') as f:
                config_dict = yaml.safe_load(f) or {}
            return cls.from_dict(config_dict)
        except Exception as e:
            print(f"Warning: Failed to load configuration from {yaml_path}: {e}")
            return cls()  # Return default configuration

    @classmethod
    def from_pytest_config(cls, pytest_config) -> 'ReporterConfig':
        """Create configuration from pytest config object."""
        config_dict = {}

        # Extract branding options
        branding = {}
        if hasattr(pytest_config, 'option'):
            branding['company_name'] = getattr(pytest_config.option, 'dashboard_company_name',
                                              "Test Automation Framework")
            branding['report_title'] = getattr(pytest_config.option, 'dashboard_report_title',
                                              "Test Execution Dashboard")
            branding['logo_url'] = getattr(pytest_config.option, 'dashboard_logo_url', None)
            branding['primary_color'] = getattr(pytest_config.option, 'dashboard_primary_color',
                                               "#004488")
            branding['secondary_color'] = getattr(pytest_config.option, 'dashboard_secondary_color',
                                                 "#0066CC")

        # Extract chart options
        charts = {}
        if hasattr(pytest_config, 'option'):
            charts['enable_charts'] = getattr(pytest_config.option, 'dashboard_charts', True)
            charts['show_pass_rate_chart'] = getattr(pytest_config.option,
                                                     'dashboard_pass_rate_chart', True)
            charts['show_status_distribution_chart'] = getattr(pytest_config.option,
                                                               'dashboard_status_chart', True)

        # Extract report options
        report = {}
        if hasattr(pytest_config, 'option'):
            report['enable_enhanced_reporting'] = getattr(pytest_config.option,
                                                         'dashboard_reporting', True)
            report['enable_error_classification'] = getattr(pytest_config.option,
                                                           'dashboard_error_classification', True)
            report['enable_comprehensive_table'] = getattr(pytest_config.option,
                                                          'dashboard_comprehensive_table', True)        config_dict['branding'] = branding
        config_dict['charts'] = charts
        config_dict['report'] = report

        return cls.from_dict(config_dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return asdict(self)

    def to_yaml(self, output_path: str):
        """Save configuration to YAML file."""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.to_dict(), f, default_flow_style=False, sort_keys=False)
            print(f"Configuration saved to {output_path}")
        except Exception as e:
            print(f"Error saving configuration to {output_path}: {e}")


def create_default_config_file(output_path: str = "pytest_dashboard.yaml"):
    """Create a default configuration file for reference."""
    config = ReporterConfig()
    config.to_yaml(output_path)

    # Add comments to the YAML file
    try:
        with open(output_path, 'r', encoding='utf-8') as f:
            content = f.read()

        commented_content = """# pytest-dashboard Configuration File
# This file contains all available configuration options for customizing your test dashboard reports

# Branding Configuration
# Customize the look and feel of your dashboard
""" + content        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(commented_content)

        print(f"Default configuration file created: {output_path}")
    except Exception as e:
        print(f"Warning: Could not add comments to configuration file: {e}")


if __name__ == "__main__":
    # Generate default configuration file
    create_default_config_file()
