"""
Created on 30 mar. 2021

@author: imoreno
"""
import os
import re
from pydatastudio import resourcesmanager

from pandas.core.frame import DataFrame
from pydatastudio.logging import Logging
import pandas
from re import match
from pandas.core.series import Series
import traceback

logger = Logging.getLogger(__name__)


def obtain_dataframe_from_sheet(ws, strip_str=True):
    data = ws.values
    columns = next(data)[0:]

    dataframe = DataFrame(data, columns=columns)

    if strip_str:
        for column in dataframe:
            try:
                idx = dataframe[column].first_valid_index()  # Will return None
                first_valid_value = (
                    dataframe[column].loc[idx] if idx is not None else None
                )

                if first_valid_value and isinstance(first_valid_value, str):
                    dataframe[column] = dataframe[column].str.strip()
                    dataframe[column] = dataframe[column].str.replace("_x000D_", "")
                    dataframe[column] = dataframe[column].str.replace("_x000A_", "")

            except:
                logger.error("Column %s is not str" % (column))

    return dataframe


def data_filter_by_dataframe(dataframe_filter, dataframe):
    result = dataframe[data_selection_by_dataframe(dataframe_filter, dataframe)]

    return result


def data_selection_by_dataframe(dataframe_filter, dataframe):
    keys = list(dataframe_filter.columns.values)

    i1 = dataframe.set_index(keys).index
    i2 = dataframe_filter.set_index(keys).index

    return i1.isin(i2)


def data_filter_by_dict(data_filter, dataframe):
    """
    Returns Data filtered by a dict or a list of dict.

    This dict will represent an AND of all pairs Key (column name) and value.

    Each element of a list will represent an OR of all included dicts

    Each dict value can be a regular expression to match, an equality expression (=), inequality expressions (<, >) or a callable function with a dataframe as only parameter.

    :param data_filter: Data Filter
    :type  data_filter: Dict
    """
    result = dataframe

    if isinstance(data_filter, list):
        initial = True
        for base_data_filter in data_filter:
            if initial:
                result = data_filter_by_dict(base_data_filter, dataframe)
                initial = False

            else:
                result = pandas.concat(
                    [result, data_filter_by_dict(base_data_filter, dataframe)],
                    ignore_index=True,
                )
                result = result.drop_duplicates(ignore_index=True)

    else:
        for key, value in data_filter.items():
            logger.debug("Applying filter {}: {}".format(str(key), str(value)))

            current_filter = {key: value}

            selection = data_selection_by_dict(current_filter, result)

            if selection is not None:
                result = result[selection]

            logger.debug("Filtered data for {}: {}".format(str(key), str(result)))

    return result


def data_selection_by_dict(data_filter, dataframe):
    if isinstance(data_filter, list):
        result = Series([False] * dataframe.shape[0], dataframe.index)

        for base_data_filter in data_filter:
            result = result | data_selection_by_dict(base_data_filter, dataframe)

    else:
        index_name = dataframe.index.name

        result = Series([True] * dataframe.shape[0], dataframe.index)

        for key, value in data_filter.items():
            try:
                logger.debug("Selection {}: {}".format(str(key), str(value)))

                if not dataframe.empty:
                    if callable(value):
                        result = result & dataframe.apply(value, axis=1)

                    elif isinstance(value, str):
                        if match("^[<>=]", str(value)):
                            query_key = key

                            if " " in query_key:
                                query_key = "`" + key + "`"

                            result = result & dataframe.eval(query_key + value)

                        else:
                            # Included to manage exact match (if no specifically defined by regexp)
                            value = "^" + value + "$"

                            if key == index_name:
                                result = result & dataframe.index.str.match(value)

                            else:
                                nan = False

                                if "--EMPTY--" in value:
                                    nan = True

                                value = value.replace("--EMPTY--", "^\\s+$", 1)

                                result = result & dataframe[key].str.match(
                                    value, na=nan
                                )

                    elif isinstance(value, list):
                        result = result & data_selection_by_dict(value, dataframe)

                    else:
                        result = result & (dataframe[key] == value)

                    logger.debug(
                        "Filtered data for {}: {}".format(str(key), str(result))
                    )

            except:
                trace = traceback.print_exc()

                message = (
                    f"Key {key} for filter {str(data_filter)} not valid. Trace: {trace}"
                )
                logger.error(message)

                result = Series([False] * dataframe.shape[0], dataframe.index)

                raise Exception(message)

    return result


def merge_dataframes_by_function(first_dataframe, second_dataframe, merge_function):
    """
    Merges two DataFrames using a custom function.

    Args:
        first_dataframe (pandas.DataFrame): The first DataFrame.
        second_dataframe (pandas.DataFrame): The second DataFrame.
        merge_function (callable): A custom function to apply to each row of the first DataFrame.

    Returns:
        pandas.Series: The merged data.
    """
    logger.debug("Merging dataframes by function %s" % (str(merge_function)))

    result = first_dataframe.apply(
        lambda row: merge_function(row, second_dataframe), axis=1
    )

    return result
