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
- Additional chart types (bar charts, line graphs, trend analysis)
- Test history tracking across multiple runs
- Comparison reports between test runs
- PDF export functionality
- Real-time test execution dashboard
- Integration with test management tools (TestRail, Xray, etc.)
- Custom reporter themes marketplace

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
