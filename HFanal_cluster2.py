import pandas as pd
import matplotlib.pyplot as plt
import HFanal_basicstats as bs

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

# record bad patient IDs
bad_id = []

"""Correlation Studies for PS mfccs, panels compare each """
intertrial_means = bs.intertrial_stats()



