# -*- coding: utf-8 -*-
"""
Calculate and plot Covid statistics
Based off of Johns Hopkins data

https://github.com/CSSEGISandData/COVID-19/
"""

# Data Setup
import os
import sys
covid_github_folder = input("Paste location of JH github folder:")
# https://github.com/CSSEGISandData/COVID-19/ Use this repo for updated data
os.system(r'github '+covid_github_folder)     # Update data from github before plotting
response = input("Was GitHub updated? y/n: ")
if response == 'n':
    sys.exit()
elif response =='y':
    pass
else:
    print('Did not input y or n, stopping')
    sys.exit()

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import numpy as np
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
from covid_support import combine, cols, states, state_info
today = pd.datetime.today().strftime('%Y-%m-%d')
latest_data = combine.index.max().strftime('%Y-%m-%d')
print("Dashboard updated:\t{} \nLatest Data:\t\t{}".format(today,latest_data))

import matplotlib
matplotlib.rc('font',size=8)

# New Cases Per Capita
# TODO: Plot days ago to show indication of when cases may not be reported yet
plt.figure(figsize=(12,6))
for i,r in state_info.iloc[:8].iterrows():
    new_cases_per_pop = combine['Confirmed',r['State']].diff().rolling(7).mean()/(r['Pop']/1e5)
    plt.plot(combine.index, new_cases_per_pop,linewidth=3, label=r['State'])
plt.title('New Cases/100k/day 7d rolling')
plt.yscale('log')
plt.ylabel('log scale cases/100k')
plt.xlabel('Date')
plt.ylim(1e0,15e1)
plt.legend()
plt.grid(which='both')

plt.figure(figsize=(12,6))
for i,r in state_info.iloc[8:].iterrows():
    new_cases_per_pop =  combine['Confirmed',r['State']].diff().rolling(7).mean()/(r['Pop']/1e5)
    plt.plot(combine.index, new_cases_per_pop,linewidth=3, label=r['State'])
plt.title('New Cases/100k/day 7d rolling')
plt.yscale('log')
plt.ylabel('log scale cases/100k')
plt.xlabel('Date')
plt.ylim(1e0,15e1)
plt.legend()
plt.grid(which='both')


# Remove hospitalization as of 10/5
#Hospitalization estimation (limited data)
"""
plt.figure(figsize=(16,8))
for i,r in state_info[:8].iterrows():
    plt.plot(combine.index, combine['Hospitalization_Rate',r['State']], label=r['State'])
plt.title("Hospitalization per 100k")
plt.legend()
plt.figure(figsize=(16,8))
for i,r in state_info[8:].iterrows():
    plt.plot(combine.index, combine['Hospitalization_Rate',r['State']], label=r['State'])
plt.title("Hospitalization per 100k")
plt.legend()
"""

# Testing Rates
combine = combine['6/1/2020':]

for sub in [state_info[:8],state_info[8:]]:
    td = combine.index[-1]
    plt.figure(figsize=(12,6))
    plt.subplot(2,1,1)
    for i,r in sub.iterrows():
        new_cases_per_pop =  combine['Confirmed',r['State']].diff().rolling(7).mean()/(r['Pop']/1e5)
        new_tests_per_pop = combine['Testing_Rate',r['State']].diff().rolling(7).mean()
        new_tests_per_pop[new_tests_per_pop <0] = np.nan
        perc_test_pos = new_cases_per_pop/new_tests_per_pop
        plt.plot(combine.index, perc_test_pos, label=r['State'])
    plt.plot((pd.datetime(2020,6,8),td),(0.1,0.1), label='10% pos rate', c='y')
    plt.plot((pd.datetime(2020,6,8),td),(0.05,0.05), linewidth=3, label='5% pos rate', c='r')
    plt.plot([td - pd.Timedelta('14D')]*2,[0,0.2],'--',c='r',label='14d ago')
    plt.ylim(0,0.2)
    ax = plt.gca()
    ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.title("Testing Rate: positive/total tests")
    plt.ylabel("% positive tests")
    plt.legend(loc='upper left')
    # Testing Rates
    #plt.figure(figsize=(16,8))
    plt.subplot(2,1,2)
    for i,r in sub.iterrows():
        new_tests_per_pop = combine['Testing_Rate',r['State']].diff().rolling(7).mean()
        new_tests_per_pop[new_tests_per_pop <0] = np.nan
        plt.plot(combine.index, new_tests_per_pop, label=r['State'])
    plt.ylim(0,1000)
    plt.title("Testing per 100k")
    plt.ylabel('Total Tests per 100k')
    plt.legend()
    
county_data = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
df = pd.read_csv(county_data, parse_dates=[0])


mult_pop = 812855   # 2019 pop
har_pop = 4.713e6

mem_day = pd.datetime(2020,5,25)
first_protest = pd.datetime(2020,6,4)
five_day = pd.datetime.today()-pd.Timedelta('5 days')
marker = [0,50]
marker = [0,.01]

plt.figure(figsize=(12,6))
mult = df[df['county']=="Multnomah"]
mult.index = mult.date
mult['new_cases'] = mult['cases'].diff()
mult['smooth'] = mult['new_cases'].rolling(7).mean()
plt.bar(mult.index, mult.new_cases,color='grey',alpha=0.5,label='New Cases Raw')
plt.plot(mult.index, mult.smooth, label='7d avg',color='black')

#plt.plot([mem_day,mem_day],marker,c='r',label='Memorial Day')
#plt.plot([first_protest,first_protest],marker,c='orange',label='First Major Protest')
#plt.plot([five_day,five_day],marker,'--',c='gray',label='5d ago')

plt.legend()
plt.xlabel('Date')
plt.ylabel("New Cases")
plt.title("Mult. Co., OR - raw and 7d avg new cases")


marker = [0,1200]
marker = [0,.01]
har = df[(df['county']=="Harris") & (df['state']=="Texas")]
har.index = har.date
har['new_cases'] = har['cases'].diff()
har['smooth'] = har['new_cases'].rolling(7).mean()
plt.figure(figsize=(12,6))
plt.bar(har.index, har.new_cases,label='New Cases Raw',color='gray',alpha=0.5)
plt.plot(har.index, har.smooth, label='7d avg',color='black')
#plt.plot([mem_day,mem_day],marker,c='r',label='Memorial Day')
#plt.plot([first_protest,first_protest],marker,c='orange',label='First Major Protest')
#plt.plot([five_day,five_day],marker,c='green',label='5d ago')
plt.legend()
plt.ylabel("New Cases")
plt.title("Harris County - Raw and 7d avg New Cases")
plt.ylim(0,3000)

    
# Rate of Cases Change Estimation
d_i_r = 18    # Days from infection to recovery
subset = combine['6/1/20':]
plt.figure(figsize=(12,6))
for i,r in state_info[:8].iterrows():
    new_cases =  subset['Confirmed',r['State']].diff()
    #new_deaths = subset['Deaths',r['State']].diff() #TODO: add this for R_0 estimations?
    current_cases = subset['Confirmed',r['State']].diff().rolling(d_i_r).sum()   # Sum last 15 days of new cases to estimate currently infected number
    susceptible = r['Pop']-subset['Confirmed',r['State']]
    beta = new_cases/current_cases    # new cases/current infection
    mu = new_cases.shift(periods=d_i_r)/current_cases
    r_0 = (beta/mu).rolling(7).mean()
    plt.plot(subset.index, r_0,linewidth=3, label=r['State'])
plt.plot((pd.datetime(2020,6,25),subset.index[-1]),(1.0,1), linewidth=3, label='Constant Case Level', c='r')
plt.title('R_0 very basic estimation')
plt.ylabel('R_0')
plt.xlabel('Date')
plt.ylim(0,5)
plt.legend()
plt.grid(which='both')

plt.figure(figsize=(12,6))
for i,r in state_info[8:].iterrows():
    new_cases =  subset['Confirmed',r['State']].diff()
    #new_deaths = subset['Deaths',r['State']].diff() #TODO: add this for R_0 estimations?
    current_cases = subset['Confirmed',r['State']].diff().rolling(d_i_r).sum()   # Sum last 15 days of new cases to estimate currently infected number
    beta = new_cases/current_cases    # new cases/current infection
    mu = new_cases.shift(periods=d_i_r)/current_cases
    r_0 = (beta/mu).rolling(7).mean()
    plt.plot(subset.index, r_0,linewidth=3, label=r['State'])
plt.plot((pd.datetime(2020,6,25),subset.index[-1]),(1.0,1), linewidth=3, label='Constant Case Level', c='r')
plt.title('R_0 very basic estimation')
plt.ylabel('R_0')
plt.xlabel('Date')
plt.ylim(0,5)
plt.legend()
plt.grid(which='both')

# New Deaths Per Capita
# Context Deaths:
heart_disease = 647457/328.2e6*100000/365   # 197 per 100k people die of heart disease per year
car_deaths = 12/365 # .03 fatality per 100k per year from nhtsa in 2016
flu_deaths = 61000/328.2e6*100000/365

plt.figure(figsize=(12,6))
for i,r in state_info.iterrows():
    new_deaths_per_pop = combine['Deaths',r['State']].diff().rolling(7).mean()/(r['Pop']/1e5)
    plt.plot(combine.index, new_deaths_per_pop,linewidth=1, label=r['State'])
plt.plot((new_deaths_per_pop.index[0],new_deaths_per_pop.index[-1]),(heart_disease,heart_disease),'--',linewidth=2,c='k',label='Heart Disease Deaths/day/100k')
plt.plot((new_deaths_per_pop.index[0],new_deaths_per_pop.index[-1]),(flu_deaths,flu_deaths),'--',linewidth=2,label='Flu Deaths/day/100k')
plt.plot((new_deaths_per_pop.index[0],new_deaths_per_pop.index[-1]),(car_deaths,car_deaths),'--',linewidth=2,c='r',label='Car Deaths/day/100k')
plt.title('Context New Deaths/100k 7d rolling')
plt.yscale('log')
plt.ylabel('log scale cases/100k')
plt.xlabel('Date')
plt.ylim(1e-2,1e0)
plt.legend(loc=3)
plt.grid(which='both')

tot_stats = pd.DataFrame(columns=['TotPerc','CurrentPercent','CurrentUnderCounted'])

for i,r in state_info.iterrows():
    tot = combine['Confirmed',r['State']][-1]/(r['Pop'])
    current = combine['Confirmed',r['State']].diff().rolling(18).sum()[-1]/(r['Pop'])
    cur_more = current * 7.7
    tot_stats.loc[r['State']] = [tot,current,cur_more]

tot_stats.to_clipboard()    # Use this for tracking in a table
