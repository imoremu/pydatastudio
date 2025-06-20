'''
Created on 2 ene. 2019

@author: imoreno
'''
import os
import sys

# Get Basic Path
if hasattr(sys, 'frozen') and hasattr(sys, '_MEIPASS'):
    
    BASIC_PATH = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
               
else:   
    
    BASIC_PATH = os.path.join(os.path.dirname(__file__),"..", "..")

print("Resources basic path: {}".format(BASIC_PATH))

def get_resource_path(conf_file):
    '''
    Returns the absolute path of a resource file.

    Args:
        conf_file (str): The path of the resource file.
        
    Returns:
        str: The absolute path of the resource file.
    '''
    
    result = conf_file

    if not os.path.isabs(conf_file):
        result = os.path.abspath(os.path.join(BASIC_PATH, conf_file)) 
        
    return result
    
def create_path_if_needed(filepath):
    '''
    Create a path if it does not exist.

    Args:
        filepath (str): The path to the file.
    '''
                
    os.makedirs(os.path.dirname(filepath), exist_ok= True )    