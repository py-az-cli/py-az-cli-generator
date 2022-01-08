"""Tests for module generate_code."""
import unittest
import generate_code

# pylint: disable=protected-access

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

    def test_get_commands(self):
        """Test function that returns dict of dict of commands keyed by the command path."""
        commands = generate_code.get_commands()
        self.assertIsInstance(commands, dict)

        #check that pyaz command is present
        pyaz = commands['pyaz']
        self.assertEqual(pyaz['version'].name , "version")

        #check that _subcommands list is also present
        subcommands = pyaz['_subcommands']
        self.assertIsInstance(subcommands, list)
        self.assertIn("storage", subcommands)
        self.assertIn("group", subcommands)

        #check that pyaz.storage.account.create command is present
        self.assertEqual(commands['pyaz/storage/account']['create'].name, "storage account create")

        #check that py.group.show command is present
        self.assertEqual(commands['pyaz/group']['show'].name, "group show")

    def test_get_az_function_def(self):
        """Test method that returns function body given arguments."""
        actual = generate_code._get_az_function_def("pyaz version", "version", "", "documentation")
        print(actual)
        print("hello")
