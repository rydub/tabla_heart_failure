import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import linear_model

# style selector for pyplot
# print(plt.style.available)
plt.style.use('seaborn-ticks')

# paths for required data
metadata_path = 'features/metadata_HF.csv'
audio_features_path = 'features/audio_features_HF.csv'
recordings_path = 'features/recordings_HF.csv'

# import data as 2D np arrays, string type?
metadata = pd.read_csv(metadata_path, index_col=0)
audio_features = pd.read_csv(audio_features_path, index_col=0, usecols=range(13))
recordings = pd.read_csv(recordings_path, index_col=0)

