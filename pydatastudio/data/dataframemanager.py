'''
Created on 4 dic. 2019

@author: imoreno
'''


import pandas as pd
from pandas.core.frame import DataFrame

from re import match

import logging

class DataFrameManager(object):
    '''
    Utility class for managing and manipulating Pandas DataFrame objects.

    '''

    @classmethod
    def obtain_dataframe_manager_from_sheet(cls, ws, strip_str=False):
        '''
        Create a DataFrameManager instance from worksheet data.

        :param ws: Worksheet data.
        :type ws: iterable
        :param strip_str: Flag to indicate if string columns should be stripped.
        :type strip_str: bool
        :return: DataFrameManager instance.
        :rtype: DataFrameManager

        '''
        data = ws.values
        columns = next(data)[0:]
        dataframe = pd.DataFrame(data, columns=columns)
        return cls(dataframe, strip_str)

    def __init__(self, dataframe, strip_str=False):
        '''
        Constructor

        :param dataframe: Pandas DataFrame object.
        :type dataframe: DataFrame
        :param strip_str: Flag to indicate if string columns should be stripped.
        :type strip_str: bool

        '''
        self.logger = logging.getLogger(__name__)
        self.dataframe = dataframe

        if strip_str:
            for column in dataframe:
                try:
                    idx = dataframe[column].first_valid_index()
                    first_valid_value = dataframe[column].loc[idx] if idx is not None else None

                    if first_valid_value and isinstance(first_valid_value, str):
                        dataframe[column] = dataframe[column].str.strip()
                        dataframe[column] = dataframe[column].str.replace("_x000D_", "")
                        dataframe[column] = dataframe[column].str.replace("_x000A_", "")
                except:
                    self.logger.error(f"Column {column} is not a string.")

    def obtain_filtered_data(self, data_filter, dataframe=None):
        '''
        Return data filtered by a dictionary or a list of dictionaries.

        The dictionary represents an AND condition for all key-value pairs (column name and value).
        The value can be a regular expression, an equality expression (=), inequality expressions (<, >),
        or a callable function with a DataFrame as the only parameter.

        :param data_filter: Data filter.
        :type data_filter: dict or list
        :param dataframe: Optional DataFrame to apply filtering.
        :type dataframe: DataFrame
        :return: Filtered DataFrame.
        :rtype: DataFrame

        '''
        if dataframe is None:
            dataframe = self.dataframe
        
        result = None

        if isinstance(data_filter, list):
            for base_data_filter in data_filter:
                result = pd.concat([result, self.obtain_filtered_data(base_data_filter, dataframe)], ignore_index=True)
                result = result.drop_duplicates(ignore_index=True)
                
        else:
            for key, value in data_filter.items():
                self.logger.debug(f"Applying filter {key}: {value}")

                if not dataframe.empty:
                    if callable(value):
                        result = dataframe.loc[value]

                    elif isinstance(value, str):
                        if match("^[<>=]", str(value)):
                            query_key = key
                            
                            if " " in query_key:
                                query_key = f"`{key}`"
                            
                            result = dataframe.query(f"{query_key} {value}")
                        
                        else:
                            value = f"^{value}$"
                            is_filtered = dataframe[key].str.match(value, na=False)
                            result = dataframe[is_filtered]

                    elif isinstance(value, list):
                        result = self.obtain_filtered_data(value, dataframe)

                    else:
                        result = dataframe[(dataframe[key] == value)]
                    
                    self.logger.debug(f"Filtered data for {key}: {result}")


        return result