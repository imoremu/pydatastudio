'''
Created on 31 ene. 2020

@author: imoreno
'''

import os
import logging.config

from pydatastudio import resourcesmanager

class Logging():

    logger_file = resourcesmanager.get_resource_path(os.path.join(".", "conf", "logging.conf"))

    is_config = False
    
    PERFORMANCE_KEY = "common.performance"

    @classmethod
    def setLoggerFile(cls, loggerFile):
                      
        if not os.path.isfile(loggerFile):
            
            raise FileNotFoundError("File {} not found. Current directory: {}".format(loggerFile, os.path.abspath(os.getcwd())))                     
            
        cls.logger_file = loggerFile
    
    @classmethod
    def getLogger(cls,name):
               
        if (not cls.is_config): 
            
            print("Logger File: {}".format(cls.logger_file))   
            
            logging.config.fileConfig(cls.logger_file)
            cls.is_config = True
    
        return logging.getLogger(name)
    
    @classmethod    
    def getPerformanceLogger(cls, name = ""):        
        if (not cls.is_config): 
            
            print("Logger File: {}".format(cls.logger_file))   
            
            logging.config.fileConfig(cls.logger_file)
            cls.is_config = True
            
        key = cls.PERFORMANCE_KEY
        
        if not name == "":
            key += "." + name
       
        return logging.getLogger(key)
    