import pandas as pd
import matplotlib.pyplot as plt
import HFanal_basicstats as stats

# style selector for pyplot
# print(plt.style.available)
# plt.style.use('seaborn-ticks')


# Utils
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


"""Represent patient fluid flow as time series for review"""

recordings = pd.read_csv('features/recordings_HF.csv', index_col=0, usecols=range(9))
features = pd.read_csv('features/audio_features_HF.csv', index_col=0, usecols=range(13))
dates = recordings['Date of Recordings']
features = features.merge(pd.DataFrame(dates), left_index=True, right_index=True)
# HF007 omitted from full index because of multiple admission problem (09/03/18)
pat_full_idx = ['HF001', 'HF002', 'HF003', 'HF004', 'HF005', 'HF006', 'HF008', 'HF009',
                'HF010', 'HF011', 'HF012', 'HF013', 'HF015', 'HF016', 'HF017', 'HF018']

# visit_dict is a dict-of-dicts that maps ID to a dict of days since admission keye by record ID
#  Ex: {ID: (ID_MMDDYY, list)}
date_series = pd.to_datetime(features['Date of Recordings'], infer_datetime_format=True)
visit_dict = {}
for pat in pat_full_idx:
    record_ids = _extract_record_names(features, pat)
    base_date = date_series[record_ids[0]]
    num_days = []
    for entry in record_ids:
        num_days.append(int((date_series[entry] - base_date).days))
    visit_dict[pat] = (record_ids, num_days)


legend = []
lgd = pat_full_idx[:]
for pat in pat_full_idx:
    y_vals = []
    for record in _extract_record_names(features, pat):
        y_vals.append(recordings.loc[record, 'Fluid Up (mL)'])
    plt.plot(visit_dict[pat][1], y_vals)
    plt.scatter(visit_dict[pat][1], y_vals, marker='.')

plt.title('Fluid Excess Over Time by Patient')
plt.xlabel('Days Since First Recording')
plt.ylabel('Fluid Up (mL)')
plt.legend(lgd)
# save results
plt.savefig('HF_results/figures/fluid_loss.png', format='png')
plt.close()

# show results
# plt.show()