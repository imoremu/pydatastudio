'''
Created on 14 feb. 2021

@author: imoreno
'''
from pydatastudio.data.studio import datastudioconstants
from pydatastudio.data.studio.datastudioconstants import ENVIRONMENT_INPUT_KEY,\
    ENVIRONMENT_RESEARCHES_KEY, ENVIRONMENT_STUDENT_KEY
from pydatastudio.logging import Logging


class DataStudentConfiguration(object):
    '''
    classdocs      
    '''
    INITIAL_RESEARCH_KEY = "Initial Researches"

    def __init__(self, configuration):
        '''
        Constructor
        
        :param
        
        configuration: Dict of the type:
        
            student: [student name]
            researchs:
               research 1:
                  initial : [True|False]
                  input: {}                                  
                  output:{}
                  filter:{}                        
                  attrs: {}
                      
               research 2:
                  initial : [True|False]
                  input: {}                                  
                  output:{}
                  filter:{}                        
                  attrs: {}
            ...
            
               research n:                  
                  initial : [True|False]
                  input: {}                                  
                  output:{}
                  filter:{}      
                  attrs: {}                    
        '''
        self.logger = Logging.getLogger(self.__class__.__module__)
        
        self.configuration = configuration
        
        self.name = configuration[ENVIRONMENT_STUDENT_KEY]        
        self.researches = configuration[ENVIRONMENT_RESEARCHES_KEY]
        
        self.required_researches = None
        
        self.info = {}                           
    
    def obtain_researches(self):
        '''
        Returns all the researches the student is able to produce
        '''
        return self.researches
    
    def obtain_initial_researches(self):        
        '''
        Return which researches the student provides when included in a studio
        '''
        result = []
        
        if DataStudentConfiguration.INITIAL_RESEARCH_KEY in self.info.keys():
            result = self.info[DataStudentConfiguration.INITIAL_RESEARCH_KEY]
        else:
            for research_name, research in self.obtain_researches().items():
                # If research has no defined initial attribute, research is not generated initially
                if (datastudioconstants.ENVIRONMENT_INITIAL_KEY in research and 
                   research[datastudioconstants.ENVIRONMENT_INITIAL_KEY]):
                        
                        result.append(research_name)
                    
            self.info[DataStudentConfiguration.INITIAL_RESEARCH_KEY] = result
            
        return result
            

    def obtain_required_researches(self, update = False):
        '''
        Return which researches the student requires (and ask for automatically) when research <code>research_name</code> is provided
        '''        
        if self.required_researches is None or update:            
        
            self.required_researches = {}                    
            
            for research_name, research in self.obtain_researches().items():                                                                          
                
                if (ENVIRONMENT_INPUT_KEY in research and 
                    ENVIRONMENT_RESEARCHES_KEY in research[ENVIRONMENT_INPUT_KEY]):
                
                    required_researches = research[ENVIRONMENT_INPUT_KEY][ENVIRONMENT_RESEARCHES_KEY]                                                                                                                                                                                        
                               
                    self.required_researches[research_name] = required_researches                                         
            
                else: 
                    self.required_researches[research_name] = None
                      
        return self.required_researches