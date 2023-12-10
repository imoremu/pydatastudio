'''
Created on 18 nov. 2018

@author: imoreno
'''

from pydatastudio.caseformatter import CaseFormatter
from pydatastudio.logging import Logging
from pydatastudio.environment.contextmanager import ContextManager

class BaseEnvironmentObject(object):
    '''
        Base class for Environment object.
        
        An environment object y an implementation that depends on a environment configuration. It allows to change the basic functionality 
        depending on configuration data.
        
        Moreover, BasicEnvironmentObject allows the environment to be decorated by the current context of the environment.    
        
        Note: each class type has its own environment. But there is only one instance per class and environment. 
        When a second instance of the same class type and environment is called, the first one is returned to avoid multiple instances with same scope to be created.                      
                     
        Base class provides:
        
        - environment: environment metadata
        - context: dictionary with current context attributes
    '''
    
    DEFAULT_PREFIX = "default"
    BROWSER_ATTR_KEY = "browser"
    BROWSER_TYPE_ATTR_KEY = "type"
    
    instances = {}
    
    def __new__(cls, *args):
        '''
            __new__ is overwritten to implement singleton factory pattern.
            
            There is only one object per class + consructor args
            
        '''
        logger = Logging.getLogger(cls.__module__)  
        
        cls_name = cls.__name__
        
        if ((cls_name,args) in cls.instances.keys()):                                   
            
            result =  cls.instances[(cls_name,args)]            
        else:
            
            logger.debug("Create new instance for {}".format(cls_name))
            result = super(BaseEnvironmentObject, cls).__new__(cls)
            
            cls.instances[(cls_name,args)] = result
            
        return result
        
          
    def __init__(self, environment):
        
        self.logger = Logging.getLogger(self.__class__.__module__)   
        
        if environment is None:
                         
            raise Exception("Environment configuration is mandatory attribute for BaseEnvironmentObject")                        
        
        self.environment = environment
        self.context = ContextManager()
        
                         
    def environment_contains(self, *attrs):
        
        parent_attrs = attrs[:-1]
        
        result = False
        
        if len(parent_attrs) > 0:               
        
            if (self.environment_contains(*parent_attrs)):            
                parent = self.environment.get_config_value(*parent_attrs)        
                result = attrs[-1] in parent 
        else:
            
            result = True
            
        return result                
        
    
    def get_config_value(self, *attrs):
        result = self.environment.get_config_value(*attrs)
        
        return result
                                         
    def get_context_config_value(self, *attrs):
        
        result = self.environment.get_config_value(*attrs)
        
        if (not result is None and isinstance(result, str)):                                                 
            result = self.context.obtain_context_text(result)
        
        return result
    
    
    def get_specific_config_value_without_formatting(self, *attrs, **data):
        
        return self._get_specific_config_value(False, *attrs, **data)
    
    def get_specific_config_value(self, *attrs, **data):
              
        return self._get_specific_config_value(True, *attrs, **data)        
    
    def _get_specific_config_value(self, formatted, *attrs, **data):
        
        result = self.get_config_value(*attrs)
        
        if (not result is None and formatted and isinstance(result, str)):                                                 
            
            formatter = CaseFormatter()              
            result = formatter.format(result, **data)
        
        
        if (not result is None and isinstance(result, dict)):
            
            for key in result.keys():
                
                key_attrs = (*attrs, key)                
                
                result[key] = self._get_specific_config_value(formatted, *key_attrs, **data)
        
        return result      
    
    def obtain_context_element_or_default_from_type(self, element_type):
        
        if self.context.context_data_contains(element_type):
            result = self.context.get_context_data(element_type)
        
        else:                        
            default_id = self.get_context_config_value("{} {}".format(BaseEnvironmentObject.DEFAULT_PREFIX,element_type))
        
            result = self.get_context_config_value("{}s".format(element_type), default_id)
            
            self.context.set_context_data(element_type, result)
        
        return result