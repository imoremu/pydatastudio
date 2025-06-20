'''
Created on 14 feb. 2021

@author: imoreno
'''
import unittest

from pydatastudio import resourcesmanager
from pydatastudio.data.studio.datastudentconfiguration import DataStudentConfiguration

from yaml.loader import FullLoader
import yaml

import os


class TestDataStudentConfiguration(unittest.TestCase):

    BASE_FILE_NAME = resourcesmanager.get_resource_path(os.path.join(".", "test", "pydatastudio", "data", "studio", "testdata", "test_student_configuration.yaml"))  
    
    def setUp(self):
        configuration = yaml.load(open(TestDataStudentConfiguration.BASE_FILE_NAME), Loader=FullLoader)
        
        self.conf = DataStudentConfiguration(configuration) 
            
    def testObtainResearchs(self):
        
        result = list(self.conf.obtain_researches().keys())
        expected = ["research.test 1", "research 2", "research 3"]
        
        self.assertListEqual(result, expected)

    def testObtainInitialResearch(self):
        
        result = self.conf.obtain_initial_researches()
        expected = ["research.test 1"]
        
        self.assertListEqual(result, expected)

    def testObtainPendingResearchs(self):
        
        result = self.conf.obtain_required_researches()
        expected = {"research.test 1" : None, "research 2" : ["research.test 1","research 3" ], "research 3" : ["research.test 1"]}
        
        self.assertDictEqual(result, expected)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()