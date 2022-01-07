"""Tests for module generate_code."""
import unittest
import generate_code


class TestUnit(unittest.TestCase):
    """Unit tests for generate_code."""

    def test_pythonize_name(self):
        """Test function that converts cli name to pythonic name."""
        cli_name = "--cli-name"
        expected = "cli_name"
        actual = generate_code.pythonize_name(cli_name)
        self.assertEqual(expected, actual)

    def test_pythonize_name_with_keyword(self):
        """Test for convert cli name to pythonic name for case where name is a python keyword."""
        cli_name = "--global"
        expected = "global_"
        actual = generate_code.pythonize_name(cli_name)
        self.assertEqual(expected, actual)
