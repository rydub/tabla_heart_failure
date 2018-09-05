import matplotlib.pyplot as plt
from HFanal_utils import *
import os
# style selector for pyplot
# print(plt.style.available)
plt.style.use('seaborn-ticks')

pat_idx = get_pat_idx()
features = get_localized_features()
recordings = get_patient_recordings()


"""Select a patient id and plot fluid overload vs. feature for each location"""
patient_id = 'HF009'

pat_features = features.loc[patient_id]
# swap level for location-based access, dates are sorted
pat_features = pat_features.swaplevel(0, 1)
locations = pat_features.index.levels[0].tolist()
i = 1

fluids = get_fluid_list(patient_id)
for feature in pat_features.columns.tolist():
    fig = plt.figure(i)
    lgd = []
    for area in locations:
        feature_vals = pat_features[feature].loc[area].tolist()
        plt.plot(fluids, feature_vals)
        lgd.append(area)
    plt.legend(lgd)
    plt.title('{} as a Function of Fluid Accumulation: {}'.format(feature, patient_id))
    plt.xlabel('Fluid Overload (mL)')
    plt.ylabel('Feature Value')

# save results
#     if not os.path.exists('HF_results/figures/feature_v_fluidover/{}/'.format(patient_id)):
#         if not os.path.exists('HF_results/figures/feature_v_fluidover/'):
#             os.mkdir('HF_results/figures/feature_v_fluidover/')
#         os.mkdir('HF_results/figures/feature_v_fluidover/{}'.format(patient_id))
#     plt.savefig('HF_results/figures/feature_v_fluidover/{}/{}_{}_v_fluid.png'.format(patient_id, patient_id,  feature),
#                 format='png')
#     plt.close()
    i += 1

plt.show()
