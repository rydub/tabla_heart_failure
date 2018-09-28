#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 14:45:20 2018

@author: yashasaxena
"""

#script to generate spectrum plots for tabla hf patients

'''Set Parameters'''
#location
#patient
#filenames array (for loop through patient file to collect files, filenames)
##use test = features.loc['HF001'].groupby('date').max() 
##test.index.values to get array of dates

'''Collect feature/magnitude arrays'''
'''Match feature/magnitude array to fluid level'''
#get_fluid_list('HF001') to get array of fluid levels
#this fluid list will be aligned with order of dates array 

'''Plot'''
#borrow from plotting section of Emily's code 
