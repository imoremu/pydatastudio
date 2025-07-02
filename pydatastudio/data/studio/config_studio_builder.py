"""
Created on 25 Jun 2025

@author: imoreno
"""
import importlib
import logging

from pydatastudio.data.studio.data_studio import DataStudio
from pydatastudio.data.studio.environment.data_studio_environment import DataStudioEnvironment
from pydatastudio.data.studio.students.abstract_student_factory import AbstractStudentFactory


class ConfigStudioBuilder:
    """
    Responsible for constructing a DataStudio instance with all its dependencies.

    This class acts as the "Composition Root" for the DataStudio, handling the
    logic of reading the environment, creating the necessary factories, and
    injecting them into the DataStudio. This separates the concern of "building"
    from the concern of "using".
    """
    def __init__(self, environment: DataStudioEnvironment):
        self.environment = environment
        self.logger = logging.getLogger(__name__)

    def _create_student_factory(self) -> AbstractStudentFactory:
        """
        Creates the student factory based on the environment configuration.
        """
        factory_class_path = self.environment.get_student_factory_class_name()

        if not factory_class_path:
            raise ValueError("Student factory 'class' not defined in environment configuration.")

        module_name, class_name = factory_class_path.rsplit('.', 1)
        
        self.logger.info(f"Loading student factory: {factory_class_path}")
        module = importlib.import_module(module_name)
        factory_class = getattr(module, class_name)
        
        return factory_class()


    def build_studio(self) -> DataStudio:
        """Builds and returns a fully configured DataStudio instance."""
        studio = DataStudio()

        student_factory = self._create_student_factory()
        
        students = student_factory.create_students()
        
        for student_name, student_obj in students.items():
            studio.add_student(student_name, student_obj)
            self.logger.info(f"Added student: {student_name}")


        return studio

