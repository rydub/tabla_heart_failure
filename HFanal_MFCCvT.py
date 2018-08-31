## Script to plot MFCC results over time for a particular patient ##
import pandas as pd
import matplotlib.pyplot as plt
import csv
import scipy
from scipy import stats
import numpy as np
from datetime import datetime
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
df_indexed = df.set_index(['patient_id','date','localization'])
#select relevant data for analysis
df_MFCCvT = df_indexed.loc['HF018',:]
#normalize MFCC coefficients
df_MFCCvT = normalize(df_MFCCvT)
df_MFCCvT = df_MFCCvT.groupby('date').mean()
first_visit = min(df_MFCCvT.index)
first_visit = datetime.strptime(str(first_visit), "%m%d%y")
#create admit days column for time variable
admit_days = []
for x in range(len(df_MFCCvT.index)):
    index_val = df_MFCCvT.index[x]
    date = datetime.strptime(str(index_val), "%m%d%y")
    date_diff = date - first_visit
    n_days = date_diff.days
    admit_days.append(n_days)    
df_MFCCvT['admit_days']=admit_days

#multiple line plot
fig, axarr = plt.subplots(3, 4)
axarr[0, 0].bar( 'admit_days', 'mfcc_00', data=df_MFCCvT, color='olive')
axarr[0, 1].bar( 'admit_days', 'mfcc_01', data=df_MFCCvT, color='chartreuse')
axarr[0, 2].bar( 'admit_days', 'mfcc_02', data=df_MFCCvT, color='palegreen')
axarr[0, 3].bar( 'admit_days', 'mfcc_03', data=df_MFCCvT, color='darkgreen')
axarr[1, 0].bar( 'admit_days', 'mfcc_04', data=df_MFCCvT, color='seagreen')
axarr[1, 1].bar( 'admit_days', 'mfcc_05', data=df_MFCCvT, color='mediumspringgreen')
axarr[1, 2].bar( 'admit_days', 'mfcc_06', data=df_MFCCvT, color='lightseagreen')
axarr[1, 3].bar( 'admit_days', 'mfcc_07', data=df_MFCCvT, color='paleturquoise')
axarr[2, 0].bar( 'admit_days', 'mfcc_08', data=df_MFCCvT, color='darkcyan')
axarr[2, 1].bar( 'admit_days', 'mfcc_09', data=df_MFCCvT, color='darkturquoise')
axarr[2, 2].bar( 'admit_days', 'mfcc_10', data=df_MFCCvT, color='deepskyblue')
axarr[2, 3].bar( 'admit_days', 'mfcc_11', data=df_MFCCvT, color='aliceblue')

