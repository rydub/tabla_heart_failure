import pandas as pd

# import data as dataframe
audio_features_path = 'features/audio_features_HF.csv'
audio_features = pd.read_csv(audio_features_path, index_col=0, usecols=range(13))

# create series for each stat of interest
mfcc_means = audio_features.mean()
mfcc_vars = audio_features.var()
mfcc_meds = audio_features.median()
mfcc_stds = audio_features.std()

# merge series to create dataframe
merged = pd.concat([mfcc_means, mfcc_meds, mfcc_vars, mfcc_stds], axis=1)
merged.rename(columns={0: 'mean', 1: 'med', 2: 'var', 3: 'std'}, inplace=True)

print merged
file_name = 'basicstats_HF.csv'
merged.to_csv('features/{}'.format(file_name))
