#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 13:11:45 2018

@author: yashasaxena
"""
import matplotlib.pyplot as plt
from HFanal_utils import *
#from audio_processing import * 

#import os
# style selector for pyplot
# print(plt.style.available)
plt.style.use('seaborn-ticks')

pat_idx = get_pat_idx()
features = get_localized_features()
recordings = get_patient_recordings()

"""select patient id and location id for plots"""
    
location_id = ['LLL']
feature_list = ['mfcc_00','mfcc_01','mfcc_02','mfcc_03','mfcc_04', 'mfcc_05',
            'mfcc_06','mfcc_07','mfcc_08','mfcc_09','mfcc_10','mfcc_11']

"""plot fluid overload vs feature val for selected locations and all patients"""
for feature in feature_list: 
    fig = plt.figure()
    ax1 = fig.add_subplot(111)

    for patient in pat_idx:
        #pat_features = normalize(features.loc[patient])
        pat_features = features.loc[patient]
        fluids = get_fluid_list(patient)
        # swap level for location-based access, dates are sorted
        pat_features = pat_features.swaplevel(0, 1)
        locations = pat_features.index.levels[0].tolist()
        
        for location in location_id:
            try:
                feature_vals = pat_features[feature].loc[location].tolist()
                ax1.scatter(fluids,feature_vals, label = patient)
                plt.title(feature)
                plt.xlabel('Fluid Overload')
                plt.ylabel('feature val')
            except:
                continue           
    plt.title(feature)
    plt.xlabel('Fluid Overload')
    plt.ylabel('feature val')
    plt.show()

