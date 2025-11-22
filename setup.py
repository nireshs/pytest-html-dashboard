#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pytest-html-dashboard
A comprehensive pytest plugin for beautiful dashboard-style HTML reports with charts, error analysis, and visual insights.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pytest-html-dashboard",
    version="1.0.0",
    author="Niresh Shanmugam",
    author_email="niresh.shanmugam@gmail.com",
    description="Beautiful dashboard-style HTML reports for pytest with charts, error analysis, and visual insights",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nireshs/pytest-html-dashboard",
    project_urls={
        "Bug Tracker": "https://github.com/nireshs/pytest-html-dashboard/issues",
        "Documentation": "https://github.com/nireshs/pytest-html-dashboard#readme",
        "Source Code": "https://github.com/nireshs/pytest-html-dashboard",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pytest>=7.0.0",
        "pytest-html>=4.0.0",
        "pytest-metadata>=3.0.0",
        "colorama>=0.4.0",
        "prettytable>=3.0.0",
        "pyyaml>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "pytest11": [
            "dashboard = pytest_html_dashboard.plugin",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "pytest",
        "plugin",
        "html",
        "report",
        "charts",
        "enhanced",
        "testing",
        "qa",
        "automation",
    ],
)
