"""
Created on 25 Jun 2025

@author: imoreno
"""
import unittest
from unittest.mock import patch, Mock, MagicMock

from pydatastudio.data.studio.config_studio_builder import ConfigStudioBuilder
from pydatastudio.data.studio.data_studio import DataStudio, AbstractStudent
from pydatastudio.data.studio.environment.data_studio_environment import DataStudioEnvironment
from pydatastudio.data.studio.students.abstract_student_factory import AbstractStudentFactory


class TestConfigStudioBuilder(unittest.TestCase):

    @patch('importlib.import_module')
    @patch('pydatastudio.data.studio.data_studio.DataStudio.add_student')
    def test_build_studio_success(self, mock_add_student, mock_import_module):
        """
        Tests that build_studio successfully constructs a DataStudio instance
        with students from the configured factory.
        """
        # --- Arrange ---
        # 1. Mock the environment to return a fake factory path
        mock_env = Mock(spec=DataStudioEnvironment)
        mock_env.get_student_factory_class_name.return_value = 'fake.factory.path.StudentFactory'

        # 2. Mock the student objects that the factory will "create"
        mock_student_1 = Mock(spec=AbstractStudent)
        mock_student_2 = Mock(spec=AbstractStudent)
        student_objects = {
            "student_one": mock_student_1,
            "student_two": mock_student_2
        }

        # 3. Mock the factory instance and its create_students method
        mock_factory_instance = Mock(spec=AbstractStudentFactory)
        mock_factory_instance.create_students.return_value = student_objects

        # 4. Mock the factory class that will be returned by the module
        mock_factory_class = Mock(return_value=mock_factory_instance)

        # 5. Mock the imported module to contain the factory class
        mock_module = MagicMock()
        setattr(mock_module, 'StudentFactory', mock_factory_class)
        mock_import_module.return_value = mock_module

        # --- Act ---
        builder = ConfigStudioBuilder(environment=mock_env)
        studio = builder.build_studio()

        # --- Assert ---
        self.assertIsInstance(studio, DataStudio)
        mock_env.get_student_factory_class_name.assert_called_once()
        mock_import_module.assert_called_once_with('fake.factory.path')
        mock_factory_class.assert_called_once_with()
        mock_factory_instance.create_students.assert_called_once()

        # Verify that add_student was called for each created student
        self.assertEqual(mock_add_student.call_count, 2)
        mock_add_student.assert_any_call("student_one", mock_student_1)
        mock_add_student.assert_any_call("student_two", mock_student_2)

    def test_build_studio_raises_error_if_no_factory_configured(self):
        """
        Tests that build_studio raises a ValueError if the factory path is not configured.
        """
        # --- Arrange ---
        mock_env = Mock(spec=DataStudioEnvironment)
        mock_env.get_student_factory_class_name.return_value = ""

        # --- Act & Assert ---
        builder = ConfigStudioBuilder(environment=mock_env)
        with self.assertRaisesRegex(ValueError, "Student factory 'class' not defined in environment configuration."):
            builder.build_studio()

if __name__ == "__main__":
    unittest.main()

