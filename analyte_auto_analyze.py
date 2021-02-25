import pandas as pd
import datetime as dt
import time
import calendar
import os

def analyte_function(trax_path,path):

    # change path to the path where we want analyzed data to end up
    os.chdir(path) 

    # generate a dataframe
    data = pd.read_excel(trax_path,'Custom Data Export', usecols='A, C:F')
    df = pd.DataFrame(data)

    # return a list of the dates
    start_date = df['Collection Date'].min().replace(day=1,hour=0,minute=0,second=0)
    end_date = df['Collection Date'].max()
    month = start_date.month
    year = start_date.year
    analyte = df['Analyte'].value_counts().idxmax().split(' ')[0]

    # chlorine requires and individual report per week
    if analyte == 'Chlorine':
        last_date_month = dt.datetime(end_date.year, end_date.month,calendar.monthrange(end_date.year,end_date.month)[-1]).replace(hour=23,minute=59,second=59)
        critical_date_list = []
        while start_date <= (last_date_month + dt.timedelta(seconds=1)):
            critical_date_list.append(start_date)
            start_date += dt.timedelta(days=7)
        if start_date > last_date_month:
            critical_date_list.append(last_date_month)

        # loop through and create --  wipe dataframe to save to excel sheet
        for i in range(1,len(critical_date_list)):
            temp = df[(df['Collection Date'] >= critical_date_list[i-1]) & (df['Collection Date'] < critical_date_list[i])]
            if temp.empty == True:
                pass
            else:
                temp = temp.groupby(['Regulators ID'])['Reading Result'].agg('mean')
                temp.to_excel(f'{analyte}_W{i}_{month}_{year}.xlsx')

    # pH, LSI, Turbidity
    else:
        df = df.groupby(['Regulators ID'])['Reading Result'].agg('mean')
        df.to_excel(f'{analyte}_{month}_{year}.xlsx')

