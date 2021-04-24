# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 16:26:33 2020

@author: nb137
"""

import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

BASEFOLDER = "redacted_github_file_location"

jh_covid_data_folder = BASEFOLDER + r"\csse_covid_19_data\csse_covid_19_daily_reports_us"
js_state_files = glob(jh_covid_data_folder+"\*.csv")

combine = pd.DataFrame()
for file in js_state_files:
    f = pd.read_csv(file)
    date = pd.to_datetime(file.split("\\")[-1][:-4])
    f['date'] = date
    combine = pd.concat([combine,f],axis=0,ignore_index=True)
    
# Remove columns I don't care about
combine.drop(['Lat','Long_','FIPS','UID','ISO3'],axis=1,inplace=True)
combine = combine[combine['Country_Region']=='US']
combine = combine.pivot_table(columns=['Province_State'],index=['date'])
cols,states = combine.columns.levels

state_info = pd.read_excel('StatePops.xlsx', engine='openpyxl')


def load_vaccine_data():
    #vaccine_data_location = "https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/raw_data/vaccine_data_us_state_timeline.csv"
    #archived
    archived_data_location = "https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/archive/vaccine_data_us_state_timeline.csv"
    # Archived data, old version we started using, broke out the 2 different vaccines as well as number of total doses, number of first and second doses, and others
    
    # updated data version
    vaccine_data_location = "https://raw.githubusercontent.com/govex/COVID-19/master/data_tables/vaccine_data/us_data/time_series/vaccine_data_us_timeline.csv"

    vf = pd.read_csv(vaccine_data_location,parse_dates=[1])
    vf = vf.pivot_table(columns=['Province_State'],index='Date')
    cols, states = vf.columns.levels
    
    return vf
    
    