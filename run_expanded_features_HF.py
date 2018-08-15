import sys
import os
import pandas as pd
import re
sys.path.append('./features')
import numpy as np
import metadata_HF as metadata
sys.path.append('../essentia/src/python/essentia')
import essentia.standard as ess

# constants for DSP
M = 1024
N = 1024
H = 512
fs = 4000

# required for file reading in the specified study
study = 'HF'
subdirectory = 'heart_failure'
in_root = 'processed_data'

# paths for file writing and metadata
audio_features_path = 'features/audio_features_expanded_' + study + '.csv'
metadata_path = 'features/metadata_' + study + '.csv'
metadata_features_path = 'features/metadata_features_' + study + '.csv'

# Use this to exempt patient_ids that have bad data
bad_patient_ids = []


def _get_mfccs(audio_file):
    """Uses essentia lib functions to return MFCCs for a recording"""
    spectrum = ess.Spectrum(size=N)
    window = ess.Windowing(size=M, type='hann')
    mfcc = ess.MFCC(numberCoefficients=12)
    x = ess.MonoLoader(filename=audio_file, sampleRate=fs)()
    mfccs = []

    for frame in ess.FrameGenerator(x, frameSize=M, hopSize=H, startFromZero=True):
        mX = spectrum(window(frame))
        mfcc_bands, mfcc_coeffs = mfcc(mX)
        mfccs.append(mfcc_coeffs)

    return np.mean(np.array(mfccs), axis=0)


def _get_centroid(audio_file):
    """Uses essentia lib functions to return the spectral centroid for a recording"""
    spectrum = ess.Spectrum(size=N)
    window = ess.Windowing(size=M, type='hann')
    centroid = ess.Centroid(range=1)
    x = ess.MonoLoader(filename=audio_file, sampleRate=fs)()
    spectrumcentroid = []

    for frame in ess.FrameGenerator(x, frameSize=M, hopSize=H, startFromZero=True):
        mX = spectrum(window(frame))
        centroidvalues = centroid(mX)
        spectrumcentroid.append(centroidvalues)

    return np.mean(np.array(spectrumcentroid))


def _create_dataframe():
    """returns multi-index dataframe with all features, indexed by [patient_id, date, test_type, localization, trial]"""
    columns = ['patient_id', 'date', 'test_type', 'localization', 'trial']
    columns.extend(['mfcc_00', 'mfcc_01', 'mfcc_02', 'mfcc_03', 'mfcc_04', 'mfcc_05',
                    'mfcc_06', 'mfcc_07', 'mfcc_08', 'mfcc_09', 'mfcc_10', 'mfcc_11', 'centroid'])

    output = np.array(columns)
    patient_dirs = '{}/{}'.format(in_root, subdirectory)

    # traverse depth-first and extract features from each file extracting values for index columns in process
    for pat in os.listdir(patient_dirs):
        row0 = np.array([pat])
        record_dirs = '{}/{}'.format(patient_dirs, pat)
        for rec in os.listdir(record_dirs):
            pat = re.compile(r'_(\d*)')
            match = pat.search(rec)
            row1 = np.append(row0, match.group(1))
            test_type_dirs = '{}/{}'.format(record_dirs, rec)
            for test_type in os.listdir(test_type_dirs):
                row2 = np.append(row1, test_type)
                file_dirs = '{}/{}'.format(test_type_dirs, test_type)
                for wav in os.listdir(file_dirs):
                    pat = re.compile(r'([A-Z]*)_([A-Z]*)_(\d)')
                    match = pat.search(wav)
                    row3 = np.append(row2, np.array([match.group(2), match.group(3)]))
                    row3 = np.append(row3, _get_mfccs('{}/{}'.format(file_dirs, wav)))
                    row3 = np.append(row3, _get_centroid('{}/{}'.format(file_dirs, wav)))
                    output = np.vstack((output, row3))

    df = pd.DataFrame(output)
    return df

# create dataframe and save to file
df = _create_dataframe()
df.to_csv(audio_features_path, header=False, index=False)

# process metadata
metadata.process_metadata(metadata_path, metadata_features_path)
