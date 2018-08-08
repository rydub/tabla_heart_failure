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


def _extract_record_names(df, pat):
    """extract and return a list of the dated record IDs for a patient ID"""
    records = pd.Series(df.index.tolist())
    expr = r'({}.*)'.format(pat)
    return records.str.extractall(expr)[0].tolist()


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

# merge datetime to features, generate date series
dates = recordings['Date of Recordings']
norm_features = norm_features.merge(pd.DataFrame(dates), left_index=True, right_index=True)
date_series = pd.to_datetime(norm_features['Date of Recordings'], infer_datetime_format=True)

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

pat_full_idx = ['HF001', 'HF002', 'HF003', 'HF004', 'HF005', 'HF006', 'HF007', 'HF008', 'HF009',
                'HF010', 'HF011', 'HF012', 'HF013', 'HF015', 'HF016', 'HF017', 'HF018', ]
pat_interest_idx = ['HF001', 'HF009', 'HF018']
mfcc_idx = list(norm_features)[:-1]

# visit dict maps ID to record IDs and num days since admission for each measurement. Ex: {ID: (ID_MMDDYY, list)}
visit_dict = {}
for pat in pat_interest_idx:
    record_ids = _extract_record_names(norm_features, pat)
    base_date = date_series[record_ids[0]]
    num_days = []
    for entry in record_ids:
        num_days.append(int((date_series[entry] - base_date).days))
    visit_dict[pat] = (record_ids, num_days)

legend = []
i = 1

# Examine trend across days of visit between patients with valid time series
for feature in mfcc_idx:
    fig = plt.figure(i)
    lgd = pat_interest_idx[:]
    for pat in pat_interest_idx:
        y_vals = []
        for record in visit_dict[pat][0]:
            y_vals.append(audio_features.loc[record, feature])
        plt.plot(visit_dict[pat][1], y_vals)
        plt.scatter(visit_dict[pat][1], y_vals, marker='.')
    plt.title('{}: (normalized) value over time'.format(feature))
    plt.xlabel('Days since admission')
    plt.legend(lgd)

    # save results
    # plt.savefig('HF_results/figures/{}_overtime'.format(feature), format='png')
    # plt.close(fig)
    i += 1

# show results
plt.show()
