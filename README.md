# pytest-dashboard

[![PyPI version](https://badge.fury.io/py/pytest-dashboard.svg)](https://badge.fury.io/py/pytest-dashboard)
[![Python versions](https://img.shields.io/pypi/pyversions/pytest-dashboard.svg)](https://pypi.org/project/pytest-dashboard/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A comprehensive pytest plugin that enhances HTML reports with:
- 📊 **Interactive Charts** - Beautiful Chart.js visualizations for test results
- 🎨 **Customizable Branding** - Configure colors, logos, and company names
- 🔍 **Enhanced Error Reporting** - Intelligent error classification with suggested actions
- 📋 **Comprehensive Test Tables** - Detailed test execution information with expandable error details
- ⚡ **Zero Configuration** - Works out of the box with sensible defaults
- 🎯 **Highly Configurable** - Extensive YAML-based configuration system

## Features

### Interactive Visual Charts
- Pass/Fail distribution donut charts
- Overall pass rate visualization
- Automatic data labels with percentages
- Responsive design for all screen sizes

### Intelligent Error Classification
Automatically categorizes test failures into:
- Assertion Failures
- Timeout Errors
- Connection Errors
- Configuration Errors
- Import Errors
- And more...

Each error category includes:
- Error type and message
- Stack trace
- Suggested remediation actions
- Timestamp and context

### Beautiful Styling
- Modern gradient backgrounds
- Clean, professional table layouts
- Sticky headers for easy navigation
- Hover effects and smooth animations
- Mobile-responsive design

### Comprehensive Test Information
- Test suite organization
- Individual test case details
- Step-by-step execution logs
- Duration and timing information
- Result details and error messages

## Installation

```bash
pip install pytest-dashboard
```

## Quick Start

### Basic Usage

Simply install the plugin and run pytest with HTML reporting:

```bash
pytest --html=report.html --self-contained-html
```

The plugin automatically enhances the HTML report with all features enabled.

### Custom Configuration

Create a `pytest_dashboard.yaml` configuration file:

```yaml
branding:
  company_name: "My Company"
  report_title: "Test Execution Report"
  logo_url: "data:image/png;base64,..."  # Base64 encoded logo
  primary_color: "#004488"
  secondary_color: "#0066CC"
  success_color: "#4CAF50"
  failure_color: "#f44336"

charts:
  enable_charts: true
  chart_height: 300
  show_pass_rate_chart: true
  show_status_distribution_chart: true

report:
  enable_enhanced_reporting: true
  enable_error_classification: true
  enable_comprehensive_table: true
  max_error_message_length: 100
  show_timestamps: true
```

### Command Line Options

Configure the plugin via command line:

```bash
pytest --html=report.html \
       --dashboard-company-name="My Company" \
       --dashboard-report-title="Test Dashboard" \
       --dashboard-primary-color="#FF6B35"
```

### Programmatic Configuration

```python
# conftest.py
from pytest_dashboard import ReporterConfig, BrandingConfig

def pytest_configure(config):
    # Customize branding
    branding = BrandingConfig(
        company_name="My Company",
        report_title="Custom Test Dashboard",
        primary_color="#1E88E5",
        secondary_color="#42A5F5"
    )

    # Apply configuration
    reporter_config = ReporterConfig(branding=branding)
    config._dashboard_reporter_config = reporter_config
```## Configuration Reference

### Branding Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `company_name` | str | "Test Automation Framework" | Your company/project name |
| `report_title` | str | "Enhanced Test Execution Report" | Report title |
| `logo_url` | str | None | Base64 encoded logo or URL |
| `primary_color` | str | "#004488" | Primary theme color |
| `secondary_color` | str | "#0066CC" | Secondary theme color |
| `success_color` | str | "#4CAF50" | Success/pass color |
| `failure_color` | str | "#f44336" | Failure/error color |
| `warning_color` | str | "#ff9800" | Warning/skip color |

### Chart Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable_charts` | bool | true | Enable/disable all charts |
| `chart_height` | int | 300 | Chart height in pixels |
| `show_pass_rate_chart` | bool | true | Show pass rate chart |
| `show_status_distribution_chart` | bool | true | Show status distribution chart |
| `chart_animation` | bool | true | Enable chart animations |

### Report Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enable_enhanced_reporting` | bool | true | Enable enhanced features |
| `enable_error_classification` | bool | true | Classify and analyze errors |
| `enable_comprehensive_table` | bool | true | Show comprehensive test table |
| `max_error_message_length` | int | 100 | Max error message length in table |
| `show_timestamps` | bool | true | Show test start/end times |
| `show_duration` | bool | true | Show test durations |

## Advanced Usage

### Custom CSS

Add custom CSS to further customize your reports:

```yaml
custom_css: |
  .report-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  }
  .test-table-container {
    border-radius: 15px;
  }
```

### Custom JavaScript

Add custom JavaScript for additional functionality:

```yaml
custom_js: |
  document.addEventListener('DOMContentLoaded', function() {
    console.log('Custom report loaded!');
    // Your custom JavaScript here
  });
```

### Integrating with CI/CD

#### Jenkins

```groovy
pipeline {
    stages {
        stage('Test') {
            steps {
                sh 'pytest --html=reports/report.html --self-contained-html'
            }
        }
    }
    post {
        always {
            publishHTML([
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Enhanced Test Report'
            ])
        }
    }
}
```

#### GitHub Actions

```yaml
- name: Run tests
  run: pytest --html=report.html --self-contained-html

- name: Upload test report
  uses: actions/upload-artifact@v3
  with:
    name: test-report
    path: report.html
```

#### GitLab CI

```yaml
test:
  script:
    - pytest --html=report.html --self-contained-html
  artifacts:
    when: always
    paths:
      - report.html
    expire_in: 30 days
```

## Examples

Check the `examples/` directory for complete working examples:

- `basic_usage.py` - Simple test suite with enhanced reporting
- `custom_branding.yaml` - Custom branding configuration
- `advanced_config.yaml` - Advanced configuration options
- `ci_integration/` - CI/CD integration examples

## Comparison with pytest-html

pytest-dashboard is built as an enhancement layer on top of pytest-html, adding:

| Feature | pytest-html | pytest-dashboard |
|---------|-------------|------------------|
| Basic HTML reports | ✅ | ✅ |
| Interactive charts | ❌ | ✅ |
| Error classification | ❌ | ✅ |
| Customizable branding | Limited | ✅ Full |
| Comprehensive test tables | ❌ | ✅ |
| Suggested error actions | ❌ | ✅ |
| Mobile responsive | Partial | ✅ Full |
| Configuration system | Limited | ✅ YAML/CLI/Code |

## Development

### Setting Up Development Environment

```bash
# Clone the repository
git clone https://github.com/nireshs/pytest-dashboard.git
cd pytest-dashboard

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=pytest_dashboard --cov-report=html

# Run specific test file
pytest tests/test_plugin.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Credits

- Built on top of [pytest](https://pytest.org/) and [pytest-html](https://github.com/pytest-dev/pytest-html)
- Charts powered by [Chart.js](https://www.chartjs.org/)
- Icons from various emoji sets

## Changelog

### Version 1.0.0 (2025-11-22)
- Initial release
- Interactive Chart.js visualizations
- Enhanced error reporting with classification
- Customizable branding system
- Comprehensive test tables
- YAML-based configuration
- Full pytest-html compatibility

## Support

- 📧 Email: niresh.shanmugam@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/nireshs/pytest-dashboard/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/nireshs/pytest-dashboard/discussions)

## Roadmap

- [ ] Additional chart types (bar charts, line graphs)
- [ ] Test history tracking across runs
- [ ] Comparison reports between test runs
- [ ] PDF export functionality
- [ ] Real-time test execution dashboard
- [ ] Integration with test management tools
- [ ] Custom reporter themes marketplace

---

Made with ❤️ by the pytest-dashboard team
