import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import isnan

# style selector for pyplot
# print(plt.style.available)
plt.style.use('seaborn-ticks')


# function found on: https://stats.stackexchange.com/questions/70801/how-to-normalize-data-to-0-1-range
def normalize(df):
    """Normalize a pandas dataframe using min-max normalization, returns a copy"""

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

# import data as Dataframes
metadata = pd.read_csv(metadata_path, index_col=0)
audio_features = pd.read_csv(audio_features_path, index_col=0, usecols=range(13))
recordings = pd.read_csv(recordings_path, index_col=0)

# normalize features
norm_features = normalize(audio_features)

# colormap for distinct color in visuals
colormap = [
        "FF0000", "00FF00", "0000FF", "FFFF00", "FF00FF", "00FFFF", "000000",
        "800000", "008000", "000080", "808000", "800080", "008080", "808080",
        "C00000", "00C000", "0000C0", "C0C000", "C000C0", "00C0C0", "C0C0C0",
        "400000", "004000", "000040", "404000", "400040", "004040", "404040",
        "200000", "002000", "000020", "202000", "200020", "002020", "202020",
        "600000", "006000", "000060", "606000", "600060", "006060", "606060",
        "A00000", "00A000", "0000A0", "A0A000", "A000A0", "00A0A0", "A0A0A0",
        "E00000", "00E000", "0000E0", "E0E000", "E000E0", "00E0E0", "E0E0E0",
        ]


# TEST: 1D analysis spreads coefficients along a unit vector
# plt.figure(1)
# legend = []
# for pat, clr in zip(norm_features.index, colormap):
#     data = norm_features.loc[pat].tolist()
#     plt.scatter(data, np.zeros(len(data)), color='#{}'.format(clr))
#     legend.append(pat)
# plt.legend(legend, ncol=3)
# plt.show()

# Cluster Analysis: per MFCC variance over time vs. variance across patients
mfcc_idx = list(norm_features)
pat_idx = ['HF001', 'HF002', 'HF003', 'HF004', 'HF005', 'HF006', 'HF007', 'HF008', 'HF009',
           'HF010', 'HF011', 'HF012', 'HF013', 'HF014', 'HF015', 'HF016', 'HF017', 'HF018', ]
legend = []
i = 1
# iterate over each patient, generating a plot for each
records = pd.Series(norm_features.index.tolist())
for pat in pat_idx:
    expr = r'({}.*)'.format(pat)
    to_extract = records.str.extractall(expr)
    print to_extract
    for cur_mfcc in mfcc_idx:
        fig = plt.figure(i)
        this_pat_mfcc = [norm_features.loc[entry, cur_mfcc] for entry in list(to_extract)]
        # for entry in to_extract.index[0].tolist():
        #     to_plot.append(norm_features.loc[entry, mfcc_])

        i += 1
        plt.close(fig)
