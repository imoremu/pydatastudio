"""
Created on 13 feb. 2021

@author: imoreno
"""
from abc import abstractmethod
import logging

import traceback


class DataStudio():
    """
    classdocs

    Studio class for managing dataframes from different sources.

    Each studio will have:

    knowledge: dictionary [of dictionaries [of dictionaries ...]] of Dataframes objects
    students: objects of AbstractStudent subclass

    When a student is added, it adds its knowledge and complete previous knowledge

    The student also can perform several tasks (its own methods) to modify knowledge or provide reports

    The student can listen other students jobs in order to complete the job done with new information

    """

    def __init__(self, environment=None):
        """
        Constructor
        """
        self.environment = environment
        self.logger = logging.getLogger(__name__)

        self.knowledge = {}
        self.students = {}
        self.research_listeners = {}

    def add_studio_research(self, research_name, research):
        """
        Adds a research to the studio's knowledge base.
        :param research_name: Name of the research to be added
        :param research: The research data to be added, should be a dictionary.
        """
        self.knowledge[research_name] = research        

    def add_student(self, student_name, student):
        """
        Adds a student to the studio.
        :param student_name: Name of the student to be added
        :param student: The student object to be added, should be
        an AbstractStudent subclass.
        """
        if isinstance(student, AbstractStudent):
            self.students[student_name] = student
            student._join_studio(self)

        else:
            self.logger.error(
                "Incorrect Student. It should be AbstractStudent subclass"
            )

            raise InvalidStudentException(
                "Incorrect Student. It should be AbstractStudent subclass"
            )

    def research(self, research_name, student_name=None, update=False, **attrs):
        """
        Students that knows how to do the research will add their research to the knowledge object. This means that the student will have a method called:

            [research_method_name]_research

        Research method name will be research_name in lower case and with underscores in place of spaces

        If student_name is provided, only that student will generate report info

        Once the research is finished (a dict with report name and report content), it's stored in knowledge variable and
        all listener students are informed to perform related studies.

        Input attributes:

        :param research_name: Study to be done by the students
        :param **attrs: Attributes for report method
        :param student_name: Name of the student to create the report (all if None)
        """

        if not research_name in self.knowledge or update:
            self.logger.info(
                f"Studio research requested:\n Research: {research_name}\n\n -------------- "
            )

            self.knowledge[research_name] = {}

            if not student_name is None:
                try:
                    self.knowledge.update(
                        self.students[student_name]._research(research_name, **attrs)
                    )

                except:
                    self.logger.error(
                        f"Non valid attributes {str(attrs)} for method {research_name} in add on {student_name}"
                    )

            else:
                for studio_student_name, studio_student in self.students.items():
                    try:
                        if studio_student._is_research_provided(research_name):
                            self.knowledge.update(
                                studio_student._research(research_name, **attrs)
                            )

                            # only the first research is performed
                            break
                    except Exception:
                        trace = traceback.print_exc()

                        self.logger.error(
                            f"Exception in method {research_name} in student {studio_student_name}: {trace}"
                        )

            self.logger.info(f"Research {research_name} finished")

            self.research_finished(research_name, **attrs)

        return self.knowledge[research_name]

    def research_finished(self, research_name, **attrs):
        if research_name in self.research_listeners:
            for listener in self.research_listeners[research_name]:
                listener._research_finished(self, research_name, **attrs)

    def add_research_listener(self, research_name, listener):
        """
        add a listener to a specific research for postprocessing purposes
        """
        if not research_name in self.research_listeners.keys():
            self.research_listeners[research_name] = [listener]
        else:
            if listener in self.research_listeners[research_name]:
                self.logger.warn(
                    f"Listener {listener} already included in listener list of {research_name}"
                )
            else:
                self.research_listeners[research_name].append(listener)

    def remove_research_listener(self, research_name, student):
        """
        remove a listener to a specific research
        """
        if not research_name in self.research_listeners.keys():
            self.logger.warn(f"Report {research_name} not registered")
        else:
            if not student in self.research_listeners[research_name]:
                self.logger.warn(
                    f"Student {student} not included in listener list of {research_name}"
                )
            else:
                self.research_listeners[research_name].remove(student)

    def check_research_ready(self, research_name):
        result = True

        if not research_name in self.knowledge:
            result = False

        return result

    def check_research_provided(self, research_name):
        """
        Checks if the research is provided by any student in the studio
        """
        result = False

        for student_name, student in self.students.items():
            if student._is_research_provided(research_name):
                result = True
                break

        return result


class AbstractResearchListener:
    def __init__(self):
        """
        Constructor
        """

    @abstractmethod
    def _research_finished(self, studio, research_name, **attrs):
        pass


class AbstractStudent:
    """
    Abstratc class responsible of define Research Students.

    Methods of AbstractStudent should not be called directly. They're called from DataStudio objects only.

    """

    def __init__(self):
        """
        Constructor
        """

    @abstractmethod
    def _join_studio(self, studio, **attrs):
        """
        Actions done by the student when join the studio
        """
        pass

    @abstractmethod
    def _research(self, studio, research_name, **attrs):
        """
        Request of a research <research_name>

        Output:

            Dict with student name as key and research as value
        """
        pass

    @abstractmethod
    def _is_research_provided(self, research_name):
        """
        Returns True if research is provided by the student
        Returns False if research is not provided by the student
        """
        pass


class InvalidStudentException(Exception):
    pass


class ResearchNotFoundException(Exception):
    pass

class RequiredResearchNotFoundException(Exception):
    pass

