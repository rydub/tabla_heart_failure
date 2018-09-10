import matplotlib.pyplot as plt
from HFanal_utils import *
import os
# style selector for pyplot
# print(plt.style.available)
plt.style.use('seaborn-ticks')

pat_idx = get_pat_idx()
features = get_localized_features()
recordings = get_patient_recordings()

"""select patient id for plots"""
patient_id = 'HF018'

pat_features = normalize(features.loc[patient_id])
fluids = get_fluid_list(patient_id)
# swap level for location-based access, dates are sorted
pat_features = pat_features.swaplevel(0, 1)
locations = pat_features.index.levels[0].tolist()


"""plot fluid overload vs. feature for each location"""
# i = 1
# for feature in pat_features.columns.tolist():
#     fig = plt.figure(i)
#     lgd = []
#     for area in locations:
#         feature_vals = pat_features[feature].loc[area].tolist()
#         plt.plot(fluids, feature_vals)
#         lgd.append(area)
#     plt.legend(lgd)
#     plt.title('{} as a Function of Fluid Accumulation: {}'.format(feature, patient_id))
#     plt.xlabel('Fluid Overload (mL)')
#     plt.ylabel('Feature Value')
#     i += 1
#
#     # save results
#     if not os.path.exists('HF_results/figures/feature_v_fluidover/{}/'.format(patient_id)):
#         if not os.path.exists('HF_results/figures/feature_v_fluidover/'):
#             os.mkdir('HF_results/figures/feature_v_fluidover/')
#         os.mkdir('HF_results/figures/feature_v_fluidover/{}'.format(patient_id))
#     plt.savefig('HF_results/figures/feature_v_fluidover/{}/{}_{}_v_fluid.png'.format(patient_id, patient_id,  feature),
#                 format='png')
#     plt.close()
#
#
# plt.show()


"""plot fluid overload vs. location for each feature"""
i = 1
for area in locations:
    fig = plt.figure(i)
    lgd = []
    for feature in pat_features.columns.tolist()[:-1]:  # slice removes centroid
        feature_vals = pat_features.loc[area][feature].tolist()
        plt.plot(fluids, feature_vals)
        lgd.append(feature)
    plt.legend(lgd)
    plt.title('Feature value as a function of Fluid Accumulation For {} Area: {}'.format(area, patient_id))
    plt.xlabel('Fluid Overload (mL)')
    plt.ylabel('Feature Value (normalized)')
    i += 1

    # save results
    if not os.path.exists('HF_results/figures/feature_v_fluidover_byloc/{}/'.format(patient_id)):
        if not os.path.exists('HF_results/figures/feature_v_fluidover_byloc/'):
            os.mkdir('HF_results/figures/feature_v_fluidover_byloc/')
        os.mkdir('HF_results/figures/feature_v_fluidover_byloc/{}'.format(patient_id))
    plt.savefig('HF_results/figures/feature_v_fluidover_byloc/{}/{}_{}_feat_v_fluid_byloc_{}.png'.format(patient_id,
                patient_id, feature, area), format='png')
    plt.close()

# plt.show()