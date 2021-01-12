# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 16:26:33 2020

@author: nathan brunner
"""

import pandas as pd
from glob import glob
import matplotlib.pyplot as plt
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

covid_github_folder = "C:\\"   # Should update this with actual location
jh_covid_data_folder = covid_github_folder+r"\csse_covid_19_data\csse_covid_19_daily_reports_us"
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

state_info = pd.read_excel('StatePops.xlsx')
