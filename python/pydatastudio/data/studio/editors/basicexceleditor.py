"""
Created on 21 feb. 2021

@author: imoreno
"""
import copy
from datetime import datetime
from threading import Thread, Lock
from pandas import ExcelWriter
from pandas.core.frame import DataFrame

import traceback
import re

from pydatastudio import resourcesmanager
from pydatastudio.data.studio.datastudio import AbstractResearchListener
from pydatastudio.logging import Logging
from pydatastudio.data.studio.editors.editorconstants import (
    EXCEL_EDITOR_CONFIGURATION_SAVE_KEY,
    EXCEL_EDITOR_CONFIGURATION_FILE_KEY,
    EXCEL_EDITOR_CONFIGURATION_SHEET_COLUMNS_KEY,
    EXCEL_EDITOR_CONFIGURATION_SHEET_KEY,
    EXCEL_EDITOR_CONFIGURATION_OUTPUT_RESEARCHES_KEY,
    EXCEL_EDITOR_CONFIGURATION_RESEARCH_BASE,
    EXCEL_EDITOR_CONFIGURATION_LEVELS_KEY,
    EXCEL_EDITOR_CONFIGURATION_LEVEL_KEY,
    EXCEL_EDITOR_CONFIGURATION_BASE_RESEARCH_KEY,
    EXCEL_EDITOR_CONFIGURATION_FILTER_KEY,
)
from pydatastudio.data.studio.dataresearchutils import research_index_max_level

class BasicExcelEditor(AbstractResearchListener):
    """
    Class responsible for handling and saving research data in Excel format coming from a data studio.

    It should be added as research listener to a specific studio. Once the studio generates a research, _research_finished is called.
    BasicExcelEditor stores the research based on environment file configuration.

    :param environment: The environment configuration for the Excel editor.
    :type environment: _EnvironmentConfig (get by environmentconfigmanagement)

    Attributes:
    - All attributes are private

    Methods:
    - All methods are private. They will be called due to the listener pattern

    Example:
    ```python
    environment_config = _EnvironmentConfig
    excel_editor = BasicExcelEditor(environment_config)
    ```
    """

    LOCK = Lock()

    def __init__(self, environment):
        """
        Constructor

        """
        self.logger = Logging.getLogger(self.__class__.__module__)
        self.environment = environment     
        self.files_created = []   

    def _research_finished(self, studio, research_name, **attrs):
        """
        Callback method triggered when a research is finished.

        :param studio: The data studio instance.
        :type studio: DataStudio
        :param research_name: The name of the finished research.
        :type research_name: str
        :param attrs: Additional attributes related to the finished research.
        :type attrs: dict
        """

        self._save_research(studio, research_name, **attrs)
    
    def _save_research(self, studio, research_name, **attrs):
        """
        Save the data of a completed research.

        :param studio: The data studio instance.
        :type studio: DataStudio
        :param research_name: The name of the finished research.
        :type research_name: str
        :param attrs: Additional attributes related to the finished research.
        :type attrs: dict
        """
        save_thread = Thread(
            target=self._save_research_thread,
            args=(studio, research_name),
            kwargs=attrs,
        )
        save_thread.start()


    def _save_research_thread(self, studio, research_name, **attrs):
        """
        Save thread

        :param studio: The data studio instance.
        :type studio: DataStudio
        :param research_name: The name of the finished research.
        :type research_name: str
        :param attrs: Additional attributes related to the finished research.
        :type attrs: dict
        """
        self.logger.info(f"Starting - Saving research {research_name}")

        output_attrs = EXCEL_EDITOR_CONFIGURATION_RESEARCH_BASE + [
            research_name,
            EXCEL_EDITOR_CONFIGURATION_OUTPUT_RESEARCHES_KEY,
        ]

        researchs_to_save = (
            self.environment.get_specific_config_value_without_formatting(
                *output_attrs, **attrs
            )
        )

        for edition_name in researchs_to_save.keys():
            if self._obtain_environment_research_attr(
                research_name,
                edition_name,
                EXCEL_EDITOR_CONFIGURATION_SAVE_KEY,
                **attrs,
            ):
                base_research = self._obtain_environment_research_attr(
                    research_name,
                    edition_name,
                    EXCEL_EDITOR_CONFIGURATION_BASE_RESEARCH_KEY,
                    **attrs,
                )

                if base_research is None:
                    output_research_name = edition_name
                else:
                    output_research_name = base_research

                data = copy.deepcopy(studio.research(output_research_name, **attrs))

                self.logger.info(
                    f"Creating saving thread for research {output_research_name}"
                )

                Logging.getPerformanceLogger().info(
                    f"\n ----- SAVING DATA -----\n Research: {research_name}\n Output: {edition_name}\n\n -------------- "
                )

                self._save_data(data, research_name, edition_name, **attrs)
                

    def _save_data(self, data, research_name, edition_name, **attrs):
        """
        Save data to Excel in a separate thread.

        :param data: The data to be saved.
        :type data: dict or pandas.DataFrame
        :param research_name: The name of the research associated with the data.
        :type research_name: str
        :param edition_name: The name of the edition associated with the data.
        :type edition_name: str
        :param attrs: Additional attributes related to the data.
        :type attrs: dict
        """
        try:
            self.logger.info(f"Starting - Save Data {research_name} - Attrs: {attrs}")

            time_format = "%d_%m_%Y"

            current_time = datetime.now().strftime(time_format)

            if attrs is None:
                attrs = {}

            attrs.update({"date": current_time})

            levels = self._obtain_environment_research_attr(
                research_name,
                edition_name,
                EXCEL_EDITOR_CONFIGURATION_LEVELS_KEY,
                **attrs,
            )

            if isinstance(data, dict):
                level_num = research_index_max_level(data)

                self.logger.debug(f"Saving: {data}")
                self.logger.debug(f"Level: {level_num}")

                level = levels[
                    EXCEL_EDITOR_CONFIGURATION_LEVEL_KEY + " " + str(level_num)
                ]

                level_filters = self._obtain_environment_research_attr(
                    research_name,
                    edition_name,
                    EXCEL_EDITOR_CONFIGURATION_FILTER_KEY,
                    **attrs,
                )

                level_filter = None

                if level_filters is not None:
                    self.logger.info(
                        f"Filter for {research_name} {edition_name} applicable: {level_filters}"
                    )

                    level_key = (
                        f"{EXCEL_EDITOR_CONFIGURATION_LEVEL_KEY} {str(level_num)}"
                    )

                    if level_key in level_filters:
                        level_filter = level_filters[level_key]

                        self.logger.info(
                            f"Filter for {research_name} {edition_name} level {level_key} applicable: {level_filter}"
                        )

                if self._check_unique_filename_by_level(
                    research_name, edition_name, level_num, **attrs
                ):
                    filename = self._obtain_environment_research_attr(
                        research_name,
                        edition_name,
                        EXCEL_EDITOR_CONFIGURATION_FILE_KEY,
                        **attrs,
                    )

                    Logging.getPerformanceLogger().info(
                        f"\n ----- SAVE DATA STARTED-----\n Research: {research_name}\n Output: {edition_name} - {filename}\n\n -------------- "
                    )

                    try:
                        self.logger.info(
                            f"Saving research {research_name} in file {filename}"
                        )
                                       
                        for key, value in data.items():
                            Logging.getPerformanceLogger().info(
                                f"\n ----- SAVE DATA STARTED-----\n Research: {research_name}\n Output: {edition_name} - {key}\n\n -------------- "
                            )

                            if level_filter is None or re.match(level_filter, key):
                                self.logger.info(f"Saving file {filename}")

                                attrs.update({level: key})
                                self._save_data(
                                    value, research_name, edition_name, **attrs
                                )

                                self.logger.info(f"File {filename} saved")
                            else:
                                self.logger.info(
                                    f"Key: {key} filtered in {research_name} research"
                                )

                            Logging.getPerformanceLogger().info(
                                f"\n ----- SAVE DATA FINISHED -----\n Research: {research_name}\n Output: {edition_name} - {key}\n\n -------------- "
                            )                                
                        
                        Logging.getPerformanceLogger().info(
                            f"\n ----- SAVE DATA FINISHED -----\n Research: {research_name}\n Output: {edition_name} - {filename}\n\n -------------- "
                        )

                    except Exception as e:
                        Logging.getPerformanceLogger().info(
                            f"\n ----- SAVE DATA FINISHED WITH ERROR -----\n Research: {research_name}\n Output: {edition_name} - {filename}\n\n -------------- "
                        )

                        if isinstance(e, IndexError):
                            self.logger.warning(
                                f"Saving {filename} of {edition_name} for research {research_name} is empty. No file is saved.\n"
                            )

                        else:
                            self.logger.error(
                                f"FAILURE: Saving {filename} of {edition_name} for research {research_name}\n"
                            )

                            raise e

                else:
                    for key, value in data.items():
                        attrs.update({level: key})
                        self._save_data(value, research_name, edition_name, **attrs)

            elif isinstance(data, DataFrame):
                filename = self._obtain_environment_research_attr(
                    research_name,
                    edition_name,
                    EXCEL_EDITOR_CONFIGURATION_FILE_KEY,
                    **attrs,
                )
                columns = self._obtain_environment_research_attr(
                    research_name,
                    edition_name,
                    EXCEL_EDITOR_CONFIGURATION_SHEET_COLUMNS_KEY,
                    **attrs,
                )
                sheet_name = self._obtain_environment_research_attr(
                    research_name,
                    edition_name,
                    EXCEL_EDITOR_CONFIGURATION_SHEET_KEY,
                    **attrs,
                )

                self.logger.info(
                    f"Saving data of {edition_name} for research {research_name} in sheet {sheet_name} of file {filename}"
                )

                if data.empty:
                    self.logger.info(
                        f"Sheet {sheet_name} of file {filename} empty. No sheet is created"
                    )

                else:
                    try:
                        with BasicExcelEditor.LOCK:                            
                            self._save_dataframe(
                                data, filename, sheet_name, columns, research_name
                            )                                                                                            

                        self.logger.info(f"Sheet {sheet_name} of file {filename} saved")

                    except Exception as e:
                        self.logger.error(
                            f"FAILURE: Saving sheet {sheet_name} of {edition_name} for research {research_name} in file {filename}\n"
                        )

                        raise e

        except:
            self.logger.error(
                f"FAILURE: Saving of {edition_name} for research {research_name}\n TRACE:"
            )

            traceback.print_exc()

        Logging.getPerformanceLogger().info(
            f"\n ----- SAVE DATA FINISHED -----\n Research: {research_name}\n Output: {edition_name}\n\n -------------- "
        )

    def _save_dataframe(self, data, filename, sheet_name, columns, research_name=""):
        """
        Save a DataFrame to Excel.

        :param data: The DataFrame to be saved.
        :type data: pandas.DataFrame
        :param writer: The ExcelWriter instance.
        :type writer: pandas.io.excel.ExcelWriter
        :param sheet_name: The name of the Excel sheet.
        :type sheet_name: str
        :param columns: The columns to include in the Excel sheet.
        :type columns: list or None
        :param research_name: The name of the associated research (optional).
        :type research_name: str
        """
        with self._obtain_writer_for_element(filename) as writer:
            self.logger.info(f"Saving DataFrame: Sheet: {sheet_name} in Research: {research_name} ")
            if columns is None:
                data.to_excel(writer, sheet_name)

            else:
                data_columns = data.columns

                displayed_columns = []

                for column in columns:
                    if column in data_columns:
                        displayed_columns.append(column)
                    else:
                        filename = writer.handles.handle.name
                        self.logger.warning(
                            f"Column {column} is not included in sheet {sheet_name} of current research data {research_name}. Filename: {filename}"
                        )

                self.logger.debug(f"Current data columns are: {data_columns} ")
                self.logger.debug(f"Displayed columns are: {columns} ")

                data.to_excel(writer, sheet_name, columns=displayed_columns)
        

    def _environment_contains_research_attr(
        self, research_name, output_research, attribute_name
    ):
        """
        Check if an attribute exists in the environment configuration for a specific research.

        :param research_name: The name of the research.
        :type research_name: str
        :param output_research: The name of the output research.
        :type output_research: str
        :param attribute_name: The name of the attribute to check.
        :type attribute_name: str
        :return: True if the attribute exists, False otherwise.
        :rtype: bool
        """        
        research_env_key = EXCEL_EDITOR_CONFIGURATION_RESEARCH_BASE + [
            research_name,
            EXCEL_EDITOR_CONFIGURATION_OUTPUT_RESEARCHES_KEY,
            output_research,
            attribute_name,
        ]

        result = attribute_name in self.environment.environment_contains(
            *research_env_key
        )

        return result

    def _obtain_environment_research_attr(
        self, research_name, output_research, attribute_name, **attrs
    ):
        """
        Obtain the value of a specific attribute from the environment configuration for a research.

        :param research_name: The name of the research.
        :type research_name: str
        :param output_research: The name of the output research.
        :type output_research: str
        :param attribute_name: The name of the attribute to retrieve.
        :type attribute_name: str
        :param attrs: Additional attributes related to the research.
        :type attrs: dict
        :return: The value of the specified attribute.
        :rtype: Any
        """
        result = None

        research_env_key = EXCEL_EDITOR_CONFIGURATION_RESEARCH_BASE + [
            research_name,
            EXCEL_EDITOR_CONFIGURATION_OUTPUT_RESEARCHES_KEY,
            output_research,
            attribute_name,
        ]

        if self.environment.environment_contains(*research_env_key):
            result = self.environment.get_specific_config_value(
                *research_env_key, **attrs
            )

        return result

    def _check_unique_filename_by_level(
        self, research_name, output_research, level_num, **attrs
    ):
        """
        Check if the filename is unique across different levels.

        :param research_name: The name of the research.
        :type research_name: str
        :param output_research: The name of the output research.
        :type output_research: str
        :param level_num: The number of levels to check.
        :type level_num: int
        :param attrs: Additional attributes related to the research.
        :type attrs: dict
        :return: True if the filename is unique, False otherwise.
        :rtype: bool
        """
        filename_key = EXCEL_EDITOR_CONFIGURATION_RESEARCH_BASE + [
            research_name,
            EXCEL_EDITOR_CONFIGURATION_OUTPUT_RESEARCHES_KEY,
            output_research,
            EXCEL_EDITOR_CONFIGURATION_FILE_KEY,
        ]

        filename = self.environment.get_config_value(*filename_key)

        levels = self._obtain_environment_research_attr(
            research_name,
            output_research,
            EXCEL_EDITOR_CONFIGURATION_LEVELS_KEY,
            **attrs,
        )

        result = True

        for level_id in range(1, level_num + 1):
            level = levels[EXCEL_EDITOR_CONFIGURATION_LEVEL_KEY + " " + str(level_id)]

            if re.match(f".*{{{level}.*", filename):
                result = False

        return result

    def _obtain_writer_for_element(self, filename, force=False):
        """
        Obtain an ExcelWriter instance for a given filename.

        :param filename: The name of the file.
        :type filename: str
        :param force: Force the creation of a new ExcelWriter instance.
        :type force: bool
        :return: The ExcelWriter instance.
        :rtype: pandas.io.excel.ExcelWriter
        """
        fileabspath = resourcesmanager.get_resource_path(filename)
        resourcesmanager.create_path_if_needed(fileabspath)

        return ExcelWriter(
                resourcesmanager.get_resource_path(fileabspath), engine="openpyxl", mode="w"
        )