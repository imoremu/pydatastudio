'''
Created on 11 feb. 2021

@author: imoreno
'''
import os
import unittest

from pydatastudio import resourcesmanager
from pydatastudio.data.dataframequerymanager import DataframeQueryManager,\
    SPECIFIC_FILTERS_KEY


class TestDataFrameQuery(unittest.TestCase):    

    DEFAULT_CONF_FILE = resourcesmanager.get_resource_path(os.path.join(".", "test", "pydatastudio", "data", "testdata", "query_data.yaml"))
    
    def setUp(self):        
        
        self.query_manager =  DataframeQueryManager.obtain_query_info_from_file(self.DEFAULT_CONF_FILE)                      
        
        pass


    def tearDown(self):
        pass


    def testGroupPreFilter(self):
        
        result = self.query_manager.obtain_pre_filter("group_1")
        
        expected = {"attr-2": 1, "attr-5":2}
        
        self.assertEqual(result, expected)
            
       
    def testGeneralFilterAll(self):
        
        groups_info = self.query_manager.obtain_info()
        
        no_elements = True
        
        for group in groups_info.values():
            
            for element_filters in group[SPECIFIC_FILTERS_KEY].values():
                no_elements = False
                
                for specific_filter in element_filters.values():                   
                    
                    expected = "attr_1"
                    
                    self.assertIn(expected, specific_filter.keys())
        
        if no_elements:
            
            self.fail("No element in filter")
        
    def testGeneralFilterGroup(self):        
        groups_info = self.query_manager.obtain_info()
        
        no_elements = True
        
        for group_name, group in groups_info.items():
            
            for element_filters in group[SPECIFIC_FILTERS_KEY].values():
                no_elements = False
                
                expected = "Scope Group"
                if ("group_2" == group_name):
                    self.assertIn(expected, element_filters.keys(), f"{expected} not found in {str(element_filters.keys())} for {group_name} group ")
                else:
                    self.assertNotIn("Scope_Group", element_filters.keys(), f"{expected} found in {str(element_filters.keys())} for {group_name} group")                        
        
        if no_elements:
            
            self.fail("No element in filter")        

            
            

    def testGeneralFilterElement(self):
        
        groups_info = self.query_manager.obtain_info()
        
        no_elements = True
        
        for group in groups_info.values():
            
            for element_name, element_filters in group[SPECIFIC_FILTERS_KEY].items():
                no_elements = False
                
                expected = "Scope Element"
                if ("element_3" == element_name):
                    self.assertIn(expected, element_filters.keys(), f"{expected} not found in {str(element_filters.keys())} for {element_name} element ")
                else:
                    self.assertNotIn("Scope_Group", element_filters.keys(), f"{expected} found in {str(element_filters.keys())} for {element_name} element")                        
        
        if no_elements:
            
            self.fail("No element in filter")        
        
    def testGeneralFilterGroupElement(self):
        groups_info = self.query_manager.obtain_info()
        
        no_elements = True
        
        for group_name, group in groups_info.items():
            
            for element_name, element_filters in group[SPECIFIC_FILTERS_KEY].items():
                no_elements = False
                
                expected = "Scope Group Element"
                if ("element_2" == element_name and "group_1" == group_name):
                    self.assertIn(expected, element_filters.keys(), f"{expected} not found in {str(element_filters.keys())} for {element_name} element and {group_name} group ")
                else:
                    self.assertNotIn("Scope_Group", element_filters.keys(), f"{expected} found in {str(element_filters.keys())} for {element_name} element and {group_name} group")                        
        
        if no_elements:
            
            self.fail("No element in filter")

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()