# Changelog

All notable changes to pytest-enhanced-reporter will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# Changelog

All notable changes to pytest-html-dashboard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Additional chart types (bar charts, line graphs)
- PDF export functionality
- Custom reporter themes marketplace
- Integration with test management tools (TestRail, Xray, etc.)

## [1.2.0] - 2025-11-22

### 🚀 Major New Features

#### 📊 Historical Trend Analysis
- **Test History Tracking**: SQLite database for storing test results over time
- **Flaky Test Detection**: Automatic identification of unstable tests
- **Trend Visualization**: Charts showing pass rate trends across runs
- **Statistics Dashboard**: Overall metrics, most failed tests, slowest tests
- **Data Retention**: Configurable retention period (default: 90 days)
- **Test History API**: Query individual test performance over time

Configuration:
```yaml
historical:
  enable_tracking: true
  database_path: "test-history.db"
  show_trends: true
  flaky_detection: true
  retention_days: 90
```

#### ⚡ Real-Time Dashboard
- **Live Test Execution**: Watch tests execute in real-time
- **Auto-Updating Charts**: Charts refresh automatically as tests complete
- **Progress Indicators**: Visual feedback for running tests
- **WebSocket Support**: Fast, efficient updates with fallback to polling
- **Current Test Display**: See which test is currently executing
- **Session Status**: Connection indicator showing live/offline status

Configuration:
```yaml
realtime:
  enable_realtime: false  # Enable for live updates
  websocket_port: 8888
  poll_interval: 2  # seconds
```

#### 🤖 AI-Powered Error Analysis
- **Pattern Matching**: 10+ common error patterns with solutions
- **Smart Suggestions**: Context-aware remediation steps
- **Documentation Links**: Automatic links to relevant docs
- **Search Integration**: One-click search on Stack Overflow, GitHub, Google
- **Error Categorization**: Severity levels (critical/high/medium/low)
- **Solution Caching**: Fast repeated lookups
- **AI Provider Support**: Ready for OpenAI/Anthropic API integration

Supported Error Patterns:
- Assertion Failures
- Timeout Errors
- Connection Errors
- Import Errors
- Attribute Errors
- Key Errors
- File Not Found
- Type Conversion Errors
- Selenium Exceptions
- Permission Errors

Configuration:
```yaml
ai:
  enable_ai_analysis: true
  provider: "local"  # local, openai, anthropic
  pattern_matching: true
```

### ✨ Enhanced Features

#### New Modules
- `history.py` - Historical data storage and retrieval (450+ lines)
- `realtime.py` - Real-time updates with WebSocket support (400+ lines)
- `ai_analyzer.py` - AI error analysis engine (500+ lines)

#### Configuration Improvements
- New configuration sections: `historical`, `realtime`, `ai`
- Enhanced `ReporterConfig` with new feature flags
- Python 3.13 compatibility added

### 🔧 Technical Details

#### Database Schema
- `test_runs`: Aggregate run statistics
- `test_results`: Individual test outcomes
- `flaky_tests`: Flaky test tracking with flip counts
- Optimized indexes for fast queries

#### Real-Time Architecture
- WebSocket server for live connections
- HTTP polling fallback for compatibility
- JSON state file for persistence
- Background thread for non-blocking operation

#### AI Analysis Engine
- Regex-based pattern matching
- Error classification system
- Suggestion generation
- Documentation lookup
- Search query generation
- HTML report generation for rich display

### 📈 Statistics & Insights

New analytics capabilities:
- Average pass rate across all runs
- Most frequently failing tests
- Slowest tests (by average duration)
- Flaky test identification with confidence scores
- Trend analysis for test stability

### 🎨 UI Enhancements
- AI analysis sections in error popups
- Real-time status indicators
- Live test execution display
- Trend charts (when historical data available)
- Enhanced error detail views

### 📚 Documentation
- Updated README with v1.2.0 features
- New configuration examples
- API documentation for new modules
- Integration guides for new features

## [1.1.0] - 2025-11-22

### Added
- ✨ **Complete HTML Enhancement System** with modern dashboard-style reports
- 📊 **Chart.js Integration** for interactive visualizations:
  - Test status distribution donut chart
  - Pass rate analysis bar chart
  - Error categories breakdown chart (shows when tests fail)
  - Responsive chart sizing and animations
- 🎨 **Modern CSS Styling** featuring:
  - Gradient headers with customizable brand colors
  - Responsive summary cards with hover effects
  - Professional table layouts with sticky headers
  - Mobile-responsive design (automatic breakpoints)
  - Custom scrollbars for improved UX
  - Print-friendly styles
- 📋 **Comprehensive Test Results Table** including:
  - Test case names with full node IDs
  - Color-coded status badges (passed/failed/skipped)
  - Duration tracking with monospace formatting
  - Error category classification badges
  - Truncated error messages with full-text tooltips
  - Inline suggested remediation actions with 💡 icons
- 🔍 **Enhanced Error Reporting Integration**:
  - Visual error category badges
  - Inline suggested actions for all failures
  - Color-coded error messages with backgrounds
  - Error categories breakdown visualization
- ⚙️ **New Configuration Options**:
  - `chart_height` - Customize chart display height
  - `chart_animation` - Toggle chart animations on/off
  - `max_error_message_length` - Control error message truncation
  - `enable_comprehensive_table` - Show/hide detailed results table
- 🚀 **Automatic Report Enhancement**:
  - New `pytest_sessionfinish` hook for post-processing
  - Seamless integration with pytest-html workflow
  - Automatic HTML injection before `</body>` tag
  - Error handling with graceful degradation

### Improved
- Enhanced `plugin.py` with global test result collection
- Better error handling with detailed user feedback messages
- Command-line option integration and override system
- Configuration loading from multiple sources (YAML > CLI > defaults)
- Plugin version metadata display (v1.1.0)

### Fixed
- Error reporter method compatibility - now uses `get_test_errors()` (returns list)
- HTML insertion point detection for various HTML structures
- Test result tracking during execution phase
- Duration capture for all test outcomes

### Technical Details
- New module: `html_generator.py` (800+ lines of code)
- `HTMLGenerator` class with modular generation methods:
  - `generate_custom_css()` - Theme-aware styling
  - `generate_chartjs_script()` - Dynamic Chart.js initialization
  - `generate_dashboard_header()` - Branded header with logo
  - `generate_summary_cards()` - Statistics cards layout
  - `generate_charts_section()` - Multiple chart types
  - `generate_comprehensive_test_table()` - Detailed results
- Chart.js 4.4.0 via CDN integration
- CSS variables for theme customization
- Proper HTML escaping and sanitization
- Standalone report generation capability

### Documentation
- Updated README with v1.1.0 feature highlights
- Enhanced examples in `examples/` directory
- Improved configuration documentation
- Added Chart.js and CSS customization guides

## [1.0.0] - 2025-11-22

### Added
- Initial release of pytest-html-dashboard
- Interactive Chart.js visualizations for test results
  - Pass/Fail distribution donut chart
  - Overall pass rate chart with percentages
  - Automatic data labels and animations
- Enhanced error reporting with intelligent classification
  - 13+ error categories (Assertion, Timeout, Connection, etc.)
  - Suggested remediation actions for each error type
  - Stack trace capture and display
  - Error statistics and breakdown
- Customizable branding system
  - Configure company name, logo, and colors
  - Primary, secondary, success, failure, and warning colors
  - Custom CSS support
  - Custom JavaScript support
- Comprehensive test results table
  - Detailed test execution information
  - Expandable error details
  - Responsive design for mobile and desktop
  - Sticky headers for easy navigation
- YAML-based configuration system
  - Load from `pytest_enhanced_reporter.yaml`
  - Command-line argument support
  - Programmatic configuration via conftest.py
- Full pytest-html compatibility
  - Works as enhancement layer on top of pytest-html
  - No breaking changes to existing pytest-html users
- Professional documentation
  - Comprehensive README with examples
  - Configuration reference
  - CI/CD integration guides
  - API documentation

### Technical Details
- Python 3.8+ support
- Pytest 7.0+ compatibility
- pytest-html 4.0+ required
- Chart.js 3.9.1 for visualizations
- Zero configuration needed (sensible defaults)
- MIT License

### Dependencies
- pytest >= 7.0.0
- pytest-html >= 4.0.0
- pytest-metadata >= 3.0.0
- colorama >= 0.4.0
- prettytable >= 3.0.0
- pyyaml >= 6.0.0

## [0.1.0] - 2025-11-15 (Internal Development)

### Added
- Initial project structure
- Basic plugin architecture
- Configuration system prototype
- Error classification engine
- HTML enhancement pipeline
- Development environment setup

---

## Version History Summary

| Version | Release Date | Key Features |
|---------|--------------|--------------|
| 1.0.0   | 2025-11-22  | Initial public release with full feature set |
| 0.1.0   | 2025-11-15  | Internal development version |

## Migration Guide

### From pytest-html Only

If you're currently using pytest-html without enhancements:

```bash
# Before
pytest --html=report.html --self-contained-html

# After (with pytest-html-dashboard installed)
# Same command - enhancements are automatic!
pytest --html=report.html --self-contained-html
```

No changes needed! The plugin automatically enhances your reports while maintaining full backward compatibility.

### Customizing Your Reports

To customize the dashboard:

1. Create `pytest_html_dashboard.yaml`:
```yaml
branding:
  company_name: "Your Company"
  primary_color: "#YOUR_COLOR"
```

2. Run pytest as usual:
```bash
pytest --html=report.html --self-contained-html
```

## Support and Contributing

- 📧 Email: niresh.shanmugam@gmail.com
- 🐛 Issues: https://github.com/nireshs/pytest-html-dashboard/issues
- 💬 Discussions: https://github.com/nireshs/pytest-html-dashboard/discussions
- 🤝 Contributing: See CONTRIBUTING.md

## Links

- [GitHub Repository](https://github.com/nireshs/pytest-html-dashboard)
- [PyPI Package](https://pypi.org/project/pytest-html-dashboard/)
- [Documentation](https://pytest-html-dashboard.readthedocs.io/)
- [Issue Tracker](https://github.com/nireshs/pytest-html-dashboard/issues)

---

**Note**: Version numbers follow [Semantic Versioning](https://semver.org/):
- MAJOR version for incompatible API changes
- MINOR version for new functionality in a backward compatible manner
- PATCH version for backward compatible bug fixes
