#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 13:11:45 2018

@author: yashasaxena
"""
import matplotlib.pyplot as plt
from HFanal_utils import *
import os
# style selector for pyplot
# print(plt.style.available)
plt.style.use('seaborn-ticks')

pat_idx = get_pat_idx()
features = get_localized_features()
recordings = get_patient_recordings()

"""select patient id and location id for plots"""
patient_id = ['HF001', 'HF009','HF018']
location_id = ['LLL','RLL']
feature_list = ['mfcc_00','mfcc_01','mfcc_02','mfcc_03','mfcc_04', 'mfcc_05',
            'mfcc_06','mfcc_07','mfcc_08','mfcc_09','mfcc_10','mfcc_11']
"""plot fluid overload vs feature val for selected locations and all patients"""
for feature in feature_list: 
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    for patient in patient_id:
        pat_features = normalize(features.loc[patient])
        fluids = get_fluid_list(patient)
        # swap level for location-based access, dates are sorted
        pat_features = pat_features.swaplevel(0, 1)
        locations = pat_features.index.levels[0].tolist()
        
        for location in location_id:
            feature_vals = pat_features[feature].loc[location].tolist()
            ax1.scatter(fluids,feature_vals, label = location)
            plt.legend(loc='upper left')
    plt.show()

