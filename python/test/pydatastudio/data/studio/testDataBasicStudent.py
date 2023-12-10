'''
Created on 19 feb. 2021

@author: imoreno
'''
import unittest

from pydatastudio.data.studio.abstractdatabasicstudent import AbstractDataBasicStudent
from yaml.loader import FullLoader
import yaml
from pydatastudio import resourcesmanager
import os
from pydatastudio.data.studio.datastudentconfiguration import DataStudentConfiguration
from pydatastudio.data.studio.datastudio import ResearchNotFoundException,\
    DataStudio
from unittest.mock import Mock, patch, call


class TestAbstractDataBasicStudent(unittest.TestCase):

    BASE_FILE_NAME = resourcesmanager.get_resource_path(os.path.join(".","python", "test", "pydatastudio", "data", "studio", "testdata", "test_student_configuration.yaml"))  
        
    @patch('pydatastudio.data.studio.datastudio.DataStudio')    
    def setUp(self, studio):        
        configuration = DataStudentConfiguration(yaml.load(open(TestAbstractDataBasicStudent.BASE_FILE_NAME), Loader=FullLoader))
        
        self.student = AbstractDataBasicStudent(configuration)
        self.studio = studio
           

    def tearDown(self):
        pass

                                                   
    def testInitialResearches(self):
        initial_research = "research.test 1"                        
        
        attrs = {"a" : "A", "b" : "B"} 
        
        self.student._join_studio(self.studio, **attrs)     
        
        self.studio.research.assert_called_once_with(initial_research, **attrs)
        
    def testCheckBlockingResearch(self):
        blocking_researches = [call("research.test 1"), call("research 3")]
        
        research_requested = "research 2"                
        
        method = Mock()        
        self.student._research_research_2 = method        
                      
        self.studio.check_research_ready = Mock(return_value = False)
        self.student._join_studio(self.studio)     
        
        self.student._research(research_requested)               
        
        self.studio.check_research_ready.assert_has_calls(blocking_researches, any_order = True)        
          
    def testResearchMethodCall(self):                
        research_requested = "research.test 1"                                             

        method = Mock()        
        self.student._research_research_test_1 = method
        
        attrs = {"a" : "A", "b" : "B"} 
        
        self.student._research(research_requested, **attrs)        
                
        method.assert_called_once_with(research_requested, **attrs)     
        
        
    def testResearchMethodNotFoundCall(self):                
        research_requested = "research.test 1"                                             

        attrs = {"a" : "A", "b" : "B"}                                    
        
        with self.assertRaises(ResearchNotFoundException):        
            self.student._research(research_requested, **attrs)
            

    def testResearchProvided(self):
        research_requested = "research.test 1"                                             

        method = Mock()        
        self.student._research_research_test_1 = method
        
        self.assertTrue(self.student._is_research_provided(research_requested))
    
    
    def testResearchNotProvided(self):
        research_requested = "research.test 1"                                            
        
        self.assertFalse(self.student._is_research_provided(research_requested))
    
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testJoinStudio']
    unittest.main()