#python 3

import pandas as pd
import csv
import utilities

"""A handful of pandas-based scripts to analyze and edit your spreadsheet-based
collection control data."""

def combine_csvs():
    """Combine two datasets."""
    dataset_a = utilities.opencsv()
    dataset_b = utilities.opencsv()
    #fill in index column or add line for input...or don't have it?
    data_a = pd.read_csv(dataset_a, index_col='')
    data_b = pd.read_csv(dataset_b, index_col='')

    if len(data_a.columns) == len(data_b.columns):
        newdataset = data_a.append(data_b)
    else:
        newdataset = pd.concat([data_a, data_b])
    newdataset.to_csv('alldren.csv', encoding='utf-8')

def merge_csvs():
    """Join two spreadsheets on a common column."""
    data_a = utilities.opencsv()
    data_b = utilities.opencsv()
    dataset_a = pd.read_csv(data_a, encoding='utf-8')
    dataset_b = pd.read_csv(data_b, encoding='utf-8')
    headerlist = dataset_a.columns.values.tolist()
    headlist = str(headerlist)
    head = headlist[1:-1]
    print('Columns: ' + head)
    mergevar = input('Enter common column: ')
    merged = dataset_a.merge(dataset_b, on=mergevar, how='left')
    merged.to_csv('/Users/aliciadetelich/Desktop/agents_w_recs_merged.csv', encoding='utf-8')

# def join_csvs():
#     """DO NOT USE"""
#     pass

def group_by():
    """Get all values that meet a certain criteria"""
    def g(dataset):
        columnname = input('In what column is your group located?: ')
        groupname = input('What value are you looking for?')
        group = dataset.groupby(columnname)
        grouped = group.get_group(groupname)
        grouped.to_csv('group.csv', encoding='utf-8')
        print(grouped)
    stit = True
    def s():
        data = input('Please enter path to input CSV: ')
        dataset = pd.read_csv(data)
        headerlist = dataset.columns.values.tolist()
        headlist = str(headerlist)
        head = headlist[1:-1]
        print('Columns: ' + head)
        c = True
        while c:
            g(dataset)
    while stit:
        s()

def all_groups():
    """Get all values that meet a certain criteria."""
    data = utilities.opencsv()
    dataset = pd.read_csv(data)
    headerlist = dataset.columns.values.tolist()
    headlist = str(headerlist)
    head = headlist[1:-1]
    print('Columns: ' + head)
    columnname = input('In what column is your group located?: ')
#        groupname = input('What value are you looking for?')
    group = dataset.groupby(columnname)
    x = 0
    for i in group:
        x = x + 1
        grouped = group.get_group(i)
        grouped.to_csv(str(x) + '_group.csv', encoding='utf-8')
        print(grouped)

def get_val_counts():
    """Get count of values in a column."""
    data = utilities.opencsv()
    dataset = pd.read_csv(data)
    headerlist = dataset.columns.values.tolist()
    headlist = str(headerlist)
    head = headlist[1:-1]
    print('Columns: ' + head)
    columnname = input('Please enter column name: ')
    counts = dataset[columnname].value_counts()
    counts.to_csv('/Users/aliciadetelich/Desktop/extent_types_in_use_prod.csv', encoding='utf-8')
    print(counts)

def describe():
    """Get a summary of data."""
    dataset = utilities.opencsv()
    data = pd.read_csv(dataset)
    description = data.describe()
    description.to_csv('description.csv', encoding='utf-8')

#Get a date range - maybe later
##def get_date_range():
##    data = input('Please enter path to input CSV: ')
##    dataset = pd.read_csv(data)
##    start_date = input('Please enter the start date (mm/dd/yyyy): ')
##    timerange = input('Please enter time span (hours, days, years, etc.: ')
##    frequency = input('Please enter freqency (hours, days, years, etc.: ')
##    rng = pd.date_range(start_date, periods=timerange, freq=frequency)
##    print(rng)
##    rng.to_csv('time_range.csv', encoding='utf-8')
