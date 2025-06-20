'''
Created on 11 feb. 2021

@author: imoreno
'''
from pydatastudio.logging import Logging
from yaml.loader import FullLoader
import yaml
import re

GENERAL_KEY = "general"
DETAIL_KEY = "detail"
PRE_FILTER_KEY = "pre-filter"
SPECIFIC_FILTERS_KEY = "specific filters"
GENERAL_FILTER_KEY = "filter"
GENERAL_SCOPE_KEY = "scope"
    
class DataframeQueryManager(object):
    '''
    This class allows to define goals of related filter queries for dataframemanager with:
    
    - Default elements filter - applied to all the elements matching defined regexp (scope)
    - Pre-Filter per goal
    - Specific Filter per element
    
    It takes a dictionary query_info of the form:
    
    { "general": {"[default_filter_name_1] : 
                        { 
                            filter: {filter_dict_1}
                            scope: [scope_1]
                        }   
                  
                  ...
                  
                  "[default_filter_name_n] : 
                        { 
                            filter: {filter_dict_n}
                            scope: [scope_n]
                        }
                }
     
      "detail": {"[Goal_name_1]" :
                      pre-filter: {pre_filter_dict_n}
                      specific filters: 
                          {
                              element_name_1:  {element_name_filter_dict_1}
                              ...
                              element_name_n:  {element_name_filter_dict_n}
                          }
                  
                  ...
                  
                 "[Goal_name_n]" :
                      pre-filter: {pre_filter_dict_n}
                      specific filters: {specific_filter_dict_n}
                      
    The "general" section provides default filters that are applied to every element unless overridden.
    Each default filter is identified by a unique name, and it consists of a filter dictionary and a scope.
    The scope is a regular expression that determines which goals and elements the default filter applies to.
    If "all", the default filter is applied to all elements.

    The "detail" section contains goal-specific information.
    For each goal, you can define a pre-filter and specific filters for individual elements.
    The pre-filter is applied to the entire goal, and specific filters override the default filters for specific elements.
    Elements are identified by unique names within each goal.

    All filters are defined using the same format as the data_filter_by_dict method of the DataFrame class.
    '''
    
    @classmethod
    def obtain_query_info_from_file(cls, filename):                                                   
        
        query_info = yaml.load(open(filename), Loader=FullLoader)
        
        return DataframeQueryManager(query_info)       
        

    def __init__(self, input_info):
        '''
        Constructor
        '''
        self.logger = Logging.getLogger(__name__)   
        
        self.query_info = self._obtain_info(input_info) 
        
                  
    def _obtain_info(self, input_info):        
              
        general_info = input_info[GENERAL_KEY]
        
        goals_info = input_info[DETAIL_KEY]
        
        result = {}
        
        
        for goal, goal_data in goals_info.items():
            
            self.logger.info(f"Getting goal {goal} query info")                        
            result[goal] = {}
            
            result[goal][PRE_FILTER_KEY] = goal_data[PRE_FILTER_KEY]
            result[goal][SPECIFIC_FILTERS_KEY] = {} 
            
            for element, element_filter in goal_data[SPECIFIC_FILTERS_KEY].items():
                
                self.logger.debug(f"Getting element {element} for goal {goal} query info")
                
                result[goal][SPECIFIC_FILTERS_KEY][element] = {}
                
                for general_filter_name, general_filter_data in general_info.items():
                    
                    scope = general_filter_data[GENERAL_SCOPE_KEY]
                        
                    if scope == "all" or re.match(scope, goal + "-" + element):
                        result[goal][SPECIFIC_FILTERS_KEY][element][general_filter_name] = {**general_filter_data[GENERAL_FILTER_KEY], 
                                                                                              **element_filter}                                                                                                                                        
            
        return result
    
    
    def obtain_info(self):
        
        return self.query_info     

    def obtain_goal_names(self):
        
        return self.query_info.keys()
        
    def obtain_pre_filter(self, goal):
        return self.query_info[goal][PRE_FILTER_KEY]
    
    def obtain_specific_filter(self, goal):
        return self.query_info[goal][SPECIFIC_FILTERS_KEY]
        