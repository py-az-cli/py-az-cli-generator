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
                location="eastus", name=Constants.TEST_GROUP_NAME
            )
            self.assertEqual(Constants.TEST_GROUP_NAME, result["name"])

            # assert that the group exists
            self.assertTrue(pyaz.group.exists(name=Constants.TEST_GROUP_NAME))

        finally:
            pyaz.group.delete(name=Constants.TEST_GROUP_NAME, yes=True, no_wait=True)

        # assert that the group no longer exists by attempted to show it
        with self.assertRaises(Exception):
            result = pyaz.group.show(name=Constants.TEST_GROUP_NAME)

    def test_az_group_with_tags(self):
        """Test az group create with support for multiple tags."""
        try:
            pyaz.group.create(
                location="eastus",
                name=Constants.TEST_GROUP_NAME,
                tags="tag1=value1 'tag2=value 2'"
            )
            group = pyaz.group.show(name=Constants.TEST_GROUP_NAME)
            print(group)
            expected = {"tag1":"value1", "tag2":"value 2"}
            actual = group['tags']
            print(expected)
            print(actual)
            self.assertDictEqual(expected, actual)

        finally:
            pyaz.group.delete(name=Constants.TEST_GROUP_NAME, yes=True, no_wait=True)
