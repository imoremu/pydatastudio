from pydatastudio.environment.baseenvironment import BaseEnvironmentObject

from pydatastudio.environment.exceptions import ConfigElementNotFoundException

class DataStudioEnvironment(BaseEnvironmentObject):

    """
    DataStudioEnvironment class that extends BaseEnvironmentObject to manage DataStudio-specific configurations.
    
    This class is designed to handle configurations related to the DataStudio, such as student configurations,
    research definitions, and editor settings.

    Data Studio environment has the next form:

        Config_name: Environment
        Current: [current environment name]
        
        enviroment name A:
            students:
                Student A:        
                    class: [class name]
                    config: 
                        student: Student A name
                        researchs:
                            Research A name:
                                initial : False
                                input: 
                                    researches: 
                                    - [research name]
                                    files:
                                    - [file name]
                                
                            Research B name:
                                initial : False
                                input: 
                                    researches: 
                                    - [research name]
                                    files:
                                    - [file name]
                                filter: [filter]                                    
                                output filter: [output filter]                        
                
            student_factory:
                class: [class name of the student factory, e.g., pydatastudio.data.studio.students.student_factory.StudentFactory]
            

    E.g.

    Config_name: PortfolioStudioEnvironment
    Current: default

        default:
        students:
            IRPF Capital Gains Losses Student:        
            class: pyportfolio.studio.students.irpf_capital_gains_losses_student.IRPFCapitalGainsLossesStudent
            config: 
                student: IRPF Capital Gains Losses Student
                researchs:
                    FIFO Earnings:
                    initial : False
                    input: 
                        researches: 
                        - portfolio initial data         
                        
                    IRPF Taxable Base:
                    initial : False
                    input: 
                        researchs: 
                        - FIFO Earnings


            IRPF Moveable Capital Income Student:
            class: pyportfolio.studio.students.irpf_moveable_capital_income_student.IRPFMoveableCapitalIncomeStudent
            config: 
                student: IRPF Moveable Capital Income Student
                researchs:
                    Dividend Income:
                    initial : False
                    input: 
                        researches: 
                        - portfolio initial data                                       

            General IRPF Student:
            class: pyportfolio.studio.students.general_irpf_student.GeneralIRPFStudent
            student: General IRPF Student
                researchs:
                    Loss Tax Compensation:
                    initial : False
                    input: 
                        researches: 
                        - IRPF Taxable Base
                        - Dividend IncomeConfig_name: PortfolioStudioEnvironment
        student_factory:
            class: pyportfolio.studio.students.student_factory.StudentFactory
               

    """

    def __init__(self, environment=None):
        """
        Constructor for DataStudioEnvironment.
        
        :param environment_parser: Optional environment parser to initialize the environment.
        """
        super().__init__(environment)

        self._check_config() # Call without argument, it will use self.environment

    def _check_config(self):
        """
        Validates the configuration of the DataStudio environment.
        
        :raises ConfigElementNotFoundException: If required configuration elements are missing.
        """
        # Check for student_factory configuration
        if not self.environment.has_config_value("student_factory"):
            raise ConfigElementNotFoundException("Missing 'student_factory' configuration in DataStudioEnvironment.")
        
        factory_config = self.environment.get_config_value("student_factory")
        if not isinstance(factory_config, dict):
            raise ConfigElementNotFoundException("Configuration for 'student_factory' is not a dictionary.")
        if "class" not in factory_config:
            raise ConfigElementNotFoundException("Missing 'class' in 'student_factory' configuration.")
        if "config" not in factory_config:
            raise ConfigElementNotFoundException("Missing 'config' in 'student_factory' configuration.")

        if not self.environment.has_config_value("students"):
            raise ConfigElementNotFoundException("Missing 'students' configuration in DataStudioEnvironment.")        
        
        
        # loop over students to check they are properly formatted:
        students = self.environment.get_config_value("students")
        
        for student_name, student_config in students.items():
            if not isinstance(student_config, dict):
                raise ConfigElementNotFoundException(f"Configuration for student '{student_name}' is not a dictionary.")
            
            if "class" not in student_config:
                raise ConfigElementNotFoundException(f"Missing 'class' in configuration for student '{student_name}'.")
            
            if "config" not in student_config:
                raise ConfigElementNotFoundException(f"Missing 'config' in configuration for student '{student_name}'.")
            
            if "researchs" not in student_config["config"]:
                raise ConfigElementNotFoundException(f"Missing 'researchs' in configuration for student '{student_name}'.")
        

    def get_students(self):
        """
        Retrieves the list of students defined in the environment.
        
        :return: A list of student names.
        """
        students = self.environment.get_config_value("students")

        return list(students.keys()) if students else []

    def get_student_configuration(self, student_name: str):
        """
        Retrieves the configuration for a specific student.
        
        :param student_name: The name of the student.
        :return: The student configuration.
        """
        return self.environment.get_config_value("students", student_name, "config")
    
    def get_student_class(self, student_name: str):
        """
        Retrieves the class path for a specific student.
        
        :param student_name: The name of the student.
        :return: The student class path.
        """
        return self.environment.get_config_value("students", student_name, "class")

    def get_student_research_configuration(self, student_name: str, research_name: str):
        """
        Retrieves the configuration for a specific research within a student.
        
        :param student_name: The name of the student.
        :param research_name: The name of the research.
        :return: The research configuration.
        """
        return self.environment.get_config_value("students", student_name, "config", "researchs", research_name)

    def get_student_research_names(self, student_name: str):
        """
        Retrieves the names of all researches for a specific student.
        
        :param student_name: The name of the student.
        :return: A list of research names.
        """
        researchs = self.environment.get_config_value("students", student_name, "config", "researchs")
        return list(researchs.keys()) if researchs else []      

    def get_student_factory_class_name(self) -> dict:
        """
        Retrieves the configuration for the student factory.
        
        :return: A dictionary containing the student factory's class path and its configuration.
        """
        return self.environment.get_config_value("student_factory.class")
   
