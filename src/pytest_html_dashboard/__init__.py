#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
pytest-dashboard: Beautiful dashboard-style HTML reports for pytest
"""

__version__ = "1.0.0"
__author__ = "pytest-dashboard contributors"
__license__ = "MIT"

from .config import ReporterConfig
from .error_reporting import ErrorClassifier, ErrorDetails

__all__ = [
    "__version__",
    "ReporterConfig",
    "ErrorClassifier",
    "ErrorDetails",
]
