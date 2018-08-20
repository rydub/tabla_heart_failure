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

# dataframes
metadata = pd.read_csv(metadata_path, index_col=0)
audio_features = pd.read_csv(audio_features_path, index_col=0, usecols=range(13))
recordings = pd.read_csv(recordings_path, index_col=0)
norm_features = normalize(audio_features)

# merge datetime to features, generate date series
dates = recordings['Date of Recordings']
norm_features = norm_features.merge(pd.DataFrame(dates), left_index=True, right_index=True)
date_series = pd.to_datetime(norm_features['Date of Recordings'], infer_datetime_format=True)

pat_full_idx = ['HF001', 'HF002', 'HF003', 'HF004', 'HF005', 'HF006', 'HF007', 'HF008', 'HF009',
                'HF010', 'HF011', 'HF012', 'HF013', 'HF015', 'HF016', 'HF017', 'HF018', ]
pat_interest_idx = ['HF001', 'HF002', 'HF006', 'HF009', 'HF018']
mfcc_idx = list(norm_features)[:-1]

"""Examine trend across days of visit between patients with valid time series"""
# visit dict maps ID to record IDs and num days since admission for each measurement. Ex: {ID: (ID_MMDDYY, list)}
# visit_dict = {}
# for pat in pat_interest_idx:
#     record_ids = _extract_record_names(norm_features, pat)
#     base_date = date_series[record_ids[0]]
#     num_days = []
#     for entry in record_ids:
#         num_days.append(int((date_series[entry] - base_date).days))
#     visit_dict[pat] = (record_ids, num_days)
#
# legend = []
# i = 1
# for feature in mfcc_idx:
#     fig = plt.figure(i)
#     lgd = pat_interest_idx[:]
#     for pat in pat_interest_idx:
#         y_vals = []
#         for record in visit_dict[pat][0]:
#             y_vals.append(norm_features.loc[record, feature])
#         plt.plot(visit_dict[pat][1], y_vals)
#         plt.scatter(visit_dict[pat][1], y_vals, marker='.')
#     plt.title('{}: (normalized) value over time'.format(feature))
#     plt.xlabel('Days since admission')
#     plt.legend(lgd)
#     # save results
#     plt.savefig('HF_results/figures/{}_overtime_expanded.png'.format(feature), format='png')
#     plt.close(fig)
#     # show results
#     plt.show()
#     i += 1

"""Examine weight deltas over time between patients with multiple measurements"""
# weight dict maps ID to record IDs and weight change from base weight for each measurement. Ex: {ID: (ID_MMDDYY, list)}
# weight_series = recordings['Weight(kgs)']
# weight_dict = {}
# for pat in pat_interest_idx:
#     record_ids = _extract_record_names(norm_features, pat)
#     base_weight = metadata.loc[pat, 'Historical Weight (kgs)']
#     weights = []
#     keep_ids = []
#     for i in range(len(record_ids)):
#         weight = float(weight_series[record_ids[i]])
#         if not isnan(weight):
#             keep_ids.append(record_ids[i])
#             weight_change = (weight - base_weight) / base_weight
#             weights.append(weight_change)
#     weight_dict[pat] = (keep_ids, weights[:])
#
# legend = []
# i = 1
# for feature in mfcc_idx:
#     fig = plt.figure(i)
#     lgd = pat_interest_idx[:]
#     for pat in pat_interest_idx:
#         y_vals = []
#         for record in weight_dict[pat][0]:
#             y_vals.append(norm_features.loc[record, feature])
#         plt.plot(weight_dict[pat][1], y_vals)
#         plt.scatter(weight_dict[pat][1], y_vals, marker='.')
#     plt.title('{}: (normalized) value vs. Weight Change'.format(feature))
#     plt.xlabel('Weight Change from Historic Weight (% increase)')
#     plt.legend(lgd)
#     # save results
#     # plt.savefig('HF_results/figures/{}_vs_fluidweight_absolute.png'.format(feature), format='png')
#     # plt.close(fig)
#     i += 1

# show results
plt.show()


