import pandas as pd
import matplotlib.pyplot as plt
import HFanal_basicstats as stats

# style selector for pyplot
# print(plt.style.available)
plt.style.use(u'seaborn-ticks')


"""Utils for analysis of features based on fluid accumulation"""


# function found on: https://stats.stackexchange.com/questions/70801/how-to-normalize-data-to-0-1-range
def normalize(df):
    """Column normalize a pandas dataframe using min-max normalization, returns a copy"""
    result = df.copy()
    for feature_name in df.columns:
        max_value = df[feature_name].max()
        min_value = df[feature_name].min()
        result[feature_name] = (df[feature_name] - min_value) / (max_value - min_value)
    return result


def get_visit_days(pat):
    """returns a list of days since admission for each record id for the patient"""
    features = _get_old_features()
    date_series = pd.to_datetime(features['Date of Recordings'], infer_datetime_format=True)
    record_ids = _extract_record_names(features, pat)
    base_date = date_series[record_ids[0]]
    num_days = []
    for entry in record_ids:
        num_days.append(int((date_series[entry] - base_date).days))
    return num_days


def get_fluid_day(record_id):
    """return the fluid overload in mL for the corresponding record id"""
    df = get_patient_recordings()
    return df.loc[record_id, 'Fluid Up (mL)']


def get_fluid_list(pat_id):
    return [get_fluid_day(record_id) for record_id in _extract_record_names(get_patient_recordings(), pat_id)]


def get_pat_idx():
    """returns list of patient ids usable for study (omits 007, 019)"""
    return ['HF001', 'HF002', 'HF003', 'HF004', 'HF005', 'HF006', 'HF008', 'HF009',
            'HF010', 'HF011', 'HF012', 'HF013', 'HF015', 'HF016', 'HF017', 'HF018']


def _extract_record_names(df, pat):
    """extract and return a list of the dated record IDs for a patient ID sorted by increasing date"""
    records = pd.Series(df.index.tolist())
    expr = r'({}.*)'.format(pat)
    ret = records.str.extractall(expr)[0].tolist()
    ret.sort()
    return ret


def get_patient_recordings():
    return pd.read_csv('features/recordings_HF.csv', index_col=0, usecols=range(9))


def get_localized_features():
    """Returns a features df of trial-meaned, location-based, PS features"""
    mean, _, _, _ = stats.intertrial_stats()
    return mean


# method hidden from API because it uses the old features csv. Use is to pick out successfully processed recordings.
def _get_old_features():
    """returns a features df for internal use, merges in a formatted date/time column for utility"""
    recordings = get_patient_recordings()
    features = pd.read_csv('features/audio_features_HF.csv', index_col=0, usecols=range(13))
    dates = recordings['Date of Recordings']
    return features.merge(pd.DataFrame(dates), left_index=True, right_index=True)


"""Represent patient fluid flow as time series for review"""
if __name__ == '__main__':

    # HF007 omitted from full index because of multiple admission problem (09/03/18)
    pat_full_idx = get_pat_idx()
    features = _get_old_features()
    recordings = get_patient_recordings()

    for pat in pat_full_idx:
        visit_days = get_visit_days(pat)
        y_vals = []
        for record in _extract_record_names(features, pat):
            y_vals.append(get_fluid_day(record))
        plt.plot(visit_days, y_vals)
        plt.scatter(visit_days, y_vals, marker='.')

    plt.title('Fluid Excess Over Time by Patient')
    plt.xlabel('Days Since First Recording')
    plt.ylabel('Fluid Up (mL)')
    plt.legend(pat_full_idx)
    # save results
    # plt.savefig('HF_results/figures/fluid_loss.png', format='png')
    # plt.close()

    # show results
    plt.show()