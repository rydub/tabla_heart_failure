import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# paths for required data
metadata_path = 'features/metadata_HF.csv'
audio_features_path = 'features/audio_features_HF.csv'
recordings_path = 'features/recordings_HF.csv'

# import data as 2D np arrays, string type?
metadata = pd.read_csv(metadata_path)
audio_features = pd.read_csv(audio_features_path)
audio_pd = audio_features.as_matrix()
recordings = pd.read_csv(recordings_path)

# create a dict of historic weights for calculation, _test var limits to good data for now
patients_test = ['HF001', 'HF002', 'HF003', 'HF004']
historic_weights = {}
for patient in patients_test:
	historic_weights[patient] = metadata.loc(patient, 'Historical Weight (kgs)')

# We create a dict of lists of tuples keyed by the dependent variable (audio feature) used
# tuples have form (weight, value)
# ex: {'PS_mean_mfcc_0': [(weight1, mfcc1), (weight2, mfcc2), ...]}
headings = audio_features[:,0]
catalogue = {}
features = list(audio_pd.columns.values)
for feature in range(1, len(features)):
	for recording in range(1, 15):
		this_record = headings[recording]
		label = this_record[:5]
		weight = recordings.loc(this_record, 'Weight(kgs)')
		weight_change = ((weight - historic_weights[label]) / historic_weights[label]) * 100

		catalogue[features[feature]] = (float(weight_change), 
			float(audio_pd.loc[recording, feature]))

print catalogue


