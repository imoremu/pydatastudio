'''
Created on 17 nov. 2018

@author: imoreno
'''
import logging
from pydatastudio.environment import environment_config_management

from builtins import KeyError

from pydatastudio.environment.exceptions import ConfigElementNotFoundException

class _EnvironmentConfig(object):
    '''
    classdocs
    
    _EnvironmentConfig is the class responsible of parsing environment configuration data.
    
    **IMPORTANT: This class should not be used directly. It should be used by mean of environment_config_management module.**
    
    Config data should be a dict with next format::
        
        
        Config_name: [Unique Config_Name]               
        
        Current: [current_environment]
            
        [environment 1]:
            [attr_level_1_1]:
                 [attr_level_2_1_1]
                 [attr_level_2_1_2]                 [...]
                 
            [attr_level_1_2]
                 [attr_level_2_2_1]
                     [atrr_level_3_...]
                 [attr_level_2_2_2]
                 [...]
    
            [...]
    
        [environment 2]
            [...]
                
    The attribute levels can be expanded as far as needed.
        
    Environments should have the same attributes. Each environment represents a 
        different configuration for the same attributes. 
        
    *Current* represents the current environment to be use. 
    '''
        
    SEPARATOR ="."
                
    def __init__(self, config, current_environment=None):
        '''
        Constructor
        
        Input attributes:
        
        :param fileName: yaml file with the environment configuration
        :param current_environment: Optional. It defines the desired current environment 
           if other than the one defined in the file.
           
        '''
        
        self.logger = logging.getLogger(__name__)    
        self.config = config
           
        try:
                    
            if (current_environment is None):
                self.current_environment = self.config[environment_config_management.CURRENT_ENVIRONMENT_NAME]
            else:
                self.current_environment = current_environment
    
        except KeyError as e:
            
            raise ConfigElementNotFoundException('{} element not found. Specifically: {}'.format(current_environment, e))
        
        
    
    def get_config_value (self, *attributes):
        result = self._get_environment_config_value(self.current_environment, *attributes)
        
        return result
        
    def _get_environment_config_value (self, environment, *attributes):
        try:
            result = self.config[environment]
            
            for subsection in attributes :
                result = result[subsection]
        
        except KeyError as e:
            
            self.logger.debug('{} element not found'.format(str(attributes)))
            
            raise ConfigElementNotFoundException('{} element not found. Specifically: {}'.format(str(attributes), e))
        
        if (isinstance(result,str) and result.startswith("<<") and result.endswith(">>")):
            result = self._getEnvironmentConfigValue(environment, result[2:-2])            
        
        return result
                
            
    def _getEnvironmentConfigValue (self, environment, attribute):
        try:
            result = self.config[environment]
            
            for subsection in attribute.split(self.SEPARATOR) :
                result = result[subsection]
        
        except KeyError as e:
            
            self.logger.debug('{} element not found'.format(attribute))
            raise ConfigElementNotFoundException('{} element not found. Specifically: {}'.format(attribute, e))
        
        return result
       
    
