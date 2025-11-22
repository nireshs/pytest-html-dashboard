"""AI-powered error analysis and suggestions."""

import re
from typing import Dict, List, Optional, Any
import hashlib


class AIErrorAnalyzer:
    """Analyzes test errors and provides AI-powered suggestions."""

    def __init__(self, api_key: Optional[str] = None, provider: str = "local"):
        """Initialize AI error analyzer.

        Args:
            api_key: Optional API key for AI service (OpenAI, Anthropic, etc.)
            provider: AI provider ('local', 'openai', 'anthropic')
        """
        self.api_key = api_key
        self.provider = provider
        self.error_patterns = self._load_error_patterns()
        self.solution_cache: Dict[str, Dict] = {}

    def _load_error_patterns(self) -> List[Dict[str, Any]]:
        """Load common error patterns and solutions.

        Returns:
            List of error pattern dictionaries
        """
        return [
            {
                "pattern": r"AssertionError: assert (\w+) == (\w+)",
                "category": "Assertion Failure",
                "severity": "high",
                "suggestions": [
                    "Check if the expected value matches actual output",
                    "Verify test data setup is correct",
                    "Review recent code changes affecting this value",
                    "Add debug logging to track value changes"
                ],
                "docs": [
                    "https://docs.pytest.org/en/stable/how-to/assert.html",
                    "https://docs.python.org/3/library/unittest.html#assert-methods"
                ]
            },
            {
                "pattern": r"TimeoutError|timeout|timed out",
                "category": "Timeout",
                "severity": "medium",
                "suggestions": [
                    "Increase timeout value if operation is legitimately slow",
                    "Check for network/database connectivity issues",
                    "Review performance of external dependencies",
                    "Add logging to identify where timeout occurs",
                    "Consider adding retry logic for flaky operations"
                ],
                "docs": [
                    "https://docs.pytest.org/en/stable/how-to/timeout.html"
                ]
            },
            {
                "pattern": r"ConnectionError|Connection refused|Connection reset",
                "category": "Connection Error",
                "severity": "high",
                "suggestions": [
                    "Verify service/server is running and accessible",
                    "Check network connectivity and firewall rules",
                    "Confirm correct host and port configuration",
                    "Review service health checks and startup time",
                    "Add retry mechanism with exponential backoff"
                ],
                "docs": [
                    "https://requests.readthedocs.io/en/latest/user/advanced/#timeouts"
                ]
            },
            {
                "pattern": r"ModuleNotFoundError|ImportError: No module named",
                "category": "Import Error",
                "severity": "critical",
                "suggestions": [
                    "Install missing package: pip install <package-name>",
                    "Check if package is in requirements.txt",
                    "Verify virtual environment is activated",
                    "Check Python path configuration",
                    "Ensure package is available in test environment"
                ],
                "docs": [
                    "https://packaging.python.org/tutorials/installing-packages/"
                ]
            },
            {
                "pattern": r"AttributeError: .* has no attribute",
                "category": "Attribute Error",
                "severity": "high",
                "suggestions": [
                    "Check object type - might be None or wrong type",
                    "Verify attribute name spelling",
                    "Review API changes in dependencies",
                    "Add type checking or validation",
                    "Check mock/fixture configuration"
                ],
                "docs": [
                    "https://docs.python.org/3/library/exceptions.html#AttributeError"
                ]
            },
            {
                "pattern": r"KeyError: '(\w+)'",
                "category": "Key Error",
                "severity": "medium",
                "suggestions": [
                    "Check if key exists before accessing: dict.get('key', default)",
                    "Verify data structure matches expectations",
                    "Review API response format",
                    "Add validation for required fields",
                    "Use defensive programming with try-except"
                ],
                "docs": [
                    "https://docs.python.org/3/library/stdtypes.html#dict"
                ]
            },
            {
                "pattern": r"FileNotFoundError|No such file or directory",
                "category": "File Not Found",
                "severity": "medium",
                "suggestions": [
                    "Verify file path is correct and file exists",
                    "Check working directory in test context",
                    "Use absolute paths or Path.resolve()",
                    "Ensure test fixtures create necessary files",
                    "Check file permissions"
                ],
                "docs": [
                    "https://docs.python.org/3/library/pathlib.html"
                ]
            },
            {
                "pattern": r"ValueError: invalid literal for int\(\)",
                "category": "Type Conversion Error",
                "severity": "medium",
                "suggestions": [
                    "Validate input before type conversion",
                    "Add try-except for conversion errors",
                    "Check data source for invalid values",
                    "Use more flexible parsing (ast.literal_eval)",
                    "Add data validation layer"
                ],
                "docs": [
                    "https://docs.python.org/3/library/functions.html#int"
                ]
            },
            {
                "pattern": r"selenium\.common\.exceptions\.(.*?):",
                "category": "Selenium Error",
                "severity": "high",
                "suggestions": [
                    "Add explicit waits for element visibility",
                    "Check if element locator is correct",
                    "Verify page is fully loaded before interaction",
                    "Handle dynamic content with WebDriverWait",
                    "Review browser compatibility"
                ],
                "docs": [
                    "https://selenium-python.readthedocs.io/waits.html",
                    "https://www.selenium.dev/documentation/webdriver/waits/"
                ]
            },
            {
                "pattern": r"PermissionError|Permission denied",
                "category": "Permission Error",
                "severity": "high",
                "suggestions": [
                    "Check file/directory permissions",
                    "Run with appropriate user privileges",
                    "Verify write access to output directory",
                    "Check for file locks by other processes",
                    "Review security policies"
                ],
                "docs": [
                    "https://docs.python.org/3/library/exceptions.html#PermissionError"
                ]
            }
        ]

    def analyze_error(
        self, error_message: str, stack_trace: Optional[str] = None
    ) -> Dict[str, Any]:
        """Analyze an error and provide AI-powered suggestions.

        Args:
            error_message: Error message text
            stack_trace: Optional full stack trace

        Returns:
            Analysis results with suggestions
        """
        # Generate cache key
        cache_key = hashlib.md5(
            error_message.encode()
        ).hexdigest()

        # Check cache
        if cache_key in self.solution_cache:
            return self.solution_cache[cache_key]

        # Match against patterns
        analysis = {
            "error_message": error_message,
            "category": "Unknown Error",
            "severity": "medium",
            "suggestions": [],
            "documentation_links": [],
            "similar_issues": [],
            "ai_analysis": None
        }

        # Pattern matching
        for pattern_dict in self.error_patterns:
            if re.search(
                pattern_dict["pattern"], error_message, re.IGNORECASE
            ):
                analysis["category"] = pattern_dict["category"]
                analysis["severity"] = pattern_dict["severity"]
                analysis["suggestions"] = pattern_dict["suggestions"]
                analysis["documentation_links"] = pattern_dict["docs"]
                break

        # Add generic suggestions if no pattern matched
        if not analysis["suggestions"]:
            analysis["suggestions"] = self._generate_generic_suggestions(
                error_message
            )

        # Add search links
        analysis["search_links"] = self._generate_search_links(error_message)

        # AI enhancement if available
        if self.api_key and self.provider != "local":
            analysis["ai_analysis"] = self._get_ai_analysis(
                error_message, stack_trace
            )

        # Cache result
        self.solution_cache[cache_key] = analysis

        return analysis

    def _generate_generic_suggestions(self, error_message: str) -> List[str]:
        """Generate generic suggestions for unknown errors.

        Args:
            error_message: Error message

        Returns:
            List of generic suggestions
        """
        suggestions = [
            "Review the full stack trace for more context",
            "Check recent code changes that might affect this test",
            "Add debug logging to identify the root cause",
            "Search for similar errors in project history"
        ]

        # Add specific suggestions based on keywords
        if "null" in error_message.lower() or "none" in error_message.lower():
            suggestions.append(
                "Add null/None checks before accessing properties"
            )

        if "database" in error_message.lower() or "sql" in error_message.lower():
            suggestions.append("Verify database connection and schema")
            suggestions.append("Check transaction handling")

        if "api" in error_message.lower():
            suggestions.append("Verify API endpoint availability")
            suggestions.append("Check request/response format")

        return suggestions

    def _generate_search_links(self, error_message: str) -> Dict[str, str]:
        """Generate search links for the error.

        Args:
            error_message: Error message

        Returns:
            Dictionary of search links
        """
        # Extract main error type
        error_type = error_message.split(":")[0].strip()
        query = error_type.replace(" ", "+")

        return {
            "stackoverflow": f"https://stackoverflow.com/search?q={query}+pytest",
            "github": f"https://github.com/search?q={query}+language:Python&type=issues",
            "google": f"https://www.google.com/search?q={query}+pytest+python"
        }

    def _get_ai_analysis(
        self, error_message: str, stack_trace: Optional[str]
    ) -> Optional[str]:
        """Get AI-powered analysis (placeholder for API integration).

        Args:
            error_message: Error message
            stack_trace: Optional stack trace

        Returns:
            AI analysis text or None
        """
        # Placeholder for actual AI integration
        # This would call OpenAI, Anthropic, or other AI services
        # For now, return None to indicate not implemented
        return None

    def generate_error_report_html(
        self, analysis: Dict[str, Any]
    ) -> str:
        """Generate HTML for error analysis display.

        Args:
            analysis: Error analysis dictionary

        Returns:
            HTML string
        """
        severity_colors = {
            "critical": "#d32f2f",
            "high": "#f57c00",
            "medium": "#fbc02d",
            "low": "#689f38"
        }

        color = severity_colors.get(analysis["severity"], "#757575")

        suggestions_html = "".join([
            f'<li class="suggestion-item">💡 {suggestion}</li>'
            for suggestion in analysis["suggestions"]
        ])

        docs_html = "".join([
            f'<li><a href="{link}" target="_blank">📚 {link}</a></li>'
            for link in analysis["documentation_links"]
        ])

        search_html = "".join([
            f'<li><a href="{url}" target="_blank">🔍 Search on {name.title()}</a></li>'
            for name, url in analysis["search_links"].items()
        ])

        ai_section = ""
        if analysis.get("ai_analysis"):
            ai_section = f"""
            <div class="ai-analysis-section">
                <h4>🤖 AI Analysis</h4>
                <div class="ai-content">{analysis["ai_analysis"]}</div>
            </div>
            """

        return f"""
        <div class="error-analysis">
            <div class="error-category">
                <span class="category-badge" style="background-color: {color}">
                    {analysis["category"]}
                </span>
                <span class="severity-badge severity-{analysis["severity"]}">
                    {analysis["severity"].upper()}
                </span>
            </div>

            <div class="suggestions-section">
                <h4>💭 Suggested Solutions</h4>
                <ul class="suggestions-list">
                    {suggestions_html}
                </ul>
            </div>

            {ai_section}

            <div class="resources-section">
                <h4>📖 Documentation & Resources</h4>
                <ul class="resources-list">
                    {docs_html}
                </ul>
            </div>

            <div class="search-section">
                <h4>🔎 Search for Solutions</h4>
                <ul class="search-links">
                    {search_html}
                </ul>
            </div>
        </div>

        <style>
            .error-analysis {{
                background: #f8f9fa;
                border-radius: 8px;
                padding: 16px;
                margin-top: 12px;
            }}

            .error-category {{
                display: flex;
                gap: 8px;
                margin-bottom: 16px;
            }}

            .category-badge {{
                padding: 4px 12px;
                border-radius: 4px;
                color: white;
                font-weight: bold;
                font-size: 12px;
            }}

            .severity-badge {{
                padding: 4px 12px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 12px;
            }}

            .severity-critical {{ background: #ffebee; color: #d32f2f; }}
            .severity-high {{ background: #fff3e0; color: #f57c00; }}
            .severity-medium {{ background: #fffde7; color: #f57f17; }}
            .severity-low {{ background: #f1f8e9; color: #558b2f; }}

            .suggestions-section, .resources-section, .search-section, .ai-analysis-section {{
                margin-bottom: 16px;
            }}

            .suggestions-section h4, .resources-section h4, .search-section h4, .ai-analysis-section h4 {{
                margin: 0 0 8px 0;
                font-size: 14px;
                color: #333;
            }}

            .suggestions-list, .resources-list, .search-links {{
                list-style: none;
                padding: 0;
                margin: 0;
            }}

            .suggestion-item {{
                padding: 8px;
                background: white;
                border-left: 3px solid #4CAF50;
                margin-bottom: 8px;
                border-radius: 4px;
            }}

            .resources-list li, .search-links li {{
                padding: 6px 0;
            }}

            .resources-list a, .search-links a {{
                color: #1976d2;
                text-decoration: none;
            }}

            .resources-list a:hover, .search-links a:hover {{
                text-decoration: underline;
            }}

            .ai-content {{
                background: white;
                padding: 12px;
                border-radius: 4px;
                border-left: 3px solid #9c27b0;
            }}
        </style>
        """

    def batch_analyze(
        self, errors: List[Dict[str, str]]
    ) -> List[Dict[str, Any]]:
        """Analyze multiple errors in batch.

        Args:
            errors: List of error dictionaries with 'message' and optional 'trace'

        Returns:
            List of analysis results
        """
        return [
            self.analyze_error(
                error.get("message", ""),
                error.get("trace")
            )
            for error in errors
        ]
