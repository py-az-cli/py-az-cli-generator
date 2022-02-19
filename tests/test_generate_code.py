"""Tests for module generate_code."""
import unittest
import requests
import yaml
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

    def test_pythonize_name_with_leading_number(self):
        """Test for name that starts with a number, adds an _ to the name"""
        cli_name = "404-document"
        expected = "_404_document"
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

    @unittest.skip("this hasn't been implemented yet")
    def test_get_commands_all(self):
        """Test that get_commands returns all the existing az top-level commands."""
        commands = generate_code.get_commands()

        #for command, command_group in commands.items():
        all_commands = get_all_az_commands()

        self.assertTrue(False, "Need to finish this test")
        #for command in all_commands:
        #   self.assertIn()

        #self.assertListEqual(commands, all_commands)

    def test_get_az_function_def(self):
        """Test method that returns function body given arguments."""
        actual = generate_code._get_az_function_def("pyaz version", "version", "", "documentation")
        print(actual)
        print("hello")

    @unittest.skip("not implemented yet.")
    def test_generate_code(self):
        """Test main generate_code function."""

        mock_commands = {}

        generate_code.get_commands = lambda : mock_commands



def get_all_az_commands():
    """Helper function that returns list of all the az top level commands in pyaz format"""
    #get list of commands from github docs
    response = requests.get("https://raw.githubusercontent.com/MicrosoftDocs/azure-docs-cli/main/latest/docs-ref-autogen/service-page/List%20A%20-%20Z.yml")
    docs = yaml.safe_load(response.content)
    
    output = []
    for command in docs['commands']:
        # strip off leading "az_"
        command = command[3:]
        command = generate_code.pythonize_name(command)
        output.append(command)
    return output

class TestHelpers(unittest.TestCase):

    def test_get_all_az_commands(self):
        """Tests that helper class returns list of az commands."""
        commands = get_all_az_commands()
        self.assertIsInstance(commands, list)
        self.assertIn("account", commands)
        self.assertIn("vm", commands)
