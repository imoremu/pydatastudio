'''
Created on 19 feb. 2021

@author: imoreno
'''
import unittest
from unittest.mock import Mock, patch, call

from yaml.loader import FullLoader
import yaml

import os

from pydatastudio.data.studio.abstractdatabasicstudent import AbstractDataBasicStudent
from pydatastudio import resourcesmanager
from pydatastudio.data.studio.abstractdatabasicstudent import AbstractDataBasicStudent, ResearchNotFoundException, RequiredResearchNotFoundException
from pydatastudio.data.studio.datastudioconstants import ENVIRONMENT_FILTER_KEY, ENVIRONMENT_FILTER_DATA_KEY, ENVIRONMENT_RESEARCHES_KEY, ENVIRONMENT_STUDENT_KEY, ENVIRONMENT_INPUT_KEY
from pydatastudio.data.studio.datastudentconfiguration import DataStudentConfiguration

import pandas as pd

class TestAbstractDataBasicStudent(unittest.TestCase):

    BASE_FILE_NAME = resourcesmanager.get_resource_path(os.path.join(".", "test", "pydatastudio", "data", "studio", "testdata", "test_student_configuration.yaml"))  
        
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

        # mock _obtain_filtered_data to avoid data filtering
        self.student._obtain_filtered_data = Mock()        
                      
        self.studio.check_research_ready = Mock(return_value = False)
        self.student._join_studio(self.studio)     
        
        self.student._research(research_requested)               
        
        self.studio.check_research_ready.assert_has_calls(blocking_researches, any_order = True)        
          
    def testResearchMethodCall(self):                
        research_requested = "research.test 1"                                             

        method = Mock()        
        self.student._research_research_test_1 = method
        
        # mock _obtain_filtered_data to avoid data filtering
        self.student._obtain_filtered_data = Mock()    

        attrs = {"a" : "A", "b" : "B"} 
        
        self.student._research(research_requested, **attrs)        
                
        method.assert_called_once_with(research_requested, **attrs)     
        
        
    def testResearchMethodNotFoundCall(self):                
        research_requested = "research.test 1"                                             

        attrs = {"a" : "A", "b" : "B"}                                    
        
        # mock _obtain_filtered_data to avoid data filtering
        self.student._obtain_filtered_data = Mock()    

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
    

    def test_research_with_data_filter(self):        
        def mock_test_filtered_research(self, research_name, **attrs):
            data = {'col1': ['1', '2', '3', '4'], 'col2': ['A', 'B', 'C', 'A']}
            df = pd.DataFrame(data)
            return {research_name: df}

        config_dict = {
            ENVIRONMENT_STUDENT_KEY: "TestStudent",
            ENVIRONMENT_RESEARCHES_KEY: {
                "test_filtered_research": {
                    ENVIRONMENT_FILTER_KEY: {
                        ENVIRONMENT_FILTER_DATA_KEY: {
                            'col1': '^[13]$'
                        }
                    }
                }
            }
        }
        student_config = DataStudentConfiguration(config_dict)

        self.student.configuration = student_config

        self.student._research_test_filtered_research = mock_test_filtered_research.__get__(self.student, AbstractDataBasicStudent)

        self.student._join_studio(self.studio)

        result = self.student._research("test_filtered_research")

        expected_df = pd.DataFrame({'col1': ['1', '3'], 'col2': ['A', 'C']})
        
        # Reset index
        result["test_filtered_research"] = result["test_filtered_research"].reset_index(drop=True)
        expected_df = expected_df.reset_index(drop=True)

        # Check data checking only data but no indexes:        
        pd.testing.assert_frame_equal(result["test_filtered_research"], expected_df)


    def test_research_with_no_filter_info(self):        
        def mock_test_no_filter_research(self, research_name, **attrs):
            data = {'col1': [1, 2, 3], 'col2': ['X', 'Y', 'Z']}
            df = pd.DataFrame(data)
            return {research_name: df}

        config_dict = {
            ENVIRONMENT_STUDENT_KEY: "TestStudent",
            ENVIRONMENT_RESEARCHES_KEY: {
                "test_no_filter_research": {} # No filter defined
            }
        }
        student_config = DataStudentConfiguration(config_dict)

        self.student.configuration = student_config

        self.student._research_test_no_filter_research = mock_test_no_filter_research.__get__(self.student, AbstractDataBasicStudent)
        self.student._join_studio(self.studio)

        result = self.student._research("test_no_filter_research")

        expected_df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['X', 'Y', 'Z']})
        pd.testing.assert_frame_equal(result["test_no_filter_research"], expected_df)

    def test_research_with_empty_filter_data(self):        
        def mock_test_empty_filter_research(self, research_name, **attrs):
            data = {'col1': [1, 2, 3], 'col2': ['X', 'Y', 'Z']}
            df = pd.DataFrame(data)
            return {research_name: df}

        config_dict = {
            ENVIRONMENT_STUDENT_KEY: "TestStudent",
            ENVIRONMENT_RESEARCHES_KEY: {
                "test_empty_filter_research": {
                    ENVIRONMENT_FILTER_KEY: {
                        ENVIRONMENT_FILTER_DATA_KEY: {} # Empty filter data
                    }
                }
            }
        }
        student_config = DataStudentConfiguration(config_dict)

        self.student.configuration = student_config

        self.student._research_test_empty_filter_research = mock_test_empty_filter_research.__get__(self.student, AbstractDataBasicStudent)
        self.student._join_studio(self.studio)


        result = self.student._research("test_empty_filter_research")

        expected_df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['X', 'Y', 'Z']})
        pd.testing.assert_frame_equal(result["test_empty_filter_research"], expected_df)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testJoinStudio']
    unittest.main()