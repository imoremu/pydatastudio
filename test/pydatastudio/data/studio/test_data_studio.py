'''
Created on 21 feb. 2021

@author: imoreno
'''
import unittest
from pydatastudio.data.studio.data_studio import DataStudio
from pydatastudio.data.studio.students.abstract_data_basic_student import AbstractDataBasicStudent
from unittest.mock import patch, Mock

import pandas as pd

class TestDataStudio(unittest.TestCase):

    @patch('pydatastudio.data.studio.students.abstract_data_basic_student.AbstractDataBasicStudent')
    @patch('pydatastudio.data.studio.students.abstract_data_basic_student.AbstractDataBasicStudent')
    def setUp(self, student_1, student_2):
        
        self.studio = DataStudio()
        
        self.student_1 = student_1                      
        self.student_2 = student_2
        
        self.student_1.mock_add_spec(AbstractDataBasicStudent)
        self.student_2.mock_add_spec(AbstractDataBasicStudent)               
        
        self.studio.add_student("student_1", self.student_1)
        self.studio.add_student("student_2", self.student_2)


    def tearDown(self):
        pass

    def test_add_studio_research(self):
        research_name = "test_research"
        test_research_data = {"key1": "value1", "key2": pd.DataFrame({"col": [1, 2]})}

        self.studio.add_studio_research(research_name, test_research_data)

        self.assertIn(research_name, self.studio.knowledge)
        self.assertEqual(self.studio.knowledge[research_name], test_research_data)

    def test_add_studio_research_overwrites_existing(self):        
        research_name = "existing_research"
        initial_data = {"version": 1, "value": "old"}
        updated_data = {"version": 2, "value": "new", "extra": True}

        # Add initial research
        self.studio.add_studio_research(research_name, initial_data)
        self.assertIn(research_name, self.studio.knowledge)
        self.assertEqual(self.studio.knowledge[research_name], initial_data)

        # Overwrite with new data
        self.studio.add_studio_research(research_name, updated_data)
        self.assertIn(research_name, self.studio.knowledge)
        self.assertEqual(self.studio.knowledge[research_name], updated_data)
        self.assertNotEqual(self.studio.knowledge[research_name], initial_data)

    def testResearchWithOneStudent(self):
        
        self.student_1._is_research_provided = Mock(return_value = False)
        self.student_2._is_research_provided = Mock(return_value = True)
        
        research_name = "Research"        
        attrs = {"a" : "A", "b" : "B"} 
        
        self.studio.research(research_name, **attrs)
        
        self.student_2._research.assert_called_once_with(research_name, **attrs)
        self.student_1._research.assert_not_called()        
        
    
    def testResearchWithMultipleStudents(self):
        self.student_1._is_research_provided = Mock(return_value = True)
        self.student_2._is_research_provided = Mock(return_value = True)
        
        research_name = "Research"        
        attrs = {"a" : "A", "b" : "B"} 
        
        self.studio.research(research_name, **attrs)
        
        self.student_1._research.assert_called_once_with(research_name, **attrs)
        self.student_2._research.assert_not_called()     
    
        
        
    def testResearchWithSpecificStudent(self):
        self.student_1._is_research_provided = Mock(return_value = True)
        self.student_2._is_research_provided = Mock(return_value = True)
        
        research_name = "Research"        
        attrs = {"a" : "A", "b" : "B"}
        
        self.studio.research(research_name, student_name = "student_2", **attrs)
        
        self.student_2._research.assert_called_once_with(research_name, **attrs)
        self.student_1._research.assert_not_called()        
        
    
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()