# PyPI Publishing Guide

## Prerequisites

1. **PyPI Account**: Create accounts on both:
   - TestPyPI: https://test.pypi.org/account/register/
   - PyPI: https://pypi.org/account/register/

2. **API Tokens**: Generate API tokens for uploading:
   - TestPyPI: https://test.pypi.org/manage/account/token/
   - PyPI: https://pypi.org/manage/account/token/

3. **Configure `.pypirc`** (Optional but recommended):
   ```ini
   [distutils]
   index-servers =
       pypi
       testpypi

   [pypi]
   username = __token__
   password = pypi-AgEIcHlwaS5vcmc...

   [testpypi]
   username = __token__
   password = pypi-AgENdGVzdC5weXBpLm9yZw...
   ```
   Save to: `%USERPROFILE%\.pypirc` (Windows) or `~/.pypirc` (Linux/Mac)

## Publishing Steps

### 1. Build the Package

```powershell
# Clean previous builds
Remove-Item -Recurse -Force dist\*, build\* -ErrorAction SilentlyContinue

# Build distribution packages
python -m build
```

This creates:
- `dist/pytest_html_dashboard-1.1.0-py3-none-any.whl` (wheel)
- `dist/pytest_html_dashboard-1.1.0.tar.gz` (source distribution)

### 2. Validate the Package

```powershell
# Check package integrity
python -m twine check dist/*

# Expected output:
# Checking dist\pytest_html_dashboard-1.1.0-py3-none-any.whl: PASSED
# Checking dist\pytest_html_dashboard-1.1.0.tar.gz: PASSED
```

### 3. Test with TestPyPI (RECOMMENDED)

```powershell
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# Install from TestPyPI and test
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pytest-html-dashboard

# Run tests to verify
pytest tests/test_dashboard_features.py --html-dashboard=reports/test_report.html
```

**Note**: `--extra-index-url https://pypi.org/simple/` is needed because TestPyPI doesn't host dependencies like pytest and pytest-html.

### 4. Publish to PyPI (Production)

```powershell
# Upload to PyPI
python -m twine upload dist/*

# You'll be prompted for credentials if not in .pypirc
# Username: __token__
# Password: your-pypi-api-token
```

### 5. Verify Installation

```powershell
# Install from PyPI
pip install pytest-html-dashboard

# Verify version
python -c "import pytest_html_dashboard; print(pytest_html_dashboard.__version__)"

# Test functionality
pytest tests/ --html-dashboard=reports/verify.html
```

### 6. Create GitHub Release

```powershell
# Tag the release
git tag -a v1.1.0 -m "Release v1.1.0: Interactive Dashboard with Charts"
git push origin v1.1.0
```

Then create a release on GitHub:
1. Go to https://github.com/nireshs/pytest-html-dashboard/releases/new
2. Select tag: `v1.1.0`
3. Release title: `v1.1.0 - Interactive Dashboard Enhancement`
4. Copy changelog from `docs/CHANGELOG.md`
5. Attach dist files (optional): `pytest_html_dashboard-1.1.0.tar.gz` and `.whl`
6. Publish release

## Troubleshooting

### Common Issues

1. **"The name 'pytest-html-dashboard' is already claimed"**
   - Solution: Package name already exists, version update only

2. **"Invalid distribution"**
   - Check `twine check dist/*` output
   - Verify `pyproject.toml` syntax

3. **"Authentication failed"**
   - Regenerate API token
   - Check `.pypirc` format
   - Use `__token__` as username

4. **"File already exists"**
   - Can't re-upload same version
   - Increment version in `pyproject.toml` and rebuild

### Version Management

To publish a new version:

```powershell
# 1. Update version in pyproject.toml
# [project]
# version = "1.2.0"

# 2. Update CHANGELOG.md

# 3. Clean and rebuild
Remove-Item -Recurse -Force dist\*, build\*
python -m build

# 4. Test on TestPyPI first
python -m twine upload --repository testpypi dist/*

# 5. Upload to PyPI
python -m twine upload dist/*

# 6. Tag and release on GitHub
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

## Useful Commands

```powershell
# Check package metadata
python -m twine check dist/*

# Upload to TestPyPI only
python -m twine upload --repository testpypi dist/*

# Upload to PyPI only
python -m twine upload dist/*

# Upload specific version
python -m twine upload dist/pytest_html_dashboard-1.1.0*

# Skip existing files (update only)
python -m twine upload --skip-existing dist/*

# View package info on PyPI
# https://pypi.org/project/pytest-html-dashboard/

# View package info on TestPyPI
# https://test.pypi.org/project/pytest-html-dashboard/
```

## Post-Publication

1. **Update README badges** if needed
2. **Announce** on social media, forums, pytest community
3. **Monitor** PyPI download stats: https://pypistats.org/packages/pytest-html-dashboard
4. **Respond** to issues and pull requests on GitHub

## Security Best Practices

- ✅ Use API tokens instead of passwords
- ✅ Set token scope to "Upload packages only"
- ✅ Store `.pypirc` securely (chmod 600 on Unix)
- ✅ Never commit API tokens to Git
- ✅ Rotate tokens periodically
- ✅ Use separate tokens for TestPyPI and PyPI

## References

- PyPI Documentation: https://packaging.python.org/
- Twine Documentation: https://twine.readthedocs.io/
- TestPyPI: https://test.pypi.org/
- PyPI: https://pypi.org/
