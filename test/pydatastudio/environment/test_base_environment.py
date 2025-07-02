'''
Created on 11 mar. 2020

@author: imoreno
'''
import unittest
import os
import yaml
from pydatastudio.environment import environment_config
from pydatastudio.environment.base_environment import BaseEnvironmentObject


class Test(unittest.TestCase):

    def setUp(self):
        
        conf_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "conf","test_configuration.yaml")
        config = yaml.safe_load(open(conf_file))
                
        parser = environment_config._EnvironmentConfig(config)
        
        self.environment = BaseEnvironmentObject(parser)
        

    def test_get_specific_config_value_with_call_attributes(self):
               
        result = self.environment.get_specific_config_value("section","first_level","second_level", id = {"subid": "TEST"}, value = "1")
         
        expected = "TEST VALUE TEST 1"
        
        self.assertEqual(result, expected)


    def test_get_specific_config_value_with_dict(self):
        
        data = {"id" : {"subid" : "TEST"}, "value" : "1"}
            
        result = self.environment.get_specific_config_value("section","first_level","second_level", **data)
            
        expected = "TEST VALUE TEST 1"
        
        self.assertEqual(result, expected)
        
        
    def test_context_contains(self): 
        
        self.assertTrue(self.environment.environment_contains("section", "first_level", "second_level"), "'second_level' is not contained in context" )        
        self.assertFalse(self.environment.environment_contains("section", "first_level", "unknown_level"))
        self.assertFalse(self.environment.environment_contains("section", "unknown_level", "second_level"))

    def test_reference_var(self):
        
        result = self.environment.get_specific_config_value("var_ref")
        
        expected = "TEST VAR"
        
        self.assertEqual(result, expected)       
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_get_specific_config_value']
    unittest.main()