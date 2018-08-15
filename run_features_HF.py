import sys
import os
import pandas as pd
from sklearn import preprocessing
sys.path.append('./features')
import mfcc
import centroid
import metadata_HF as metadata
# sys.path.append('./essentia/src/python/essentia')

# contains all subdirectories required for parsing
study = 'HF'
subdirectory = 'heart_failure'

in_root = 'processed_data'
audio_features_path = 'features/audio_features_' + study + '.csv'
metadata_path = 'features/metadata_' + study + '.csv'
metadata_features_path = 'features/metadata_features_' + study + '.csv'
full_features_path = 'features/features_' + study + '.csv'
normalized_features_path = 'features/normalized_features_' + study + '.csv'

# Use this to exempt patient_ids that have bad data
bad_patient_ids = []

def write_features(file, patient_id, patient_dir, create_header):
    """Calculates features (MFCCs, centroid) for a patient recording, writes to file (.csv)"""
    headers = ['id']
    features = [patient_id]

    mfcc_headers, mfcc_features = mfcc.get_features(patient_dir)
    headers = headers + mfcc_headers
    features = features + mfcc_features

    centroid_headers, centroid_features = centroid.get_features(patient_dir)
    headers = headers + centroid_headers
    features = features + centroid_features

    if create_header:
        file.write(','.join(headers) + ',\r')
    file.write(','.join(map(str, features)) + ',\r')


def get_patient_ids(path, study):
    """Returns a list of all ID's contained in the specified directory"""
    patient_ids = [file for file in os.listdir(path) if file.startswith(study)]
    patient_ids = [patient_id for patient_id in patient_ids if patient_id not in bad_patient_ids]
    patient_ids.sort()
    return patient_ids


file = open(audio_features_path, "w")
create_header=True

# Iterate over recordings and write features to file
for patient_id in get_patient_ids('{}/{}'.format(in_root, subdirectory), study):
    records = '{}/{}/{}'.format(in_root, subdirectory, patient_id)
    for record in [_ for _ in os.listdir(records)]:
        write_features(file, record, '{}/{}'.format(records, record), create_header)
        if create_header:
            create_header=False

file.close()

# Process metadata
metadata.process_metadata(metadata_path, metadata_features_path)
