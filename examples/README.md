# Examples

This directory is reserved for future example scripts and demonstrations.

For now, please refer to:
- **Test Suite**: `tests/test_dashboard_features.py` - Comprehensive test examples
- **Sample Report**: `reports/complete_dashboard_report.html` - Generated dashboard report
- **Configuration**: `config/sample_config.yaml` - Example configuration file

## Running Examples

To generate a sample report:

```bash
pytest tests/test_dashboard_features.py --html=reports/sample_report.html --self-contained-html
```

To use custom configuration:

```bash
cp config/sample_config.yaml pytest_html_dashboard.yaml
# Edit pytest_html_dashboard.yaml with your settings
pytest tests/ --html=reports/report.html --self-contained-html
```
