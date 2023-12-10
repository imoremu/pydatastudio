'''
Created on 26 feb. 2021

@author: imoreno
'''
from pandas.core.frame import DataFrame
from pydatastudio.logging import Logging

logger = Logging.getLogger(__name__)

def research_index_max_level (research, level = 0):     
    '''
        Returns the max level of a research index
        
        E.g.:
        
        Research A:
            Goal 1:
                Subgoal 1:
                    DATAFRAME
            Goal 2:
                Subgoal 2:
                    DATAFRAME
                    
        Will return Level 3             
                    
    '''
    if not isinstance(research, dict) or not research: 
        
        logger.debug(f"Research: {research} has level 0")
        logger.debug(f"Research type is: {type(research)}")
        
        return level 
    
    return max(research_index_max_level(research[key], level + 1) for key in research) 
 

def summary_research(research):
    '''
        Returns the number of rows of the dataframe in the 
        
        E.g.:
        
        Input:
        
            Group_1:
                Sub_group_1:
                    Goal 1:
                        Subgoal 1_1:
                            DATAFRAME (4 rows)
                        Subgoal 1_2:
                            DATAFRAME (5 rows)
                            
                    Goal 2:
                        Subgoal 2:
                            DATAFRAME (3 rows)
                    
        Will return:
            Group_1: 
                Subgroup_1: 
                    Dataframe (Rows goals, Columns subgoals, value = number or dataframe rows)
                    
        If no group or subgroup: Only Dataframe is returned
        
        If max level is below 3, exception is returned                         
                    
    '''
        
    if not isinstance(research, dict) or not research:
        raise Exception (f"Research is not well defined. It has to be a dict with DataFrame on the leaves")
        
    if research_index_max_level(research) == 1:
        result = {}
        
        subgoals = []
        values = []

        for key, value in research.items():
            subgoals.append(key)
            values.append(value.shape[0])
            
        result = {"subgoal" : subgoals, "value" : values}

    elif research_index_max_level(research) == 2:

        data = {"goal": [], "subgoal" : [], "value": []}
                
        for key, value in research.items():
            data_subgoal = summary_research(value)
            
            for key_sub, value_sub in data_subgoal.items():
                data[key_sub].extend(value_sub)

            data["goal"].extend([key] * len(data_subgoal["subgoal"]))                        
        
        result = DataFrame.from_dict(data)
    
    else:
        
        result = {}
        
        for key, value in research.items():
            
            result.update({key: summary_research(value)})                   
        
        
    return result     
    