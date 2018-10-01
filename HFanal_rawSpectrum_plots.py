#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 14:45:20 2018

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
patient = 'HF004'
dates = features.loc[patient].groupby('date').max() 
dates = dates.index.values
fluids = get_fluid_list(patient)
#filename root folder
#path = 'raw_data/heart_failure/'

'''Collect feature/magnitude arrays and Plot'''
fig = plt.figure()
plt.title(patient + ' ' + location + ' ' + 'Magnitude vs Frequency')
for x in range(len(dates)):
    #data
    date_mod = '0'+str(dates[x])
    spectrum_data = audio_to_spectrum(patient,date_mod,location)
    freqs = spectrum_data[0]
    mags = spectrum_data[1]
    fluid_level = fluids[x]
    #add to plot 
    plt.plot(freqs, mags, label=str(fluid_level) + "_mL")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.xlim(0,1000)
plt.ylim(-20,100)
plt.show()