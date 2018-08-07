import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model
from math import isnan

# style selector for pyplot
# print(plt.style.available)
plt.style.use('seaborn-ticks')

# paths for required data
metadata_path = 'features/metadata_HF.csv'
audio_features_path = 'features/audio_features_HF.csv'
recordings_path = 'features/recordings_HF.csv'
# record bad patient IDs
bad_id = ['HF007']
# import data as 2D np arrays, string type?
metadata = pd.read_csv(metadata_path, index_col=0)
audio_features = pd.read_csv(audio_features_path, index_col=0, usecols=range(13))
recordings = pd.read_csv(recordings_path, index_col=0)
records = pd.Series(recordings.index.tolist())

# create a dict of lists of tuples keyed by the dependent variable (audio feature)
# tuples have form (weight, value)
# ex: {'PS_mean_mfcc_0': [(weight1, mfcc1), (weight2, mfcc2), ...]}
result_idx = audio_features.index.tolist()
catalogue = {}
features = audio_features.columns.values.tolist()
for feature in features:
    dict_entry = []
    for recording in [pat for pat in result_idx if pat not in bad_id]:
        patient_id = recording[:5]
        try:
            weight = float(recordings.loc[recording, 'Weight(kgs)'])
        except ValueError:
            # throw out record if no weight recorded
            continue
        # Current feature is assumed absolute fluid weight or difference between admission weight and "historic" weight
        expr = r'({}.*)'.format(patient_id)
        # pulls rows with patient_id then extracts the first instance.
        # throw our the patient if no weight is recorded at admission
        admission_id = records.str.extractall(expr).iloc[0, 0]
        try:
            if not isnan(float(recordings.loc[admission_id, 'Weight(kgs)'])):
                admission_weight = float(recordings.loc[admission_id, 'Weight(kgs)'])
            else:
                bad_id.append(patient_id)
                continue
        except ValueError:
            # throw out records with no weight recorded
            continue
        # assume historic_weight represents dry weight
        historic_weight = metadata.loc[patient_id, 'Historical Weight (kgs)']
        # avoid division by zero!!
        fluid_weight = (admission_weight - historic_weight) + .001
        weight = (weight - historic_weight)
        weight_change = (weight / fluid_weight) - 1
        dict_entry.append((float(weight_change), float(audio_features.loc[recording, feature])))
    catalogue[feature] = dict_entry

print catalogue
# train a linear regression for each audio feature, plot results
i = 1
for feature in features:
    [x, y] = zip(*catalogue[feature])
    x = np.array(x).reshape(-1, 1)
    y = np.array(y)
    regr = linear_model.LinearRegression()
    regr.fit(x, y)
    plt.figure(i)
    plt.scatter(x, y)
    plt.plot(x, regr.predict(x), color='red', linewidth=3)
    plt.title('Weight Change From Baseline vs. {}'.format(feature))
    plt.xlabel('Change in Assumed Fluid Weight (\% increase)')
    plt.ylabel(feature)
    i += 1
plt.show()
