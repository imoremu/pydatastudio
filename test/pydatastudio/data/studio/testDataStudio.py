'''
Created on 21 feb. 2021

@author: imoreno
'''
import unittest
from pydatastudio.data.studio.datastudio import DataStudio
from pydatastudio.data.studio.abstractdatabasicstudent import AbstractDataBasicStudent
from unittest.mock import patch, Mock


class TestDataStudio(unittest.TestCase):

    @patch('pydatastudio.data.studio.abstractdatabasicstudent.AbstractDataBasicStudent')
    @patch('pydatastudio.data.studio.abstractdatabasicstudent.AbstractDataBasicStudent')
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