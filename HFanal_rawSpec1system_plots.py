#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:03:54 2018

@author: yashasaxena
"""
import matplotlib.pyplot as plt
from HFanal_utils import *
from audio_processing_util import *
import numpy as np
#script to generate spectrum plots for tabla hf patients

'''Set Parameters'''
#location
locations = ['LLL','LML','LUL','RLL','RML','RUL']
#patient, (HF001, HF002, HF004) & patient dates 
features = get_localized_features()
patients = ['HF001','HF010']
thoracic_circs = [1.13, 1.30]
freqs_avg_all = []
mags_avg_all = []
freqs_min_all = []
freqs_max_all = []
mags_min_all = []
mags_max_all = []
fluids_all = []
n=0
for patient in patients: 
    dates = features.loc[patient].groupby('date').max() 
    dates = dates.index.values
    fluids = get_fluid_list(patient)
    fluid_level_min = min(fluids)
    fluids_all.append(fluid_level_min)
    fluid_level_max = max(fluids)
    fluids_all.append(fluid_level_max)
    min_fluid_ind = fluids.index(min(fluids))
    max_fluid_ind = fluids.index(max(fluids))
    #thoracic circumference for normalization
    t_c = thoracic_circs[n]
    n = n+1
    #filename root folder
    #path = 'raw_data/heart_failure/'    
    '''Collect feature/magnitude arrays'''
    for location in locations: 
        try:
            #data
            date_mod = '0'+str(dates[min_fluid_ind])
            #collect spectra from all 3 audio files 
            spectrum_data_min_1 = audio_to_spectrum(patient,date_mod,location, 1)
            spectrum_data_min_2 = audio_to_spectrum(patient,date_mod,location, 2)
            spectrum_data_min_3 = audio_to_spectrum(patient,date_mod,location, 3)
            freqs_min = [] 
            mags_min = []
            freqs_min.append(spectrum_data_min_1[0])
            freqs_min.append(spectrum_data_min_2[0])
            freqs_min.append(spectrum_data_min_3[0])
            freqs_min = np.mean(freqs_min, axis=0)
            
            mags_min.append(spectrum_data_min_1[1])
            mags_min.append(spectrum_data_min_2[1])
            mags_min.append(spectrum_data_min_3[1])
            mags_min = np.mean(mags_min, axis=0)*t_c
            #append to master arrays
            freqs_min_all.append(freqs_min)
            mags_min_all.append(mags_min)
        except: 
            pass
    #average frequencies collected at min fluid values from each location
    freqs_avg_all.append(np.mean(freqs_min_all, axis=0))
    mags_avg_all.append(np.mean(mags_min_all, axis=0))
    for location in locations:
        try:
            #data
            date_mod = '0'+str(dates[max_fluid_ind])
            spectrum_data_max_1 = audio_to_spectrum(patient,date_mod,location, 1)
            spectrum_data_max_2 = audio_to_spectrum(patient,date_mod,location, 2)
            spectrum_data_max_3 = audio_to_spectrum(patient,date_mod,location, 3)
            freqs_max = []
            mags_max = []
            freqs_max.append(spectrum_data_max_1[0])
            freqs_max.append(spectrum_data_max_2[0])
            freqs_max.append(spectrum_data_max_3[0])
            freqs_max = np.mean(freqs_max, axis=0)
            
            mags_max.append(spectrum_data_max_1[1])
            mags_max.append(spectrum_data_max_2[1])
            mags_max.append(spectrum_data_max_3[1])
            mags_max = np.mean(mags_max, axis=0)
            #append to master arrays
            freqs_max_all.append(freqs_max)
            mags_max_all.append(mags_max)      
        except:
            pass
    #average frequencies collected at max fluid values from each location
    freqs_avg_all.append(np.mean(freqs_max_all, axis=0))
    mags_avg_all.append(np.mean(mags_max_all, axis=0))
'''Plot'''
fig = plt.figure()
plt.title('Location Averaged' + ' ' + 'Magnitude vs Frequency')
#plt.plot(freqs_all, mags_all, label=str(fluids_all) + "_mL")
for x in range(len(freqs_avg_all)):
    plt.plot(freqs_avg_all[x], mags_avg_all[x], label=str(fluids_all[x]) + "_mL")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.xlim(0,1000)
plt.ylim(-20,200)
plt.show()