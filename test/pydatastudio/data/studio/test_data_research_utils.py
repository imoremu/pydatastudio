'''
Created on 26 feb. 2021

@author: imoreno
'''
import unittest

from pandas.core.frame import DataFrame
from pandas.testing import assert_frame_equal

from pydatastudio.data.studio.data_research_utils import research_index_max_level, summary_research


data_goal_1 = {"A" : [1,2,3], "B" : [4,5,6]}
data_goal_2 = {"C" : [1,2,3,4], "D" : [4,5,6,7]}  
    
df_1 = DataFrame.from_dict(data_goal_1)
df_2 = DataFrame.from_dict(data_goal_2)

dict = {"Research A" : 
            { "Group 1" :
                {
                    "Subgroup 1" :
                    {
                        "Goal 1" : 
                        {
                            "Subgoal 1_1": df_1,
                            "Subgoal 1_2": df_2
                        }
                    ,            
                        "Goal 2" : 
                        {
                            "Subgoal 1": df_2
                        }
                    }
                }
            }                        
       }

expected_summary =  { "Group 1" :
                        {
                            "Subgroup 1" :                            
                                DataFrame.from_dict(
                                    {
                                        "goal" : ["Goal 1", "Goal 1", "Goal 2"],
                                        "subgoal" : ["Subgoal 1_1", "Subgoal 1_2", "Subgoal 1"],
                                        "value" : [3,4,4]                                                                    
                                    }
                                )                            
                        }
                    }   
                        

expected_summary_last_level = {
                            "subgoal": ["Subgoal 1_1", "Subgoal 1_2"],
                            "value" : [3,4]
                        }       

class Test(unittest.TestCase):
        
    def testResearchIndexMaxLevel(self):
        
        self.assertEqual(4, research_index_max_level(dict["Research A"]))


    def testResearchSummary(self):
        
        assert_frame_equal(expected_summary["Group 1"]["Subgroup 1"], summary_research(dict["Research A"])["Group 1"]["Subgroup 1"])
    
    def testResearchSummaryLastLevel(self): 
        self.assertEqual(expected_summary_last_level, summary_research(dict["Research A"]["Group 1"]["Subgroup 1"]["Goal 1"]))
        
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testResearcgIndexMaxLevel']
    unittest.main()