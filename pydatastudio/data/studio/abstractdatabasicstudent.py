'''
Created on 15 feb. 2021

@author: imoreno
'''
from pydatastudio.data.studio.datastudio import AbstractStudent,\
    ResearchNotFoundException

import re

from pydatastudio.logging import Logging
from pydatastudio.data.studio.datastudioconstants import ENVIRONMENT_FILE_KEY,\
    ENVIRONMENT_FILTER_KEY, ENVIRONMENT_DIR_KEY,\
    ENVIRONMENT_FILE_NAME_KEY, ENVIRONMENT_FILTER_DATA_KEY
    
from pydatastudio.data.dataframeutils import data_filter_by_dataframe, data_filter_by_dict
from pydatastudio import resourcesmanager

from pandas.core.frame import DataFrame


class AbstractDataBasicStudent(AbstractStudent):
    '''
    A base class for implementing data-oriented students.

    This class extends AbstractStudent and provides common functionality for students dealing with data.

    From abstractDataBasicStudent a complete student can be generated by adding one or several research methods.
    Research methods has to be named with the name of the research substituting any space o special char by underscore '_'. 
    
    These researches and their input needs (researches or files) and attributes will be defined in the :class:'DataStudentConfiguration'.

    Attributes:
        configuration (:class:'DataStudentConfiguration'): The configuration object for the student.
        
    '''            
    def __init__(self, configuration):
        '''
        Constructor
        
        :param
        
        configuration : DataStudentConfiguration object with student configuration
        
        '''
        self.logger = Logging.getLogger(self.__class__.__module__)
        
        self.configuration = configuration
        self.name = configuration.name
        
    
    def _join_studio(self, studio, **attrs):
                
        self.studio = studio             
        
        for research in self.configuration.obtain_initial_researches():
            studio.research(research, **attrs)                                   
                    
    
    def _research(self, research_name, **attrs):        
        
        # First, all researches needed by the student for implementing the requested research are requested (if they're not already created and stored in the studio)
        required_researches = self.configuration.obtain_required_researches()[research_name]
        
        if required_researches is not None:       
        
            if isinstance(required_researches, dict):                
                required_researches = required_researches.values()
             
            for required_research in required_researches:       
                done = self._check_research_ready(required_research)
            
                if not done:
                    self.studio.research(required_research, **attrs)                                               
            
        research_method_name = self._obtain_research_method_name(research_name)            
                    
        if not self._is_research_provided(research_name):
            
            self.logger.error(f"Research {research_method_name} not available in student {self.name}")            
            raise ResearchNotFoundException(f"Research {research_method_name} not available in student {self.name}")
        
        else:                                   
            
            Logging.getPerformanceLogger().info(f"\n ----- STARTED-----\n Research: {research_name}\n Student: {self.name}\n\n -------------- ")
            
            research_method = getattr(self, research_method_name)            
            result = research_method(research_name, **attrs)
            
            Logging.getPerformanceLogger().info(f"\n ----- FINISHED -----\n Research: {research_name}\n Student: {self.name}\n\n -------------- ")
                
        return result
        
    def _is_research_provided(self, research_name):
        
        result = hasattr(self, self._obtain_research_method_name(research_name))                                                    
            
        return result
        
    def _obtain_research_method_name (self, research_name):
        
        result = research_name.lower()
        result = "_research_" + re.sub (" |\.|-", "_", result)                
                    
        return result
    
    def _check_research_ready(self, research):               
        return self.studio.check_research_ready(research)                                
                             
    def _obtain_filter_info(self, research_name):
        result = None
        
        if (ENVIRONMENT_FILTER_KEY in self.configuration.obtain_researches()[research_name]):
        
            result = self.configuration.obtain_researches()[research_name][ENVIRONMENT_FILTER_KEY]
        
        return result

    
    def _obtain_filtered_data(self, research_name, research):
        '''
        Filter result data. 
        
        Two kind of filters:
        
        - Dictionary / List of dictionary: Dataframe filtering
        - File: file with a sheet with a table of cases to be filtered. Each field in each line will represent an AND operand. 
        Each file line will be included as an OR 
        
        '''
        result = research 
                        
        if research_name in research and isinstance(research[research_name], DataFrame):

            Logging.getPerformanceLogger().info(f"\n ----- FILTER STARTED-----\n Research: {research_name}\n Student: {self.name}\n\n -------------- ")
                                 
            filtered_df = research[research_name]
            
            filter_info = self._obtain_filter_info(research_name)
            
            if (filter_info is not None):                
                if (ENVIRONMENT_FILTER_DATA_KEY in filter_info):
                    data_filter_info = filter_info[ENVIRONMENT_FILTER_DATA_KEY]
                    
                    filtered_df = data_filter_by_dict(data_filter_info, filtered_df)
                    
                result[research_name] = filtered_df        
            
            Logging.getPerformanceLogger().info(f"\n ----- FILTER FINISHED-----\n Research: {research_name}\n Student: {self.name}\n\n -------------- ")
            
        return result                                                                                           
    