# Example: Basic Usage of pytest-enhanced-reporter

import pytest


class TestBasicExamples:
    """Basic test examples to demonstrate pytest-enhanced-reporter features."""

    def test_simple_pass(self):
        """A simple passing test."""
        assert 1 + 1 == 2

    def test_with_multiple_assertions(self):
        """Test with multiple assertions."""
        result = [1, 2, 3, 4, 5]
        assert len(result) == 5
        assert sum(result) == 15
        assert max(result) == 5
        assert min(result) == 1

    def test_string_operations(self):
        """Test string operations."""
        text = "pytest-enhanced-reporter"
        assert "pytest" in text
        assert text.startswith("pytest")
        assert text.endswith("reporter")

    def test_dictionary_operations(self):
        """Test dictionary operations."""
        data = {"name": "Test", "version": "1.0", "active": True}
        assert data["name"] == "Test"
        assert data["version"] == "1.0"
        assert data["active"] is True

    def test_list_operations(self):
        """Test list operations."""
        numbers = [1, 2, 3, 4, 5]
        assert 3 in numbers
        assert len(numbers) == 5
        assert numbers[0] == 1
        assert numbers[-1] == 5


class TestErrorDemonstrations:
    """Tests that demonstrate error reporting features."""

    def test_assertion_failure(self):
        """This test will fail with an assertion error."""
        expected = 10
        actual = 5
        assert actual == expected, f"Expected {expected}, but got {actual}"

    @pytest.mark.skip(reason="Demonstrating skipped tests")
    def test_skipped_test(self):
        """This test will be skipped."""
        assert False

    def test_timeout_simulation(self):
        """Test that simulates a timeout scenario."""
        import time
        timeout = 0.1
        start = time.time()
        time.sleep(0.05)
        elapsed = time.time() - start
        assert elapsed < timeout, f"Operation took {elapsed:.3f}s, exceeded timeout of {timeout}s"

    def test_type_error_demo(self):
        """Test demonstrating type error."""
        def add_numbers(a, b):
            return a + b

        result = add_numbers(5, 10)
        assert result == 15

    def test_import_error_demo(self):
        """Test demonstrating successful imports."""
        import os
        import sys
        import json

        assert os.path.exists(".")
        assert sys.version_info.major >= 3


class TestDataDrivenExamples:
    """Data-driven test examples."""

    @pytest.mark.parametrize("input,expected", [
        (1, 2),
        (2, 4),
        (3, 6),
        (4, 8),
        (5, 10),
    ])
    def test_multiply_by_two(self, input, expected):
        """Test multiplication by two with various inputs."""
        assert input * 2 == expected

    @pytest.mark.parametrize("text,should_be_uppercase", [
        ("HELLO", True),
        ("hello", False),
        ("Hello", False),
        ("WORLD", True),
    ])
    def test_string_case(self, text, should_be_uppercase):
        """Test string case checking."""
        assert text.isupper() == should_be_uppercase


if __name__ == "__main__":
    # Run tests with enhanced reporter
    pytest.main([
        __file__,
        "--html=report.html",
        "--self-contained-html",
        "-v"
    ])
