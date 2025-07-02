'''
Created on 7 feb. 2020

@author: imoreno
'''

from pydatastudio.case_formatter import CaseFormatter
import logging

class ContextManager(object):
    
    '''
    classdocs
    '''    
    instance = None
                       
    def __new__(cls):
        
        if (cls.instance is None):
            
            cls.instance = object.__new__(cls)
            cls.instance.context = {}
             
        return cls.instance
    
    def __init__(self):
        
        self.logger = logging.getLogger(__name__)
               
    def get_context_data(self, attribute):
        result = None
        
        self.logger.debug("attribute: {}".format(str(attribute)))
        
        if (attribute in self.context):
            result = self.context[attribute]
            self.logger.debug("result: {}".format(str(result)))

        else:
            raise Exception ("Key not found: {}".format(str(attribute)))
                        
        return result
           
    def set_context_data(self, attribute, value):
                     
        self.context[attribute] = value
        self.logger.debug("attribute: {}".format(str(attribute)))
        self.logger.debug("value: {}".format(str(value)))


          
    def context_data_contains(self, attribute):
        return attribute in self.context
    
    def obtain_context_text(self, text):
        '''
        Return a text changing {} parameters with *context values*
        
        E.g.:
        
            If the context have a dict for key KEY with values {"SUBKEY_1" : "VALUE_1", "SUBKEY_2": "VALUE_2"}
            
            and next string is passed:
            
                "The value of subkey_1 is {KEY[SUBKEY_1]}"

            It will be returned
            
                "The value of subkey_1 is VALUE_1"
            
                context = ContextManager()
            
        Example::
            
            name = {"name": "Ed", "apellido":"Sullivan"}
                
            age = {"persona": name, "edad": 32}
                
            context.set_context_data("info", age)
                
            print context.obtain_context_text("{info[persona][name]} {info[persona][apellido]} is {info[edad]} years old")
                
                
        Input attributes:
        
        :param text: Message to format.        
            
        Output:
            
        :return Formatted message with context         
             
        '''  
    
        formatter = CaseFormatter()
              
        result = formatter.format(text, **self.context)
        
        return result
               
    def clean_context(self):                
        self.context = {}
    