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
                  input:
                    researches:
                        - research_name_1
                        - research_name_2
                        
                  input filters: 
                    filter name A: {}
                    filter name B: {}                                      
                  output filter:{}                        
                  attrs: {}
                      
               research 2:
                  initial : [True|False]
                  input: {}      
                  input filters: 
                    filter name X: {}
                    filter name Y: {}                                      
                  
                  output filter:{}                        
                  attrs: {}
            ...
            
               research n:                  
                  initial : [True|False]
                  input: {}      
                  input filters:{} 
                  output filter:{}     
                  attrs: {}             


        Attributes definition:

        - student: Name of the student
        - researches: Dictionary of researches, where each key is the research name and the value is a dictionary with the research configuration.
        - initial: Researches that the student provides automatically when included in a studio (even if it's not requested explicitly by any consumer).        
        - input: Dictionary of input sources for the research. Can contain 'files', 'researches', 'bbdd', 'dictionary' or any other source type. The student is responsible for interpreting and using these sources.               
        - input filters (Optional): Dictionary of filters (dictionary or a list of dictionaries) to be applied to input data.
        - output filter (Optional): Filters to be applied to output data. It can be a dictionary or a list of dictionaries.
        - attrs (Optional): Additional attributes for the research method.
        
        The configuration should be structured to allow the student to understand what researches it can perform, what inputs it needs, and how to filter the data.
        
        Note: To know more about filters and how to use them, please refer to the documentation of the DataFrameUtils class.
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