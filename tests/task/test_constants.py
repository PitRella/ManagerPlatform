from typing import TYPE_CHECKING
from django.test import TestCase

from task.constants import (
    TASK_TEXT_MIN_LENGTH,
    TASK_TEXT_MAX_LENGTH,
    TASK_PRIORITY_MIN,
    TASK_PRIORITY_MAX,
    DEFAULT_TASKS_PER_PAGE,
    MAX_TASKS_PER_PAGE,
    MIN_SEARCH_QUERY_LENGTH,
    MAX_SEARCH_QUERY_LENGTH,
    ERROR_TASK_TEXT_EMPTY,
    ERROR_TASK_TEXT_TOO_SHORT,
    ERROR_TASK_TEXT_TOO_LONG,
    ERROR_TASK_TEXT_INVALID_CHARS,
    ERROR_TASK_NOT_FOUND,
    ERROR_TASK_NO_PERMISSION,
    ERROR_PROJECT_NOT_FOUND,
    ERROR_TASK_PRIORITY_INVALID,
    ERROR_TASK_REORDER_FAILED,
    ERROR_TASK_TOGGLE_FAILED,
)

if TYPE_CHECKING:
    pass


class TaskConstantsTest(TestCase):
    """Test cases for Task constants."""

    def test_text_length_constants(self) -> None:
        """Test text length constants."""
        self.assertEqual(TASK_TEXT_MIN_LENGTH, 1)
        self.assertEqual(TASK_TEXT_MAX_LENGTH, 64)
        self.assertGreater(TASK_TEXT_MAX_LENGTH, TASK_TEXT_MIN_LENGTH)

    def test_priority_constants(self) -> None:
        """Test priority constants."""
        self.assertEqual(TASK_PRIORITY_MIN, 1)
        self.assertEqual(TASK_PRIORITY_MAX, 1000)
        self.assertGreater(TASK_PRIORITY_MAX, TASK_PRIORITY_MIN)

    def test_pagination_constants(self) -> None:
        """Test pagination constants."""
        self.assertEqual(DEFAULT_TASKS_PER_PAGE, 20)
        self.assertEqual(MAX_TASKS_PER_PAGE, 100)
        self.assertGreater(MAX_TASKS_PER_PAGE, DEFAULT_TASKS_PER_PAGE)

    def test_search_constants(self) -> None:
        """Test search constants."""
        self.assertEqual(MIN_SEARCH_QUERY_LENGTH, 1)
        self.assertEqual(MAX_SEARCH_QUERY_LENGTH, 50)
        self.assertGreater(MAX_SEARCH_QUERY_LENGTH, MIN_SEARCH_QUERY_LENGTH)

    def test_error_message_constants(self) -> None:
        """Test error message constants."""
        # Test that all error constants are strings
        error_constants: list[str] = [
            ERROR_TASK_TEXT_EMPTY,
            ERROR_TASK_TEXT_TOO_SHORT,
            ERROR_TASK_TEXT_TOO_LONG,
            ERROR_TASK_TEXT_INVALID_CHARS,
            ERROR_TASK_NOT_FOUND,
            ERROR_TASK_NO_PERMISSION,
            ERROR_PROJECT_NOT_FOUND,
            ERROR_TASK_PRIORITY_INVALID,
            ERROR_TASK_REORDER_FAILED,
            ERROR_TASK_TOGGLE_FAILED,
        ]
        
        for error_constant in error_constants:
            self.assertIsInstance(error_constant, str)
            self.assertGreater(len(error_constant), 0)

    def test_error_message_content(self) -> None:
        """Test error message content."""
        self.assertIn("empty", ERROR_TASK_TEXT_EMPTY.lower())
        self.assertIn("short", ERROR_TASK_TEXT_TOO_SHORT.lower())
        self.assertIn("long", ERROR_TASK_TEXT_TOO_LONG.lower())
        self.assertIn("invalid", ERROR_TASK_TEXT_INVALID_CHARS.lower())
        self.assertIn("not found", ERROR_TASK_NOT_FOUND.lower())
        self.assertIn("permission", ERROR_TASK_NO_PERMISSION.lower())
        self.assertIn("not found", ERROR_PROJECT_NOT_FOUND.lower())
        self.assertIn("priority", ERROR_TASK_PRIORITY_INVALID.lower())
        self.assertIn("reorder", ERROR_TASK_REORDER_FAILED.lower())
        self.assertIn("toggle", ERROR_TASK_TOGGLE_FAILED.lower())

    def test_error_message_formatting(self) -> None:
        """Test error message formatting with constants."""
        # Test that error messages contain the actual constant values
        self.assertIn(str(TASK_TEXT_MIN_LENGTH), ERROR_TASK_TEXT_TOO_SHORT)
        self.assertIn(str(TASK_TEXT_MAX_LENGTH), ERROR_TASK_TEXT_TOO_LONG)
        self.assertIn(str(TASK_PRIORITY_MIN), ERROR_TASK_PRIORITY_INVALID)
        self.assertIn(str(TASK_PRIORITY_MAX), ERROR_TASK_PRIORITY_INVALID)

    def test_constant_types(self) -> None:
        """Test that all constants have correct types."""
        # Numeric constants
        self.assertIsInstance(TASK_TEXT_MIN_LENGTH, int)
        self.assertIsInstance(TASK_TEXT_MAX_LENGTH, int)
        self.assertIsInstance(TASK_PRIORITY_MIN, int)
        self.assertIsInstance(TASK_PRIORITY_MAX, int)
        self.assertIsInstance(DEFAULT_TASKS_PER_PAGE, int)
        self.assertIsInstance(MAX_TASKS_PER_PAGE, int)
        self.assertIsInstance(MIN_SEARCH_QUERY_LENGTH, int)
        self.assertIsInstance(MAX_SEARCH_QUERY_LENGTH, int)

    def test_constant_values_positive(self) -> None:
        """Test that all numeric constants are positive."""
        numeric_constants: list[int] = [
            TASK_TEXT_MIN_LENGTH,
            TASK_TEXT_MAX_LENGTH,
            TASK_PRIORITY_MIN,
            TASK_PRIORITY_MAX,
            DEFAULT_TASKS_PER_PAGE,
            MAX_TASKS_PER_PAGE,
            MIN_SEARCH_QUERY_LENGTH,
            MAX_SEARCH_QUERY_LENGTH,
        ]
        
        for constant in numeric_constants:
            self.assertGreater(constant, 0)

    def test_constant_relationships(self) -> None:
        """Test relationships between related constants."""
        # Text length constraints
        self.assertLessEqual(TASK_TEXT_MIN_LENGTH, TASK_TEXT_MAX_LENGTH)
        
        # Priority constraints
        self.assertLessEqual(TASK_PRIORITY_MIN, TASK_PRIORITY_MAX)
        
        # Pagination constraints
        self.assertLessEqual(DEFAULT_TASKS_PER_PAGE, MAX_TASKS_PER_PAGE)
        
        # Search constraints
        self.assertLessEqual(MIN_SEARCH_QUERY_LENGTH, MAX_SEARCH_QUERY_LENGTH)

    def test_constant_boundaries(self) -> None:
        """Test constant boundary values."""
        # Test minimum values
        self.assertEqual(TASK_TEXT_MIN_LENGTH, 1)
        self.assertEqual(TASK_PRIORITY_MIN, 1)
        self.assertEqual(MIN_SEARCH_QUERY_LENGTH, 1)
        
        # Test reasonable maximum values
        self.assertLessEqual(TASK_TEXT_MAX_LENGTH, 1000)  # Reasonable max
        self.assertLessEqual(TASK_PRIORITY_MAX, 10000)    # Reasonable max
        self.assertLessEqual(MAX_TASKS_PER_PAGE, 1000)    # Reasonable max
        self.assertLessEqual(MAX_SEARCH_QUERY_LENGTH, 1000)  # Reasonable max

    def test_error_message_uniqueness(self) -> None:
        """Test that error messages are unique."""
        error_messages: list[str] = [
            ERROR_TASK_TEXT_EMPTY,
            ERROR_TASK_TEXT_TOO_SHORT,
            ERROR_TASK_TEXT_TOO_LONG,
            ERROR_TASK_TEXT_INVALID_CHARS,
            ERROR_TASK_NOT_FOUND,
            ERROR_TASK_NO_PERMISSION,
            ERROR_PROJECT_NOT_FOUND,
            ERROR_TASK_PRIORITY_INVALID,
            ERROR_TASK_REORDER_FAILED,
            ERROR_TASK_TOGGLE_FAILED,
        ]
        
        # Check that all messages are unique
        unique_messages: set[str] = set(error_messages)
        self.assertEqual(len(error_messages), len(unique_messages))

    def test_constant_importability(self) -> None:
        """Test that all constants can be imported."""
        # This test ensures that all constants are properly defined
        # and can be imported without errors
        constants_to_test: list = [
            TASK_TEXT_MIN_LENGTH,
            TASK_TEXT_MAX_LENGTH,
            TASK_PRIORITY_MIN,
            TASK_PRIORITY_MAX,
            DEFAULT_TASKS_PER_PAGE,
            MAX_TASKS_PER_PAGE,
            MIN_SEARCH_QUERY_LENGTH,
            MAX_SEARCH_QUERY_LENGTH,
            ERROR_TASK_TEXT_EMPTY,
            ERROR_TASK_TEXT_TOO_SHORT,
            ERROR_TASK_TEXT_TOO_LONG,
            ERROR_TASK_TEXT_INVALID_CHARS,
            ERROR_TASK_NOT_FOUND,
            ERROR_TASK_NO_PERMISSION,
            ERROR_PROJECT_NOT_FOUND,
            ERROR_TASK_PRIORITY_INVALID,
            ERROR_TASK_REORDER_FAILED,
            ERROR_TASK_TOGGLE_FAILED,
        ]
        
        # If we get here, all constants are importable
        self.assertEqual(len(constants_to_test), 18)
