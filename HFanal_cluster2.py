import pandas as pd
import matplotlib.pyplot as plt
from math import isnan

# style selector for pyplot
# print(plt.style.available)
plt.style.use('seaborn-ticks')


# function found on: https://stats.stackexchange.com/questions/70801/how-to-normalize-data-to-0-1-range
def normalize(df):
    """Normalize a pandas dataframe along columns using min-max normalization, returns a copy"""

    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


# paths for required data
metadata_path = 'features/metadata_HF.csv'
audio_features_path = 'features/audio_features_HF.csv'
recordings_path = 'features/recordings_HF.csv'
expanded_features_path = 'features/audio_features_expanded_HF.csv'

# record bad patient IDs
bad_id = []

# dataframes
expanded_features = pd.read_csv(expanded_features_path)
indices = expanded_features.columns.tolist()[:5]
expanded_features.set_index(indices, inplace=True)
exp_ps_features = expanded_features.sort_index().xs('PS', level=2)

"""Correlation Studies for mfccs, panels compare each feature to the other per location, per"""