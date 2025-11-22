"""
Comprehensive test suite to demonstrate all pytest-html-dashboard features.
This test file includes examples of:
- Passed tests
- Failed tests with assertions
- Skipped tests
- Tests with various error types
- Tests with custom metadata
"""

import pytest
import time


class TestBasicFeatures:
    """Basic test scenarios demonstrating pass/fail/skip status."""

    def test_simple_pass(self):
        """A simple passing test."""
        assert 1 + 1 == 2
        assert "hello".upper() == "HELLO"

    def test_math_operations_pass(self):
        """Test various math operations - should pass."""
        assert 10 > 5
        assert 100 / 4 == 25
        assert 2 ** 8 == 256

    def test_string_operations_pass(self):
        """Test string operations - should pass."""
        text = "pytest dashboard"
        assert text.startswith("pytest")
        assert "dash" in text
        assert len(text) == 16

    @pytest.mark.skip(reason="Demonstrating skip functionality")
    def test_skipped_example(self):
        """This test is intentionally skipped."""
        assert False, "This should never execute"

    @pytest.mark.skipif(True, reason="Conditional skip example")
    def test_conditional_skip(self):
        """Conditionally skipped test."""
        assert False


class TestFailureScenarios:
    """Tests demonstrating various failure scenarios."""

    def test_assertion_failure(self):
        """Test with assertion error."""
        expected_value = 100
        actual_value = 50
        assert actual_value == expected_value, f"Expected {expected_value}, got {actual_value}"

    def test_comparison_failure(self):
        """Test with comparison failure."""
        data = {"name": "John", "age": 30}
        assert data["age"] == 25, "Age mismatch in user data"

    def test_list_assertion_failure(self):
        """Test with list comparison failure."""
        expected_list = [1, 2, 3, 4, 5]
        actual_list = [1, 2, 3, 4, 6]
        assert actual_list == expected_list, "List elements don't match"

    def test_type_error_example(self):
        """Test that causes a TypeError."""
        result = "string" + 123

    def test_zero_division_error(self):
        """Test that causes ZeroDivisionError."""
        value = 10 / 0

    def test_key_error_example(self):
        """Test that causes KeyError."""
        data = {"name": "Alice"}
        email = data["email"]  # Key doesn't exist

    def test_index_error_example(self):
        """Test that causes IndexError."""
        items = [1, 2, 3]
        value = items[10]

    def test_attribute_error_example(self):
        """Test that causes AttributeError."""
        text = "hello"
        text.non_existent_method()


class TestWithDurations:
    """Tests with different execution durations."""

    def test_fast_execution(self):
        """Quick test - should complete in milliseconds."""
        assert True

    def test_medium_duration(self):
        """Test with medium duration."""
        time.sleep(0.1)
        assert sum(range(100)) == 4950

    def test_slow_execution(self):
        """Test with longer duration."""
        time.sleep(0.3)
        total = 0
        for i in range(1000):
            total += i
        assert total == 499500


class TestComplexScenarios:
    """More complex test scenarios."""

    def test_nested_data_structures(self):
        """Test with nested dictionaries and lists."""
        config = {
            "server": {
                "host": "localhost",
                "port": 8080,
                "ssl": True
            },
            "database": {
                "host": "db.example.com",
                "credentials": ["user", "password"]
            }
        }
        assert config["server"]["port"] == 8080
        assert config["database"]["credentials"][0] == "user"

    def test_multiple_assertions(self):
        """Test with multiple assertions to check various conditions."""
        user = {
            "username": "testuser",
            "email": "test@example.com",
            "active": True,
            "roles": ["user", "admin"]
        }

        assert user["username"] == "testuser"
        assert "@" in user["email"]
        assert user["active"] is True
        assert "admin" in user["roles"]
        assert len(user["roles"]) == 2

    @pytest.mark.xfail(reason="Known issue - feature not implemented yet")
    def test_expected_failure(self):
        """Test that is expected to fail."""
        assert False, "This failure is expected"

    def test_boundary_conditions(self):
        """Test boundary conditions."""
        assert 0 == 0  # Lower boundary
        assert 999999 < 1000000  # Upper boundary
        assert -1 < 0  # Negative boundary


class TestDataValidation:
    """Tests for data validation scenarios."""

    def test_email_validation_pass(self):
        """Valid email format."""
        email = "user@example.com"
        assert "@" in email
        assert "." in email.split("@")[1]

    def test_email_validation_fail(self):
        """Invalid email format - should fail."""
        email = "invalid-email"
        assert "@" in email, "Email must contain @ symbol"

    def test_phone_number_validation(self):
        """Phone number format validation."""
        phone = "123-456-7890"
        parts = phone.split("-")
        assert len(parts) == 3, "Phone number should have 3 parts"
        assert len(parts[0]) == 3, "Area code should be 3 digits"

    def test_password_strength_fail(self):
        """Password strength validation - should fail."""
        password = "weak"
        assert len(password) >= 8, "Password must be at least 8 characters"
        assert any(c.isupper()
                   for c in password), "Password must contain uppercase"
        assert any(c.isdigit()
                   for c in password), "Password must contain digit"


class TestAPISimulation:
    """Simulated API testing scenarios."""

    def test_api_status_code_200(self):
        """Simulate successful API response."""
        # Simulated response
        status_code = 200
        assert status_code == 200, f"Expected 200, got {status_code}"

    def test_api_status_code_404(self):
        """Simulate not found API response - should fail."""
        status_code = 404
        assert status_code == 200, f"API returned {status_code} instead of 200"

    def test_api_response_structure(self):
        """Validate API response structure."""
        response = {
            "status": "success",
            "data": {
                "id": 123,
                "name": "Test Item"
            },
            "timestamp": "2024-01-01T00:00:00Z"
        }

        assert "status" in response
        assert response["status"] == "success"
        assert "data" in response
        assert response["data"]["id"] == 123

    def test_api_response_validation_fail(self):
        """API response validation failure."""
        response = {"status": "error", "message": "Not found"}
        assert response["status"] == "success", f"API call failed: {
            response.get('message')}"


@pytest.mark.performance
class TestPerformance:
    """Performance-related tests."""

    def test_algorithm_performance(self):
        """Test algorithm performance."""
        start = time.time()

        # Simulate some computation
        result = sum(i * i for i in range(10000))

        duration = time.time() - start
        assert result == 333283335000
        assert duration < 1.0, f"Algorithm took {
            duration:.3f}s, expected < 1.0s"

    def test_memory_intensive_operation(self):
        """Test with larger data structures."""
        large_list = list(range(100000))
        assert len(large_list) == 100000
        assert large_list[0] == 0
        assert large_list[-1] == 99999


# Fixtures for test data
@pytest.fixture
def sample_user_data():
    """Fixture providing sample user data."""
    return {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "active": True
    }


@pytest.fixture
def sample_database_config():
    """Fixture providing database configuration."""
    return {
        "host": "localhost",
        "port": 5432,
        "database": "testdb",
        "username": "testuser"
    }


class TestWithFixtures:
    """Tests using pytest fixtures."""

    def test_user_data_fixture(self, sample_user_data):
        """Test using user data fixture."""
        assert sample_user_data["username"] == "testuser"
        assert sample_user_data["active"] is True

    def test_database_config_fixture(self, sample_database_config):
        """Test using database config fixture."""
        assert sample_database_config["host"] == "localhost"
        assert sample_database_config["port"] == 5432

    def test_fixture_data_modification_fail(self, sample_user_data):
        """Test fixture data - should fail."""
        sample_user_data["email"] = "wrong@example.com"
        assert sample_user_data["email"] == "test@example.com", "Email was modified"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
