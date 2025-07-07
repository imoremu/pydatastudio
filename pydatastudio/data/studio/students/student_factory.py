"""
Created on 24 Jun 2025

@author: imoreno
"""

import importlib
import logging
from typing import Dict, Any, Optional

from pydatastudio.data.studio.students.data_student_configuration import DataStudentConfiguration
from pydatastudio.data.studio.data_studio import AbstractStudent
from pydatastudio.data.studio.students.abstract_student_factory import AbstractStudentFactory

class StudentFactory(AbstractStudentFactory):
    """
    Responsible for creating student instances from a configuration dictionary.
    
    This factory centralizes the logic for interpreting the 'students'
    configuration block, dynamically importing student classes, and handling
    potential errors during instantiation.
    """
    def __init__(self, students_config: Dict[str, Any]):
        """Initializes the StudentFactory with its own logger."""        
        self.students_config = students_config or {}
        self.logger = logging.getLogger(self.__class__.__name__)

    def create_students(self) -> Dict[str, AbstractStudent]:
        """
        Creates all student instances from a students configuration block.

        :param students_config: The dictionary from the YAML file under the 'students' key.
        :return: A dictionary mapping each student's name to its created object instance.
                 e.g., {'StudentOneName': StudentOneObject, ...}
        """
        created_students = {}
        
        for student_name, student_details in self.students_config.items():
            student_obj = self._create_one_student(student_name, student_details)
            if student_obj:
                created_students[student_name] = student_obj
        
        return created_students

    def _create_one_student(self, name: str, details: Dict[str, Any]) -> Optional[AbstractStudent]:
        """
        (Internal method) Creates a single student instance from its details.

        This method contains the core logic for dynamic import and instantiation,
        wrapped in robust error handling.

        :param name: The name of the student instance (used for logging).
        :param details: The configuration dictionary for this specific student.
        :return: A DataStudent object instance, or None if creation fails.
        """
        class_path = details.get("class")

        if not class_path:
            self.logger.warning(f"Student '{name}' in configuration is missing the 'class' key. Skipping.")
            raise InvalidStudentConfigurationException("Student configuration is missing the 'class' key.")
        
        try:
            module_name, class_name = class_path.rsplit('.', 1)                        
            module = importlib.import_module(module_name)                        
            StudentClass = getattr(module, class_name)
                        
            student_config = DataStudentConfiguration(details.get("config"))
                        
            student_obj = StudentClass(student_config)
            
            self.logger.info(f"Successfully created student '{name}' from class {class_path}")
            return student_obj

        except (ModuleNotFoundError, ImportError) as e:
            self.logger.error(f"Could not import module for student '{name}' at path '{class_path}'. Please check the path. Error: {e}. Skipping.")
            raise InvalidStudentConfigurationException(f"Could not import module for student '{name}' at path '{class_path}'.") from e
        
        except AttributeError as e:
            self.logger.error(f"Could not find class '{class_name}' in module '{module_name}' for student '{name}'. Please check the class name. Error: {e}. Skipping.")
            raise InvalidStudentConfigurationException(f"Could not find class '{class_name}' in module '{module_name}' for student '{name}'.") from e
        
        except Exception as e:
            self.logger.error(f"An unexpected error occurred while creating student '{name}'. Error: {e}. Skipping.")
            raise InvalidStudentConfigurationException(f"An unexpected error occurred while creating student '{name}'.") from e
        

# Exceptions
class InvalidStudentConfigurationException(Exception):
    pass
    
