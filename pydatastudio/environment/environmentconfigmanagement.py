'''
Created on 24 dic. 2018

@author: imoreno
'''
import yaml
from yaml.loader import FullLoader
from pydatastudio.environment import environmentconfig

environment_confs = {}

CONFIG_NAME = "config_name"
CURRENT_ENVIRONMENT_NAME = "Current"


def get_environment_config_by_yaml_file(file_name, current_environment=None):
    """
    Return the environment config paser associated to the yaml file name and environment.
    
    Yaml file will have the format needed for environmentconfig.              
    
    Note: This should be the default way to treat environment config parser.
    
    Input attributes:
        
    :param file_name: Filen name with the configuration.
    :param current_environment: current environment
        
    Output:
        
    :return Parser associated to file_name and current_environment 
    :rtype: _EnvironmentConfig    
       
    :raise ConfigElementNotFoundException
        
    """    
    config = _get_config_from_yaml_file(file_name)
        
    result = get_environment_by_config(config, current_environment)
    
    return result


def get_environment_by_config(config, current_environment=None):
    """
    Return the config parser associated to the general config data and environment.
    
    Config data will have the format needed for environmentconfig.              
    
    Note: This should be the default way to treat environment config parser.
    
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

    Input attributes:
        
    :param config: Configuration.
    :param current_environment: current environment
        
    Output:
        
    :return Parser associated to file_name and current_environment 
    :rtype: _EnvironmentConfig    
       
    :raise ConfigElementNotFoundException
        
    """ 
    config_name = config[CONFIG_NAME]
    
    if ((config_name, current_environment) in environment_confs):
        result = environment_confs.get((config_name, current_environment))
    else:
        result = environmentconfig._EnvironmentConfig(config, current_environment)
        environment_confs[(config_name, current_environment)] = result
        
    return result

def _get_config_from_yaml_file(file_name):
    """
    Return the config data associated to a config yaml file.

    Input attributes:
        
    :param filename: YAML file with the configuration.
            
    Output:
        
    :return Config Data
    :rtype: Object    
        
    """ 
    #config = yaml.load(open(file_name))
    config = yaml.load(open(file_name), Loader=FullLoader)
        
    config[CONFIG_NAME] = file_name
     
    return config

def obtain_default_environment(config):
    return config[CURRENT_ENVIRONMENT_NAME]