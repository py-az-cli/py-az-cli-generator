"""Tests for module pyaz."""
import logging
import sys
import unittest

from output import pyaz

# log to stdout
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

class Constants:
    """Constants for use in tests."""

    TEST_GROUP_NAME = "pyaz-test-group"


class TestIntegration(unittest.TestCase):
    """Integration test class."""

    def test_az_version(self):
        """Test for pyaz.version."""
        result = pyaz.version()
        self.assertIsInstance(result, dict)

        # test that the result has a key named azure-cli
        version = result["azure-cli"]
        self.assertIsNotNone(version)

    def test_az_version_negative(self):
        """Test that calling pyaz.version with an argument raises an error."""
        with self.assertRaises(TypeError):
            pyaz.version("test") # pylint: disable=[too-many-function-args]

    def test_az_account_list(self):
        """Test for az account list."""
        result = pyaz.account.list()
        self.assertIsInstance(result, list)

        # test that the first item in the result has a key named homeTenantId
        tenant_id = result[0]["homeTenantId"]
        self.assertIsNotNone(tenant_id)

    def test_az_group_create_exists_and_delete(self):
        """Test for az group create, exists and delete."""
        try:
            result = pyaz.group.create(
                location="eastus", name="test_az_group"
            )
            self.assertEqual("test_az_group", result["name"])

            # assert that the group exists
            self.assertTrue(pyaz.group.exists(name="test_az_group"))

        finally:
            pyaz.group.delete(name="test_az_group", yes=True, no_wait=True)

        # assert that the group no longer exists by attempted to show it
        with self.assertRaises(Exception):
            result = pyaz.group.show(name="test_az_group")

    def test_az_group_with_tags(self):
        """Test az group create with support for multiple tags."""
        try:
            pyaz.group.create(
                location="eastus",
                name="test_az_group_with_tags",
                tags="tag1=value1 'tag2=value 2'"
            )
            group = pyaz.group.show(name="test_az_group_with_tags")
            print(group)
            expected = {"tag1":"value1", "tag2":"value 2"}
            actual = group['tags']
            print(expected)
            print(actual)
            self.assertDictEqual(expected, actual)

        finally:
            pyaz.group.delete(name="test_az_group_with_tags", yes=True, no_wait=True)

    def test_az_parameter_with_spaces(self):
        """Test that az command can handle parameter with spaces in it."""
        try:
            pyaz.group.create(
                location="eastus",
                name="test_az_parameter_with_spaces"
            )

            result = pyaz.ts.create(
                name="test_template",
                resource_group="test_az_parameter_with_spaces",
                description="this is a test description"
            )

            self.assertEqual(result['description'], 'this is a test description')

        finally:
            pyaz.group.delete(name="test_az_parameter_with_spaces", yes=True, no_wait=True)
