import numpy as np
import scipy.stats
import scipy.spatial
import random
import math
import sys
import csv

class CreateDictionary():
    def __init__(self, csv_data, data_type_meta):
        """

        :param csv_data: raw data table
        :param data_type_meta: data type of each column (Temporal, Numerical, Categorical)
        """

        self.csv_data = csv_data
        self.data_type_meta = data_type_meta

    def initialize_dic(self):
        """
        column dictionary :
        "data" : column data
        "data_type" : column data type
        "avg" : column data average (if "data_type" = numerical)
        "min" : column data minimum (if "data_type" = numerical)
        "max" : column data maximum (if "data_type" = numerical)
        "trend" : column data trend value
        :return:
        """
        csv_contents = self.csv_data[0]
        csv_data_table = self.csv_data[1:]

        count = 0
        column_dic = {}
        for item in csv_contents:
            column_dic[item] = {}
            column_dic[item]["data"] = np.transpose(csv_data_table)[count]
            column_dic[item]["data_type"] = self.data_type_meta[count]
            if column_dic[item]["data_type"] == "num":
                for i in range(len(column_dic[item]["data"])):
                    if column_dic[item]["data"][i] == "":
                        column_dic[item]["data"][i] = "0"
                column_dic[item]["data"] = column_dic[item]["data"].astype(float)
                column_dic[item]["enum"], column_dic[item]["avg"] = self.calculate_Avg(column_dic[item]["data"])
                column_dic[item]["min"], column_dic[item]["max"], column_dic[item]["std"], column_dic[item]["var"], \
                column_dic[item]["qua_1"], column_dic[item]["med"], column_dic[item]["qua_3"] = self.calculate_Stat(column_dic[item]["data"])
            count += 1


        return column_dic

    def calculate_Avg(self, column):
        """
        enum : count nonzero elements
        avg : calculate average of nonzero elements
        :param column: input column
        :return: enum, avg
        """
        enum = np.count_nonzero(column)
        avg = np.sum(column)/np.count_nonzero(column)
        return enum, avg

    def create_nonzero_column(self, column):
        nonzero_index = np.nonzero(column)
        nonzero_column = []
        for item in nonzero_index:
            nonzero_column.append(column[item])
        return nonzero_column

    def calculate_Stat(self, column):
        """
        min, max, std, var : statistical data of column
        qua_1, med, qua_3 : quantile(0.25, 0.5, 0.75) of column data
        :param column: input column
        :return: min, max, std, var, qua_1, med, qua_3
        """
        nonzero_column = self.create_nonzero_column(column)
        qua_1 = np.quantile(nonzero_column, 0.25)
        med = np.quantile(nonzero_column, 0.5)
        qua_3 = np.quantile(nonzero_column, 0.75)
        min = np.min(nonzero_column)
        max = np.max(nonzero_column)
        std = np.std(nonzero_column)
        var = np.var(nonzero_column)
        return min, max, std, var, qua_1, med, qua_3