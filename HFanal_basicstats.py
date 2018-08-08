import pandas as pd
import numpy as np

def _extract_record_names(df, pat):
    """extract and return a list of the dated record IDs for a patient ID"""
    records = pd.Series(df.index.tolist())
    expr = r'({}.*)'.format(pat)
    return records.str.extractall(expr)[0].tolist()

# import data as dataframe
audio_features_path = 'features/audio_features_HF.csv'
audio_features = pd.read_csv(audio_features_path, index_col=0, usecols=range(13))

# generate inter-patient statistics
mfcc_means = audio_features.mean()
mfcc_vars = audio_features.var()
mfcc_meds = audio_features.median()
mfcc_stds = audio_features.std()
crosspatient_stats = pd.concat([mfcc_means, mfcc_meds, mfcc_vars, mfcc_stds], axis=1)
crosspatient_stats.rename(columns={0: 'mean', 1: 'med', 2: 'var', 3: 'std'}, inplace=True)

# generate intra-patient stats
pat_full_idx = ['HF001', 'HF002', 'HF003', 'HF004', 'HF005', 'HF006', 'HF007', 'HF008', 'HF009',
                'HF010', 'HF011', 'HF012', 'HF013', 'HF015', 'HF016', 'HF017', 'HF018', ]
pat_interest_idx = ['HF001', 'HF009', 'HF018']
frame_index = ['mfcc0', 'mfcc1', 'mfcc2', 'mfcc3', 'mfcc4', 'mfcc5', 'mfcc6', 'mfcc7', 'mfcc8',
               'mfcc9', 'mfcc10', 'mfcc11']

multi = pd.MultiIndex.from_product([pat_full_idx, frame_index], names=('patient ID', 'mfcc'))
intrapatient_stats = pd.DataFrame(columns=['mean', 'med', 'var', 'std'], index=multi)
for pat in pat_full_idx:
    record_ids = _extract_record_names(audio_features, pat)
    intrapatient_stats['mean'][pat] = audio_features.loc[record_ids].mean()
    intrapatient_stats['med'][pat] = audio_features.loc[record_ids].var()
    intrapatient_stats['var'][pat] = audio_features.loc[record_ids].median()
    intrapatient_stats['std'][pat] = audio_features.loc[record_ids].std()


# save results
crosspatient_stats.to_csv('HF_results/inter_patient_stats.csv')
intrapatient_stats.to_csv('HF_results/intra_patient_stats.csv')

# # print results
# print crosspatient_stats
# print intrapatient_stats
