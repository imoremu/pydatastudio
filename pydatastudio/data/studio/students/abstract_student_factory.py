"""
Created on 24 Jun 2025

@author: imoreno
"""

from abc import ABC, abstractmethod
from typing import Dict

from pydatastudio.data.studio.data_studio import AbstractStudent


class AbstractStudentFactory(ABC):
    """
    Defines the interface for all student factory implementations.
    
    This ensures that any factory used by PortfolioStudio will have a
    consistent `create_students` method.
    """
    
    @abstractmethod
    def create_students(self) -> Dict[str, AbstractStudent]:
        """
        Creates all configured students.
        
        The source of the configuration (e.g., dict, db connection)
        should be provided during the concrete factory's initialization.
        
        :return: A dictionary mapping each student's name to its object instance (AbstractStudent).
        """
        pass
