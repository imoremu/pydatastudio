"""
Created on 21 feb. 2021

@author: imoreno
"""
import time
import unittest
import pandas as pd
import os

from unittest.mock import Mock, patch
from pandas.core.frame import DataFrame

from pydatastudio.environment.environment_config_management import (
    get_environment_by_config,
)
from pydatastudio.environment.base_environment import BaseEnvironmentObject
from pydatastudio.data.studio.editors.basicexceleditor import BasicExcelEditor
from pydatastudio.data.studio.data_studio import DataStudio
from pydatastudio.resources_manager import get_resource_path


class TestBasicExcelEditor(unittest.TestCase):
    environment_data = {
        "config_name": "TEST",
        "Current": "Test",
        "Test": {
            "editors": {
                "basic editor": {
                    "researches": {
                        "research 1": {
                            "outputs": {
                                "research 1": {
                                    "save": True,
                                    "type": "Dataframe",
                                    "filter": {"level 1": ".*B"},
                                    "levels": {
                                        "level 1": "sheet",
                                        "level 2": "goal",
                                        "level 3": "subgroup",
                                        "level 4": "group",
                                    },
                                    "file": "./output/test/data/studio/editors/{date} - {group} - Test File - {goal}.xlsx",
                                    "sheet": "Test - {sheet}",
                                }
                            }
                        },
                        "research 2": {
                            "outputs": {
                                "sub_research 2": {
                                    "save": False,
                                    "type": "Dataframe",
                                    "file": "./output/test/data/studio/editors/{date} - Test File 2.xlsx",
                                    "sheet": "Test Sheet",
                                },
                                "sub_research 3": {
                                    "save": True,
                                    "type": "Dataframe",
                                    "file": "./output/test/data/studio/editors/{date} - Test File 3.xlsx",
                                    "sheet": "Test Sheet",
                                },
                            }
                        },
                    }
                }
            }
        },
    }

    def setUp(self):
        environment_parser = get_environment_by_config(
            TestBasicExcelEditor.environment_data
        )

        environment = BaseEnvironmentObject(environment_parser)

        self.editor = BasicExcelEditor(environment)

    def tearDown(self):
        pass

    @patch("pydatastudio.data.studio.editors.basicexceleditor.Thread")
    def test_save_research_calls_save_research_thread_with_correct_attributes(
        self, mock_thread
    ):
        # Create an instance of BasicExcelEditor class
        environment_config = Mock()
        excel_editor = BasicExcelEditor(environment_config)

        # Define some test values
        studio = Mock()
        research_name = "my_research"
        attrs = {"key": "value"}

        # Call the _save_research method
        excel_editor._save_research(studio, research_name, **attrs)

        # Verify that the thread was called with the correct attributes
        mock_thread.assert_called_once_with(
            target=excel_editor._save_research_thread,
            args=(studio, research_name),
            kwargs=attrs,
        )

        mock_thread_instance = mock_thread.return_value
        mock_thread_instance.start.assert_called_once()

    def test_save_research_with_saving_enabled(self):
        data = {
            "Group A": {
                "Sub Group A": {
                    "Goal A": {
                        "Sheet A": DataFrame.from_dict({"A": [1, 2, 3]}),
                        "Sheet B": DataFrame.from_dict({"B": [4, 5, 6]}),
                    },
                    "Goal B": {
                        "Sheet B": DataFrame.from_dict({"A": [5, 2, 9]}),
                        "Sheet D": DataFrame.from_dict({"B": [7, 8, 9]}),
                    },
                }
            }
        }

        studio = Mock()
        studio.research = Mock(return_value=data)

        self.editor._save_research_thread(
            studio, "research 1"
        )  # _save_research is tested in test_save_research_calls_save_research_thread_with_correct_attributes

        current_date = pd.to_datetime("now").strftime("%d_%m_%Y")

        file_path_goal_a = get_resource_path(
            f"./output/test/data/studio/editors/{current_date} - Group A - Test File - Goal A.xlsx"
        )
        expected_data_goal_a = {
            "Test - Sheet B": {"B": [4, 5, 6]}
        }  # Test - Sheet A is filtered
        self.assert_file_content_equals_expected(file_path_goal_a, expected_data_goal_a)

        file_path_goal_b = get_resource_path(
            f"./output/test/data/studio/editors/{current_date} - Group A - Test File - Goal B.xlsx"
        )
        expected_data_goal_b = {
            "Test - Sheet B": {"A": [5, 2, 9]}
        }  # Test - Sheet A is filtered

        self.assert_file_content_equals_expected(file_path_goal_b, expected_data_goal_b)

    def test_save_research_with_saving_disabled(self):
        data = DataFrame.from_dict({"A": [4, 5, 6]})

        studio = Mock(spec=DataStudio)
        studio.research = Mock(return_value=data)

        self.editor._save_research_thread(studio, "research 2")

        current_date = pd.to_datetime("now").strftime("%d_%m_%Y")

        filepath_sub_research_2 = get_resource_path(
            f"./output/test/data/studio/editors/{current_date} - Test File 2.xlsx"
        )

        filepath_sub_research_3 = get_resource_path(
            f"./output/test/data/studio/editors/{current_date} - Test File 3.xlsx"
        )

        self.assertTrue(
            os.path.exists(filepath_sub_research_3),
            f"El archivo {filepath_sub_research_3} no existe.",
        )
        self.assertFalse(
            os.path.exists(filepath_sub_research_2),
            f"El archivo {filepath_sub_research_2} existe.",
        )

    def assert_file_content_equals_expected(self, file_path, expected_data):
        self.assertTrue(os.path.exists(file_path), f"El archivo {file_path} no existe.")

        loaded_data = pd.read_excel(
            file_path, sheet_name=None, index_col=0, engine="openpyxl"
        )  # Cargar todas las hojas

        for sheet_name, expected_sheet_data in expected_data.items():
            self.assertIn(
                sheet_name,
                loaded_data,
                f"La hoja {sheet_name} no existe en el archivo.",
            )

            exceldf = loaded_data[sheet_name]
            expecteddf = pd.DataFrame(expected_sheet_data)

            pd.testing.assert_frame_equal(exceldf, expecteddf)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testSaveResearchInExcel']
    unittest.main()