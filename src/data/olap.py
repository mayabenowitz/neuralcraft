import sys
import os
ROOT_DIR = os.path.dirname(os.path.abspath('...'))
sys.path.insert(0, os.path.abspath(ROOT_DIR))

from functools import reduce
from copy import deepcopy
from typing import Callable
import datetime
import re

import pandas as pd
import numpy as np


class Tesseract(object):
    """This class is used for the analysis and visualization of multi-dimensional
    time-series data. It instantiates an OLAP-like cube for user-defined dynamic
    grouping, aggregating, filtering and the application of user-defined calculations
    and functions at run-time.
    """

    def __init__(self, df, precision=None):
        """
        Parameters
        -----------
        df: pandas DataFrame

        precision: int
            Sets the precision of the returned DataFrame


        Attributes
        -----------
        df: pandas DataFrame
            Returns the DataFrame passed to Tesseract

        precision: int
            Returns the set precision

        current_date: datetime object
            Returns the current date, assumed to be the datetime of the last row
            in the DataFrame.

        current_year: str
            Returns the current year, assumed to be the year of the datetime for the
            last row in the DataFrame.

        current_month: int
            Returns the current month, assumed to be the month of the datetime for the
            last row in the DataFrame.


        Inherits
        ---------
        GridApp
            Class that connects various JS APIs through ipywidgets for
            interactive data viz.

        """

        if precision is None:
            self.df = df
        if precision is not None:
            self.precision = precision
            self.df = df.round(self.precision)

        GridApp.__init__(self, df)

    def copy(self):
        """Returns a deepcopy of a Tesseract object.
        """
        self = deepcopy(self)
        return self

    def date(self, by_date, frequency=None):
        """Filters a pandas.DataFrame by date.

        Parameters
        -----------
        by_date: str
            Valid args: year_to_date, month_do_date, trailing_{ int }_months,
            trailing_{ int }_years

        frequency (optional): int
            Filters the pandas.DataFrame by datetime index to the desired
            frequency. Valid args: daily, monthly, quarterly, yearly.

        Returns
        --------
        self.df: pandas.DataFrame
            Dataframe filtered by date.
        """
        self.current_date = self.df.index.unique()[-1]
        self.current_year = str(self.current_date.year)
        self.current_month = self.current_date.month

        # filter dates by frequency
        if frequency is not None:
            self.df = filter_dates(self.df, frequency=frequency)

        # filter dates by year or month to date
        if by_date == "year_to_date":
            self.df = self.df[self.current_year]
        if by_date == "month_do_date":
            self.df = self.df[self.df["month"] == self.current_month]

        try:
            # extracts the integer digit from the by_date argument if there is one
            instances = [
                int(i) for i in by_date.replace("_", " ").split() if i.isdigit()
            ][0]

            # filters dataframe by trailing months
            if "trailing" and "month" in by_date:
                self.df = trailing_dates(
                    self.df,
                    start_date=self.current_date,
                    instances=instances,
                    unique_dates=False,
                )

            # filters dataframe by trailing years
            if "trailing" and "year" in by_date:
                self.df = trailing_dates(
                    self.df,
                    start_date=self.current_date,
                    instances=instances * 12,
                    unique_dates=False,
                )
        # if there is no integer digit in the by_date arg the try block is ignored
        except IndexError:
            pass
        return self

    def merge(self, data, on):
        """Merges a list of dataframes on the dataframe passed to Tesseract.

        Parameters
        -----------
        data: list[pandas.DataFrame]
            List of dataframes to merge.

        on: list[str]
            list of columns (keys) to merge the dataframes on.

        Returns
        --------
        self.df: pandas.DataFrame
            Merged dataframe
        """

        # creates a list of dataframes to merge and calls the enrich function
        # to do the heavy lifting
        self.df = [self.df]
        try:
            data = [df.round(self.precision) for df in data]
        except AttributeError:
            pass
        data = self.df + data
        self.df = enrich(data=data, merge_on=on)
        return self

    def group(
        self,
        by_fields=None,
        aggregate_by=None,
        by_calcs=None,
        post_agg_filter=None,
        post_calc_filter=None,
    ):
        """Dynamically applies user-defined grouping, aggregations, calculations, functions, and filters to the data.

        Parameters
        -----------
        by_fields: list[str]
            Fields (columns) to group by. This is otherwise known as the drill-down
            sequence. Order matters!

        aggregate_by: str, set[function], dict[str, function], or function
            Supports simple built-in aggregations (str args): 'sum', 'mean', 'median', 'count', 'std'.
            Supports user-defined aggregation functions. To apply a single custom agg function simply pass
            the function. To apply multiple custom agg functions pass a dictionary with column names as keys
            and the agg functions as values.

        by_calcs: function (optional)
            User-defined function/calculation to apply to the underlying dataframe after grouping and
            aggregating but before filtering.

        post_agg_filter: str (optional)
            Filters post-aggregation and pre-application of any calculations with a
            Pandas query on the dataframe. See the pandas.DataFrame.query method
            for more information.

        post_calc_filter: str (optional)
            Filters post-aggregation and post-application of any calculations with a
            Pandas query on the dataframe. See the pandas.DataFrame.query method
            for more information.

        Raises
        -------
        KeyError
            Raised if the passed columns of the by_fields arg are not in the DataFrame.

        Returns
        --------
        self.df: pandas.DataFrame
            Aggregated DataFrame.
        """

        if by_fields is None:
            return self

        self.by_fields = by_fields

        # asserts fields passed to the by_fields arg are all valid column names.
        # should be moved to a seperate decorator.
        try:
            col_list = self.df.columns.tolist()
            valid = [i in self.df.columns for i in self.by_fields]
            df_valid = pd.DataFrame({"input": self.by_fields, "valid": valid})
            df_invalid = df_valid[df_valid["valid"] == False]["input"].tolist()
            assert all(valid)
        except AssertionError:
            raise KeyError(
                "{} are/is invalid field name(s).".format(df_invalid),
                "Please choose fields from the following options: {}".format(col_list),
            )

        # groups the dataframe and applies simple aggregations.
        if isinstance(aggregate_by, str) is True:
            if aggregate_by == "sum":
                self.df = self.df.groupby(by_fields).sum()
            if aggregate_by == "mean":
                self.df = self.df.groupby(by_fields).mean()
            if aggregate_by == "median":
                self.df = self.df.groupby(by_fields).median()
            if aggregate_by == "count":
                self.df = self.df.groupby(by_fields).count()
            if aggregate_by == "std":
                self.df = self.df.groupby(by_fields).std()

        # groups the dataframe and applies user-defined aggregation functions
        if (
            isinstance(aggregate_by, dict) or isinstance(aggregate_by, Callable)
        ) is True:
            self.df = self.df.groupby(by_fields).agg(aggregate_by)

        self.df.reset_index(level=by_fields, inplace=True)

        # applies filter post-aggregation
        if post_agg_filter is not None:
            self.df = self.df.query(post_agg_filter)

        if by_calcs is not None:
            # lets user apply custom function
            def apply_func(func):
                self.df = func(self.df)
                return self.df

            self.df = apply_func(by_calcs)

            try:
                self.df = self.df.round(self.precision)
            except AttributeError:
                pass

        # applies filter post-agg and post-calc
        if post_calc_filter is not None:
            self.df = self.df.query(post_calc_filter)
        return self

    def view(self, by_calcs=None, pre_calc_filter=None, post_calc_filter=None):
        """Dynamically applies user-defined calculations and filters to an aggregated dataframe.

        Parameters
        -----------
        by_calcs: dict[functions]
            User-defined calculations/functions to be applied post-aggregation.

        pre_calc_filter: function or dict[str, function] (optional)
            User-defined filter applied before application of calcs. Passed function
            filters on a slice-by-slice basis.

        post_calc_filter: string (optional)
            Filters the dataframe with a pandas.DataFrame.query post-application of
            user-defined calculations. (See pandas query method for more info.)

        Raises
        -------
        TypeError, KeyError, NameError, SyntaxError
            Rasied if the data is not properly cleaned for the pandas.DataFrame.query method.
            (The method will attempt to clean then data for you and print a message if successful.)

        Returns
        --------
        self.df: pandas.DataFrame
            DataFrame with applied calculations and filters.
        """

        if by_calcs is None:
            return self

        # removes the time dimension from the by_fields arg. Resulting fields
        # are used to apply calculations.
        self.by_fields = [
            i for i in self.by_fields if i != "month" if i != "year" if i != "day"
        ]

        # make this a decorator?
        def chop():
            def return_df_slices():
                # slices the dataframe by field with a list of dictionaries.
                slices = self.df[self.by_fields].drop_duplicates().to_dict("records")
                """
                Example
                --------
                A simple example:

                df = pd.DataFrame(
                    {
                        'fruits': ['apple', 'banna', 'pear'],
                        'veggies': ['potatoe','carrot','celery']
                    }
                )

                >>> df
                    fruits  veggies
                  0  apple  potatoe
                  1  banna   carrot
                  2   pear   celery

                by_fields = ['fruits', 'veggies']

                >>> slices
                [{'fruits': 'apple', 'veggies': 'potatoe'},
                {'fruits': 'banna', 'veggies': 'carrot'},
                {'fruits': 'pear', 'veggies': 'celery'}]
                """

                # builds a list of strings from slices's keys and values
                query_list = [
                    " & ".join([f"({k}=='{v}')" for k, v in slices[i].items()])
                    for i in range(0, len(slices))
                ]
                """
                Example
                --------
                Using the example df from above:

                >>> query_list
                ["(fruits=='apple') & (veggies=='potatoe')",
                "(fruits=='banna') & (veggies=='carrot')",
                "(fruits=='pear') & (veggies=='celery')"]
                """

                # breaks the dataframe down into a list of dataframes for each combination
                # of fields in the by_fields arg.
                df_slices_list = [self.df.query(query) for query in query_list]
                """
                Example
                -------
                Using query_list from above:

                >>>df_slices_list
                [
                      fruits  veggies
                    0  apple  potatoe,

                      fruits  veggies
                    1  banna   carrot,

                       fruits veggies
                    2   pear  celery
                ]
                """
                return df_slices_list

            # trys to run return_df_slices()
            try:
                df_slices_list = return_df_slices()
                return df_slices_list

            # if synatax, key, or name error is raised tries to clean the data
            except (SyntaxError, KeyError, NameError) as e:
                try:
                    print("Data too dirty! Attempting to clean...")
                    col_list = self.df.columns.tolist()

                    # iterates over every column and tries to remove string-breaking quotes
                    for col in col_list:
                        try:
                            self.df[col] = (
                                self.df[col].str.replace("'", "").str.replace('"', "")
                            )
                        except AttributeError:
                            continue

                    df_slices_list = return_df_slices()
                    print("Data successfully clean. Horay!")
                except (TypeError, KeyError, NameError, SyntaxError) as e:
                    print(
                        e,
                        "Failed to clean the data. Make sure there are no characters "
                        "that break nested strings in column names or rows.",
                    )
                    sys.exit(0)
                return df_slices_list

        df_slices_list = chop()

        # applies user-defined filter before calculations are applied.
        # Filter is applied per slice.
        if pre_calc_filter is not None:
            if isinstance(pre_calc_filter, Callable) is True:
                df_slices_list = list(filter(pre_calc_filter, df_slices_list))

            if isinstance(pre_calc_filter, dict) is True:
                df_slices_list = list(
                    filter(list(pre_calc_filter.values())[0], df_slices_list)
                )

        # first row of each sliced dataframe
        temp_df_list = [
            pd.DataFrame(df[self.by_fields].iloc[0]).T.reset_index()
            for df in df_slices_list
        ]

        # applies user-defined functions to each sliced dataframe
        def slice_apply_func(func, df):
            result = func(df)
            return result

        # returns a list of dictionaries of calcd values for each sliced dataframe
        applied_calc_dict_list = [
            {k: slice_apply_func(v, df) for k, v in by_calcs.items()}
            for df in df_slices_list
        ]

        # converts each dictionary of returned calcs per slice to a dataframe
        df_calcd_list = [
            pd.DataFrame.from_dict(d, orient="index").T.reset_index()
            for d in applied_calc_dict_list
        ]

        # zips the first row of each sliced dataframe (containing the group-by fields)
        # and the dataframes containing the returned calculations per slice
        # zipped_list = list(zip(temp_df_list, df_calcd_list))

        # converts list of tuples from zipped_list to a list of lists
        lol = [list(x) for x in zip(temp_df_list, df_calcd_list)]

        # merges the dataframes containing the group-by fields and the dataframes
        # containing the calculations for each slice
        df_final_list = [
            reduce(
                lambda left, right: pd.merge(
                    left, right, left_index=True, right_index=True
                ),
                pair,
            )
            for pair in lol
        ]

        # concats (stacks) each merged dataframe into a final dataframe
        df_final = pd.concat(df_final_list)
        df_final = df_final.drop(columns=["index_x", "index_y"])

        self.df = df_final

        try:
            self.df = self.df.round(self.precision)
        except AttributeError:
            pass

        if post_calc_filter is None:
            return self

        # applies user-defined filter after calculations are applied.
        if post_calc_filter is not None:
            self.df = self.df.query(post_calc_filter)
            return self

