import pandas as pd
from pandas import ExcelFile
from pandas import ExcelWriter
import xlrd


def nonwear_log_reader(filepath):
    df = pd.read_excel(filepath)

    print(df)

    print("Column Headings: ")
    print(df.columns)

    # print(df['Off'])
    # print(df['On'])
    # print(df['Structured Removal'])

    off_list = df['Off']
    on_list = df['On']
    structured_removal_list = df['Structured Removal']

    # print("Off: ", off_list)
    # print("On: ", on_list)
    print("Structured Removal: ", structured_removal_list)

    off_list = pd.to_datetime(off_list)
    on_list = pd.to_datetime((on_list))

    print("Off: ", off_list)
    print("On: ", on_list)

    for element in structured_removal_list:
        if "Yes" in structured_removal_list:
            print(True)
        if "No" in structured_removal_list:
            print(False)
        else:
            print("No structured removal")
    return df

