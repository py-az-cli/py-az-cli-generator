"""Tests for pyaz_utils module."""
import unittest
import pyaz_utils


class TestUnit(unittest.TestCase):
    """Unit tests for pyaz_utils."""

    # pylint: disable=protected-access

    def test_call_az(self):
        """Test happy path for _call_az function with version."""
        parameters = {}
        result = pyaz_utils._call_az("az version", parameters)
        version = result["azure-cli"]
        self.assertIsNotNone(version)
        self.assertEqual(version, "2.31.0")

    def test_get_cli_name(self):
        """Test that parameter name is converted back to cli format."""
        cli_name = pyaz_utils._get_cli_param_name("test_parameter_name_")
        self.assertEqual("--test-parameter-name", cli_name)

    def test_get_cli_name_with_leading_number(self):
        """Test that parameter name with leading number is returned back properly."""
        cli_name = pyaz_utils._get_cli_param_name("_404_document")
        self.assertEqual("--404-document", cli_name)
        

    def test_get_params(self):
        """
        Test function that given a dictionary of parameters.

        Returns a cli formatted string of the parameters names and values
        note: boolean doesn't have a value and false boolean is removed
        """
        params = {
            "parameter_int": "1",
            "parameter_string": "string",
            "parameter_bool_true": True,
            "parameter_bool_false": False
        }
        expected = [
            "--parameter-int",
            '"1"',
            "--parameter-string",
            '"string"',
            "--parameter-bool-true",
        ]
        actual = pyaz_utils._get_params(params)
        self.assertEqual(expected, actual)
