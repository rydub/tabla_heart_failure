#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 10:03:54 2018

@author: yashasaxena
"""

import matplotlib.pyplot as plt
from HFanal_utils import *
from audio_processing_util import *
#script to generate spectrum plots for tabla hf patients

'''Set Parameters'''
#location
location = 'RUL'
#patient, (HF001, HF002, HF004) & patient dates 
features = get_localized_features()
patients = ['HF001', 'HF009','HF010']
freqs_all = []
mags_all = []
fluids_all = []
for patient in patients: 
    dates = features.loc[patient].groupby('date').max() 
    dates = dates.index.values
    fluids = get_fluid_list(patient)
    min_fluid_ind = fluids.index(min(fluids))
    max_fluid_ind = fluids.index(max(fluids))
    #filename root folder
    #path = 'raw_data/heart_failure/'    
    '''Collect feature/magnitude arrays'''
    try:
        #data
        date_mod = '0'+str(dates[min_fluid_ind])
        spectrum_data_min = audio_to_spectrum(patient,date_mod,location)
        freqs_min = spectrum_data_min[0]
        mags_min = spectrum_data_min[1]
        fluid_level_min = min(fluids)
        #append to master arrays
        freqs_all.append(freqs_min)
        mags_all.append(mags_min)
        fluids_all.append(fluid_level_min)
    except: 
        pass
    try:
        #data
        date_mod = '0'+str(dates[max_fluid_ind])
        spectrum_data_max = audio_to_spectrum(patient,date_mod,location)
        freqs_max = spectrum_data_max[0]
        mags_max = spectrum_data_max[1]
        fluid_level_max = max(fluids)
        #append to master arrays
        freqs_all.append(freqs_max)
        mags_all.append(mags_max)
        fluids_all.append(fluid_level_max)      
    except:
        pass
'''Plot'''
fig = plt.figure()
plt.title(location + ' ' + 'Magnitude vs Frequency')
#plt.plot(freqs_all, mags_all, label=str(fluids_all) + "_mL")
for x in range(len(freqs_all)):
    plt.plot(freqs_all[x], mags_all[x], label=str(fluids_all[x]) + "_mL")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.xlim(0,1000)
plt.ylim(-20,100)
plt.show()