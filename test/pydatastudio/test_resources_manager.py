"""
Created on 2 ene. 2019

@author: imoreno
"""
import unittest
import os
import shutil

from pydatastudio import resources_manager


class Test(unittest.TestCase):
    def testGetRelativeConfigFile(self):
        conf_file = os.path.join(
            ".", "test", "pydatastudio", "conf", "test.file"
        )

        expected = os.path.join(os.path.dirname(__file__), "conf", "test.file")

        result = resources_manager.get_resource_path(conf_file)

        self.assertFalse(os.path.isabs(conf_file), "Input path is absolute")

        self.assertEqual(
            result,
            expected,
            "Resource File should be {0} and is {1}".format(expected, result),
        )
        pass

    def testGetAbsoluteConfigFile(self):
        conf_file = os.path.join(os.path.abspath(__file__), "conf", "test.file")

        expected = os.path.abspath(conf_file)

        result = resources_manager.get_resource_path(conf_file)

        self.assertTrue(os.path.isabs(conf_file), "Input path is not absolute")

        self.assertEqual(
            result,
            expected,
            "Resource File should be {0} and is {1}".format(expected, result),
        )

    def testCreateDir(self):
        DEFAULT_CONF_FILE = resources_manager.get_resource_path(
            os.path.join("output", "test_create_dir", "test.yaml")
        )

        path = os.path.dirname(DEFAULT_CONF_FILE)

        if os.path.exists(path):
            shutil.rmtree(path)

        resources_manager.create_path_if_needed(DEFAULT_CONF_FILE)

        self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
