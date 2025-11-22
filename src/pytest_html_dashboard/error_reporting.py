#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhanced Error Reporting Module for pytest-dashboard
Provides detailed error capture, classification, and reporting for test failures.
"""

import re
import traceback
import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict


@dataclass
class ErrorDetails:
    """Structured error information for comprehensive reporting."""
    error_type: str
    error_message: str
    error_category: str
    stack_trace: str
    test_step: Optional[str]
    timestamp: str
    suggested_action: str
    error_code: Optional[str] = None
    affected_component: Optional[str] = None


class ErrorClassifier:
    """Classify errors into categories for better analysis and resolution."""

    # Error pattern definitions (generic patterns applicable to any test framework)
    ERROR_PATTERNS = {
        'ASSERTION_FAILURE': [
            r'.*AssertionError.*',
            r'.*assert.*failed.*',
            r'.*expected.*but.*got.*',
            r'.*assertion.*error.*'
        ],
        'TIMEOUT_ERROR': [
            r'.*timeout.*',
            r'.*timed out.*',
            r'.*TimeoutException.*',
            r'.*connection.*timeout.*'
        ],
        'CONNECTION_ERROR': [
            r'.*connection.*error.*',
            r'.*connection.*refused.*',
            r'.*connection.*failed.*',
            r'.*cannot connect.*',
        ],
        'NETWORK_ERROR': [
            r'.*network.*error.*',
            r'.*host.*unreachable.*',
            r'.*dns.*resolution.*failed.*',
            r'.*socket.*error.*'
        ],
        'PERMISSION_ERROR': [
            r'.*permission.*denied.*',
            r'.*access.*denied.*',
            r'.*insufficient.*privileges.*',
            r'.*SecurityException.*'
        ],
        'FILE_NOT_FOUND': [
            r'.*file.*not.*found.*',
            r'.*FileNotFoundError.*',
            r'.*path.*does.*not.*exist.*',
            r'.*No such file.*'
        ],
        'CONFIGURATION_ERROR': [
            r'.*config.*error.*',
            r'.*configuration.*invalid.*',
            r'.*settings.*not.*found.*',
            r'.*yaml.*error.*',
            r'.*json.*error.*'
        ],
        'IMPORT_ERROR': [
            r'.*ImportError.*',
            r'.*ModuleNotFoundError.*',
            r'.*cannot import.*',
            r'.*import.*failed.*'
        ],
        'VALUE_ERROR': [
            r'.*ValueError.*',
            r'.*invalid.*value.*',
            r'.*value.*error.*'
        ],
        'TYPE_ERROR': [
            r'.*TypeError.*',
            r'.*type.*error.*',
            r'.*unexpected.*type.*'
        ],
        'ATTRIBUTE_ERROR': [
            r'.*AttributeError.*',
            r'.*attribute.*not.*found.*',
            r'.*has no attribute.*'
        ],
        'KEY_ERROR': [
            r'.*KeyError.*',
            r'.*key.*not.*found.*',
            r'.*missing.*key.*'
        ],
        'INDEX_ERROR': [
            r'.*IndexError.*',
            r'.*index.*out.*of.*range.*',
            r'.*list.*index.*'
        ],
    }

    # Suggested actions for each error category
    SUGGESTED_ACTIONS = {
        'ASSERTION_FAILURE': 'Review test logic, verify expected values, check test data validity',
        'TIMEOUT_ERROR': 'Increase timeout values, check performance, verify system responsiveness',
        'CONNECTION_ERROR': 'Verify connection parameters, check service availability, review network settings',
        'NETWORK_ERROR': 'Check network connectivity, verify IP addresses/URLs, test network access',
        'PERMISSION_ERROR': 'Run with elevated privileges, check file/directory permissions',
        'FILE_NOT_FOUND': 'Verify file paths, check if files were created, review test setup',
        'CONFIGURATION_ERROR': 'Validate configuration files, check syntax, verify settings',
        'IMPORT_ERROR': 'Check module installation, verify dependencies, review Python path',
        'VALUE_ERROR': 'Validate input values, check data types, review function parameters',
        'TYPE_ERROR': 'Verify data types, check type conversions, review function signatures',
        'ATTRIBUTE_ERROR': 'Check object attributes, verify class definitions, review API usage',
        'KEY_ERROR': 'Verify dictionary keys, check data structure, validate JSON/dict access',
        'INDEX_ERROR': 'Check list bounds, verify array access, validate index values',
        'UNKNOWN': 'Review error message and stack trace, check logs for additional context'
    }

    @classmethod
    def classify_error(cls, error_message: str, stack_trace: str = "") -> str:
        """Classify error into predefined categories."""
        error_text = f"{error_message} {stack_trace}".lower()

        for category, patterns in cls.ERROR_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, error_text, re.IGNORECASE):
                    return category

        return 'UNKNOWN'

    @classmethod
    def get_suggested_action(cls, category: str) -> str:
        """Get suggested action for error category."""
        return cls.SUGGESTED_ACTIONS.get(category, cls.SUGGESTED_ACTIONS['UNKNOWN'])


class ErrorExtractor:
    """Extract detailed error information from various sources."""

    @staticmethod
    def extract_from_pytest_log(log_content: str) -> Optional[ErrorDetails]:
        """Extract error details from pytest log content."""
        if not log_content:
            return None

        error_type = "Unknown"
        error_message = ""
        stack_trace = ""
        test_step = None

        # Extract different types of errors
        error_types = [
            "RuntimeError", "AssertionError", "TimeoutException", "TimeoutError",
            "ValueError", "TypeError", "AttributeError", "KeyError", "IndexError",
            "ImportError", "ModuleNotFoundError", "FileNotFoundError",
            "ConnectionError", "NetworkError", "PermissionError"
        ]

        for err_type in error_types:
            if f"{err_type}:" in log_content:
                error_type = err_type
                error_start = log_content.find(f"{err_type}:")
                if error_start != -1:
                    error_line = log_content[error_start:].split('\n')[0]
                    error_message = error_line.replace(f"{err_type}: ", "").strip()
                break

        # Fallback: Generic error extraction
        if not error_message:
            lines = log_content.split('\n')
            for line in lines:
                if line.strip().startswith('E   '):
                    error_message = line.replace('E   ', '').strip()
                    if error_message:
                        break

        # Extract stack trace
        if "Traceback" in log_content:
            traceback_start = log_content.find("Traceback")
            if traceback_start != -1:
                traceback_end = log_content.find("\n\n", traceback_start)
                if traceback_end == -1:
                    traceback_end = len(log_content)
                stack_trace = log_content[traceback_start:traceback_end].strip()

        if not error_message:
            error_message = "Test execution failed"

        # Classify error
        error_category = ErrorClassifier.classify_error(error_message, stack_trace)
        suggested_action = ErrorClassifier.get_suggested_action(error_category)

        return ErrorDetails(
            error_type=error_type,
            error_message=error_message,
            error_category=error_category,
            stack_trace=stack_trace,
            test_step=test_step,
            timestamp=datetime.datetime.now().isoformat(),
            suggested_action=suggested_action
        )

    @staticmethod
    def extract_from_exception(exception: Exception) -> ErrorDetails:
        """Extract error details from Python exception."""
        error_type = type(exception).__name__
        error_message = str(exception)
        stack_trace = traceback.format_exc()

        # Classify error
        error_category = ErrorClassifier.classify_error(error_message, stack_trace)
        suggested_action = ErrorClassifier.get_suggested_action(error_category)

        return ErrorDetails(
            error_type=error_type,
            error_message=error_message,
            error_category=error_category,
            stack_trace=stack_trace,
            test_step=None,
            timestamp=datetime.datetime.now().isoformat(),
            suggested_action=suggested_action
        )


class ErrorReportFormatter:
    """Format error information for different reporting formats."""

    @staticmethod
    def format_for_html(error_details: ErrorDetails, max_length: int = 100) -> Dict[str, str]:
        """Format error details for HTML display."""
        # Truncate error message for table display
        short_message = error_details.error_message
        if len(short_message) > max_length:
            short_message = short_message[:max_length-3] + "..."

        # Create detailed popup content
        stack_trace_html = ""
        if error_details.stack_trace:
            # Limit stack trace length for HTML display
            stack_trace_display = error_details.stack_trace
            if len(stack_trace_display) > 1000:
                stack_trace_display = stack_trace_display[:1000] + "\n... (truncated)"
            stack_trace_html = f'''<div class="stack-trace">
                <h5>Stack Trace:</h5>
                <pre>{stack_trace_display}</pre>
            </div>'''

        detailed_content = f"""
        <div class="error-details-popup">
            <h4>🚫 Error Details</h4>
            <table class="error-info-table">
                <tr><td><strong>Type:</strong></td><td>{error_details.error_type}</td></tr>
                <tr><td><strong>Category:</strong></td><td>{error_details.error_category}</td></tr>
                <tr><td><strong>Message:</strong></td><td>{error_details.error_message}</td></tr>
                {f'<tr><td><strong>Test Step:</strong></td><td>{error_details.test_step}</td></tr>' if error_details.test_step else ''}
                <tr><td><strong>Timestamp:</strong></td><td>{error_details.timestamp}</td></tr>
                <tr><td><strong>Suggested Action:</strong></td><td class="suggested-action">{error_details.suggested_action}</td></tr>
            </table>
            {stack_trace_html}
        </div>
        """

        return {
            'short_message': short_message,
            'detailed_content': detailed_content,
            'category_icon': ErrorReportFormatter._get_category_icon(error_details.error_category),
            'severity_class': ErrorReportFormatter._get_severity_class(error_details.error_category)
        }

    @staticmethod
    def format_for_console(error_details: ErrorDetails) -> str:
        """Format error details for console display."""
        icon = ErrorReportFormatter._get_category_icon(error_details.error_category)

        formatted = f"""
{icon} ERROR DETAILS:
  Type: {error_details.error_type}
  Category: {error_details.error_category}
  Message: {error_details.error_message}
  Test Step: {error_details.test_step or 'N/A'}
  Suggested Action: {error_details.suggested_action}
  Timestamp: {error_details.timestamp}
"""

        if error_details.stack_trace:
            formatted += f"\n  Stack Trace:\n{error_details.stack_trace}\n"

        return formatted

    @staticmethod
    def _get_category_icon(category: str) -> str:
        """Get icon for error category."""
        icons = {
            'ASSERTION_FAILURE': '⚠️',
            'TIMEOUT_ERROR': '⏰',
            'CONNECTION_ERROR': '🔌',
            'NETWORK_ERROR': '🌐',
            'PERMISSION_ERROR': '🔒',
            'FILE_NOT_FOUND': '📁',
            'CONFIGURATION_ERROR': '⚙️',
            'IMPORT_ERROR': '📦',
            'VALUE_ERROR': '💢',
            'TYPE_ERROR': '🔤',
            'ATTRIBUTE_ERROR': '🔍',
            'KEY_ERROR': '🔑',
            'INDEX_ERROR': '📊',
            'UNKNOWN': '❓'
        }
        return icons.get(category, '❓')

    @staticmethod
    def _get_severity_class(category: str) -> str:
        """Get CSS class for error severity."""
        high_severity = ['CONNECTION_ERROR', 'NETWORK_ERROR', 'TIMEOUT_ERROR']
        medium_severity = ['ASSERTION_FAILURE', 'CONFIGURATION_ERROR', 'IMPORT_ERROR']

        if category in high_severity:
            return 'error-high-severity'
        elif category in medium_severity:
            return 'error-medium-severity'
        else:
            return 'error-low-severity'


class EnhancedErrorReporter:
    """Main class for enhanced error reporting."""

    def __init__(self):
        self.error_storage: Dict[str, List[ErrorDetails]] = {}
        self.error_statistics: Dict[str, int] = {}

    def capture_test_error(self, test_id: str, log_content: str = "",
                          exception: Optional[Exception] = None) -> Optional[ErrorDetails]:
        """Capture and store detailed error information."""
        error_details = None

        # Try different extraction methods
        if exception:
            error_details = ErrorExtractor.extract_from_exception(exception)
        elif log_content:
            error_details = ErrorExtractor.extract_from_pytest_log(log_content)

        if error_details:
            # Store error details
            if test_id not in self.error_storage:
                self.error_storage[test_id] = []
            self.error_storage[test_id].append(error_details)

            # Update statistics
            category = error_details.error_category
            self.error_statistics[category] = self.error_statistics.get(category, 0) + 1

        return error_details

    def get_test_errors(self, test_id: str) -> List[ErrorDetails]:
        """Get all errors for a specific test."""
        return self.error_storage.get(test_id, [])

    def get_error_summary(self) -> Dict[str, int]:
        """Get error category statistics."""
        return self.error_statistics.copy()

    def format_error_for_display(self, test_id: str, format_type: str = "html") -> str:
        """Format error information for display."""
        errors = self.get_test_errors(test_id)
        if not errors:
            return "No error details available"

        # Use the most recent/relevant error
        primary_error = errors[-1]

        if format_type == "html":
            formatted = ErrorReportFormatter.format_for_html(primary_error)
            return formatted['short_message']
        elif format_type == "console":
            return ErrorReportFormatter.format_for_console(primary_error)
        else:
            return primary_error.error_message

    def generate_error_report_html(self) -> str:
        """Generate comprehensive error report HTML."""
        if not self.error_storage:
            return "<p>No errors to report</p>"

        html = """
        <div class="error-report-section">
            <h3>🚫 Error Analysis Report</h3>
            <div class="error-statistics">
                <h4>Error Category Breakdown:</h4>
                <table class="error-stats-table">
                    <thead>
                        <tr><th>Category</th><th>Count</th><th>Percentage</th></tr>
                    </thead>
                    <tbody>
        """

        total_errors = sum(self.error_statistics.values())
        for category, count in sorted(self.error_statistics.items()):
            percentage = (count / total_errors * 100) if total_errors > 0 else 0
            icon = ErrorReportFormatter._get_category_icon(category)
            html += f"<tr><td>{icon} {category}</td><td>{count}</td><td>{percentage:.1f}%</td></tr>"

        html += """
                    </tbody>
                </table>
            </div>
        </div>
        """

        return html


# Global enhanced error reporter instance
enhanced_error_reporter = EnhancedErrorReporter()


# Convenience functions for integration
def capture_test_error(test_id: str, log_content: str = "",
                      exception: Optional[Exception] = None) -> Optional[ErrorDetails]:
    """Capture test error using global reporter."""
    return enhanced_error_reporter.capture_test_error(test_id, log_content, exception=exception)


def get_formatted_error_details(test_id: str, format_type: str = "html") -> str:
    """Get formatted error details for a test."""
    return enhanced_error_reporter.format_error_for_display(test_id, format_type)


def generate_error_analysis_html() -> str:
    """Generate error analysis HTML section."""
    return enhanced_error_reporter.generate_error_report_html()
