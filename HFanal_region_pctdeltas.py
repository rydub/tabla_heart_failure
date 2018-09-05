#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 11:16:36 2018

@author: yashasaxena
"""
## Script to plot MFCC results over time for different lung regions ##
import pandas as pd
import matplotlib.pyplot as plt
import csv
import scipy
from scipy import stats
import numpy as np
from datetime import datetime, date
#functions
def normalize(df):
    """Normalize a pandas dataframe using min-max normalization, returns a copy"""
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result
#import dataset
filepath = 'HF_results/intertrial_means.csv'
df = pd.read_csv(filepath)
df_indexed = df.set_index(['patient_id','localization', 'date'])
patient_array = ['HF001', 'HF009', 'HF018']
patient = 'HF009'
MFCC = 'mfcc_01'

df_patient = df_indexed.loc[patient,:]
lung_regions = ['LLL','LML','LUL','RLL','RML','RUL']
#create 6 datasets, one for each lung region 
region_datasets = []
for region in lung_regions:
    df_region = df_patient.loc[region,:]
    visit_dates = df_region.index
    first_visit = str(min(df_region.index))
    first_visit_y = int(first_visit[-2:])
    first_visit_m = int(first_visit[:-4])
    first_visit_d = int((first_visit[:-2])[-2:])
    first_visit = date(first_visit_y, first_visit_m, first_visit_d)
    #create admit days column for time variable
    admit_days = []
    for x in range(len(df_region.index)):
        index_val = str(df_region.index[x])
        date_y = int(index_val[-2:])
        date_m = int(index_val[:-4])
        date_d = int((index_val[:-2])[-2:])
        date_visit = date(date_y, date_m, date_d)
        date_diff = date_visit - first_visit
        n_days = date_diff.days
        admit_days.append(n_days)    
    df_region['admit_days']=admit_days
    #create percentage change column 
    mfcc_pctdelta = []
    for y in range(len(df_region[MFCC])):
        if y==0:
            prev_val = df_patient[MFCC].values[y]
        else:
            prev_val = df_patient[MFCC].values[y-1]
        val = df_patient[MFCC].values[y]
        pct_delta = (val-prev_val)/val 
        mfcc_pctdelta.append(pct_delta)
    df_region['mfcc_pctdelta'] = mfcc_pctdelta 
    region_datasets.append(df_region)

##plot data
fig, axarr = plt.subplots(3,2, sharex=True, sharey=True)
counter = 0
for n in range(2):
    for m in range(3):
        axarr[m][n].bar( 'admit_days', 'mfcc_pctdelta', data=region_datasets[counter], color='olive')
        counter = counter + 1