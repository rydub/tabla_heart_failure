import pandas as pd


def _extract_record_names(df, pat):
    """extract and return a list of the dated record IDs for a patient ID"""
    records = pd.Series(df.index.tolist())
    expr = r'({}.*)'.format(pat)
    return records.str.extractall(expr)[0].tolist()


# import to pandas dataframes
audio_features = pd.read_csv('features/audio_features_HF.csv', index_col=0, usecols=range(13))
expanded_features = pd.read_csv('features/audio_features_expanded_HF.csv')

# extract 5 levels of labelling for multi-index and apply
indices = expanded_features.columns.tolist()[:5]
expanded_features.set_index(indices, inplace=True)

exp_ps_features = expanded_features.sort_index().xs('PS', level=2)

# useful indices
pat_full_idx = ['HF001', 'HF002', 'HF003', 'HF004', 'HF005', 'HF006', 'HF007', 'HF008', 'HF009',
                'HF010', 'HF011', 'HF012', 'HF013', 'HF015', 'HF016', 'HF017', 'HF018', ]
pat_interest_idx = ['HF001', 'HF009', 'HF018']
frame_index = ['mfcc00', 'mfcc01', 'mfcc02', 'mfcc03', 'mfcc04', 'mfcc05', 'mfcc06', 'mfcc07', 'mfcc08',
               'mfcc09', 'mfcc10', 'mfcc11']


"""generate inter-patient statistics"""
mfcc_means = audio_features.mean()
mfcc_vars = audio_features.var()
mfcc_meds = audio_features.median()
mfcc_stds = audio_features.std()
crosspatient_stats = pd.concat([mfcc_means, mfcc_meds, mfcc_vars, mfcc_stds], axis=1).T
column_dict = dict(zip(audio_features.columns.tolist(), frame_index))
crosspatient_stats.rename(index={0: 'mean', 1: 'med', 2: 'var', 3: 'std'}, columns=column_dict, inplace=True)


"""general intra-patient stats"""
intra_idx = pd.MultiIndex.from_product([pat_full_idx, frame_index], names=('patient ID', 'mfcc'))
intrapatient_stats = pd.DataFrame(columns=['mean', 'med', 'var', 'std'], index=intra_idx)
for pat in pat_full_idx:
    record_ids = _extract_record_names(audio_features, pat)
    intrapatient_stats['mean'][pat] = audio_features.loc[record_ids].mean()
    intrapatient_stats['med'][pat] = audio_features.loc[record_ids].var()
    intrapatient_stats['var'][pat] = audio_features.loc[record_ids].median()
    intrapatient_stats['std'][pat] = audio_features.loc[record_ids].std()


"""stats from the new expanded feature set"""


"""inter-trial stats"""
names = exp_ps_features.index.names
trial_means = exp_ps_features.mean(level=names[:-1])
trial_var = exp_ps_features.var(level=names[:-1])
trial_med = exp_ps_features.median(level=names[:-1])
trial_std = exp_ps_features.std(level=names[:-1])


"""trial-meaned intra-patient stats by locality"""
reordered = trial_means.reorder_levels(['patient_id', 'localization', 'date'])
loc_mean = reordered.mean(level=['patient_id', 'localization'])
loc_var = reordered.var(level=['patient_id', 'localization'])
loc_med = reordered.median(level=['patient_id', 'localization'])
loc_std = reordered.std(level=['patient_id', 'localization'])


""""""


"""print or save results"""
crosspatient_stats.to_csv('HF_results/inter_patient_stats.csv')
intrapatient_stats.to_csv('HF_results/intra_patient_stats.csv')

# print crosspatient_stats
# print intrapatient_stats
