import sys
sys.path.append('./features')
import metadata_HF

study = 'HF'
metadata_path = 'features/metadata_' + study + '.csv'
metadata_features_path = 'features/metadata_features_' + study + '.csv'

metadata_HF.process_metadata(metadata_path, metadata_features_path)
