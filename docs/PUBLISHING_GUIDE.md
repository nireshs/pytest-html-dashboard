# Publishing Guide - pytest-html-dashboard v1.1.0

This guide provides step-by-step instructions for publishing pytest-html-dashboard v1.1.0 to PyPI.

## Prerequisites

### 1. Install Required Tools
```powershell
# Install/upgrade build tools
pip install --upgrade build twine setuptools wheel
```

### 2. Verify Accounts
- [ ] PyPI account: https://pypi.org/account/register/
- [ ] TestPyPI account (optional): https://test.pypi.org/account/register/
- [ ] GitHub account with repository access

### 3. Configure PyPI Credentials

#### Option A: Using PyPI Tokens (Recommended)
```powershell
# Create ~/.pypirc (or %USERPROFILE%\.pypirc on Windows)
# Replace __token__ with your actual API token
```

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YOUR-API-TOKEN-HERE

[testpypi]
username = __token__
password = pypi-YOUR-TESTPYPI-TOKEN-HERE
```

#### Option B: Using Username/Password
You'll be prompted during upload (less secure).

## Pre-Release Checklist

### Code Quality
- [x] All tests passing: `pytest tests/`
- [x] Code formatted: `black src/ tests/`
- [x] Linting clean: `flake8 src/ tests/`
- [x] Type checking: `mypy src/`

### Documentation
- [x] README.md updated with v1.1.0 features
- [x] CHANGELOG.md has v1.1.0 entry
- [x] Version bumped in:
  - [x] pyproject.toml
  - [x] setup.py
  - [x] plugin.py (metadata)
- [x] Examples verified working
- [x] RELEASE_v1.1.0.md created

### Testing
```powershell
# Run complete test suite
pytest tests/ -v

# Test with example
cd examples
pytest basic_usage.py --html=report.html --self-contained-html
# Verify enhanced_report.html looks good

# Test installation in clean environment
python -m venv test_env
.\test_env\Scripts\activate
pip install .
pytest --version  # Should show plugin
deactivate
rm -rf test_env
```

## Publishing Steps

### Step 1: Clean Previous Builds
```powershell
# Remove old build artifacts
Remove-Item -Recurse -Force dist, build, *.egg-info -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force src\*.egg-info -ErrorAction SilentlyContinue
```

### Step 2: Build Distribution Packages
```powershell
# Build wheel and source distribution
python -m build

# This creates:
# - dist/pytest_html_dashboard-1.1.0-py3-none-any.whl
# - dist/pytest-html-dashboard-1.1.0.tar.gz
```

### Step 3: Verify Package Contents
```powershell
# Check distribution packages
twine check dist/*

# Expected output: "Checking dist/...: PASSED"
```

### Step 4: Test on TestPyPI (Optional but Recommended)
```powershell
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ pytest-html-dashboard==1.1.0

# Run quick test
pytest --version  # Should show plugin

# Test report generation
cd examples
pytest basic_usage.py --html=test_report.html --self-contained-html
# Verify test_report.html renders correctly
```

### Step 5: Upload to PyPI
```powershell
# Upload to production PyPI
twine upload dist/*

# You'll see output like:
# Uploading distributions to https://upload.pypi.org/legacy/
# Uploading pytest_html_dashboard-1.1.0-py3-none-any.whl
# Uploading pytest-html-dashboard-1.1.0.tar.gz
```

### Step 6: Verify PyPI Package
1. Visit: https://pypi.org/project/pytest-html-dashboard/
2. Verify version shows 1.1.0
3. Check package description renders correctly
4. Verify installation instructions

### Step 7: Test Fresh Installation
```powershell
# Create new virtual environment
python -m venv verify_env
.\verify_env\Scripts\activate

# Install from PyPI
pip install pytest-html-dashboard

# Verify installation
pip show pytest-html-dashboard
# Version: 1.1.0

# Quick functional test
cd examples
pytest basic_usage.py --html=verify_report.html --self-contained-html

# Clean up
deactivate
rm -rf verify_env
```

## GitHub Release

### Step 1: Create Git Tag
```bash
# Create annotated tag
git tag -a v1.1.0 -m "Release v1.1.0 - Complete HTML Enhancement System"

# Push tag to GitHub
git push origin v1.1.0
```

### Step 2: Create GitHub Release
1. Go to: https://github.com/nireshs/pytest-html-dashboard/releases/new
2. Select tag: v1.1.0
3. Release title: `v1.1.0 - Complete HTML Enhancement System`
4. Description: Copy from CHANGELOG.md v1.1.0 section
5. Attach files (optional):
   - dist/pytest_html_dashboard-1.1.0-py3-none-any.whl
   - dist/pytest-html-dashboard-1.1.0.tar.gz
6. Click "Publish release"

### Step 3: Update Repository
```powershell
# Ensure all changes are committed
git add .
git commit -m "Release v1.1.0"
git push origin main
```

## Post-Release Activities

### 1. Verify Installation
```powershell
# From any machine, verify installation works
pip install pytest-html-dashboard==1.1.0
pytest --version
```

### 2. Update Documentation Sites
If you have documentation hosted (ReadTheDocs, GitHub Pages):
- [ ] Trigger documentation rebuild
- [ ] Verify v1.1.0 docs are live
- [ ] Update any version references

### 3. Announce Release

#### PyPI Discussions
Post announcement in pytest discussions:
- Forum: https://github.com/pytest-dev/pytest/discussions
- Category: Plugins
- Title: "pytest-html-dashboard v1.1.0 Released - Chart.js Visualizations & Modern Dashboard"

#### Social Media / Communities
- [ ] Reddit: r/Python, r/pytest
- [ ] Dev.to article
- [ ] Twitter/X announcement
- [ ] LinkedIn post
- [ ] Company blog (if applicable)

#### Sample Announcement
```markdown
🎉 pytest-html-dashboard v1.1.0 Released!

New features:
✨ Chart.js visualizations (status distribution, pass rate, error categories)
🎨 Modern dashboard styling with gradients and responsive cards
📋 Comprehensive test results table with error details
🔍 Enhanced error reporting with suggested actions

Install: pip install pytest-html-dashboard

GitHub: https://github.com/nireshs/pytest-html-dashboard
PyPI: https://pypi.org/project/pytest-html-dashboard/

#pytest #python #testing #automation
```

### 4. Monitor Issues
- [ ] Watch GitHub issues for installation problems
- [ ] Respond to PyPI reviews/comments
- [ ] Check for compatibility reports

### 5. Update Project Status
- [ ] Close completed milestones on GitHub
- [ ] Create v1.2.0 milestone for future features
- [ ] Update project README badges (if needed)

## Troubleshooting

### Common Issues

#### "File already exists" on PyPI
```powershell
# You cannot re-upload same version. Increment version and rebuild.
# Edit pyproject.toml and setup.py: 1.1.0 -> 1.1.1
python -m build
twine upload dist/*
```

#### "Invalid credentials"
```powershell
# Verify ~/.pypirc or %USERPROFILE%\.pypirc
# Or use interactive login:
twine upload dist/* --username YOUR_USERNAME
```

#### Build Errors
```powershell
# Clean everything and rebuild
Remove-Item -Recurse -Force dist, build, *.egg-info
pip install --upgrade build setuptools wheel
python -m build
```

#### Import Errors After Installation
```powershell
# Verify package structure
pip show -f pytest-html-dashboard

# Reinstall
pip uninstall pytest-html-dashboard
pip install pytest-html-dashboard --no-cache-dir
```

## Rollback Procedure

If major issues are discovered after release:

### 1. Yank Release (PyPI)
```powershell
# Yank removes from default search but keeps available
# Use PyPI web interface or:
# (Yanking requires project maintainer access)
```

### 2. Release Patch Version
```powershell
# Quick fix in v1.1.1
# Edit files, increment version to 1.1.1
python -m build
twine upload dist/*
```

### 3. Communicate Issue
- Update GitHub release notes with known issues
- Post announcement about patch release
- Update documentation with workarounds

## Version Numbering

Following Semantic Versioning (SemVer):

- **MAJOR** (x.0.0): Incompatible API changes
- **MINOR** (1.x.0): New features, backward compatible
- **PATCH** (1.1.x): Bug fixes, backward compatible

**v1.1.0** is a MINOR release:
- Adds new features (Chart.js, enhanced styling)
- Fully backward compatible with v1.0.0
- No breaking changes

Next versions:
- v1.1.1 - Bug fixes only
- v1.2.0 - Next feature release
- v2.0.0 - Breaking changes (if needed)

## Success Criteria

Release is successful when:
- [x] Package appears on PyPI with correct version
- [x] `pip install pytest-html-dashboard` works globally
- [x] Generated reports show Chart.js visualizations
- [x] No critical issues reported within 48 hours
- [x] Documentation is accessible and accurate
- [x] GitHub release is published with notes

## Support Resources

- **PyPI Help**: https://pypi.org/help/
- **Twine Docs**: https://twine.readthedocs.io/
- **Python Packaging**: https://packaging.python.org/
- **Semantic Versioning**: https://semver.org/

## Contact

- **Maintainer**: Niresh Shanmugam
- **Email**: niresh.shanmugam@gmail.com
- **GitHub**: https://github.com/nireshs
- **Issues**: https://github.com/nireshs/pytest-html-dashboard/issues

---

**Last Updated**: November 22, 2025
**Document Version**: 1.0
**For Release**: v1.1.0
