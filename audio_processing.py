import numpy as np
import csv
import matplotlib.pyplot as plt # naming convention for matplotlib
import json
from scipy.io import wavfile as wav
from scipy.fftpack import fft # import discrete fourier transform and its inverse
from scipy import signal
from scipy.io.wavfile import write
from pydub import AudioSegment

#Read in the file upload
#FOR EXAMPLE: Folder: Bone Transducer, fileName = BoneTransducer_T02_2
#don't include .wav for obvious reasons
#FOR EXAMPLE: Folder: Bone Transducer, fileName = BoneTransducer_T02_2
#don't include .wav for obvious reasons

# ===== M4A TO WAV ========

#fileName = "cf"
#path = "piezo/" + fileName
#
#sound = AudioSegment.from_file(path + ".m4a", format="m4a")
#file_handle = sound.export(path + ".wav", format="wav")
#
#wav_sound = AudioSegment.from_wav(path + ".wav")
#wav_sound = wav_sound.set_channels(1)
#wav_sound.export(path + ".wav", format="wav")

# ===== END M4A TO WAV ========

folder = '/home/yashasaxena/Repositories/tabla_heart_failure/\
raw_data/heart_failure/HF001/HF001_011918/PS/'
fileName = 'PS_LLL_1'
sampFreq, snd = wav.read(folder + "/" + fileName + '.wav')

folder2 = '/home/yashasaxena/Repositories/tabla_heart_failure/\
raw_data/heart_failure/HF001/HF001_012618/PS'
fileName2 = 'PS_LLL_1'
sampFreq2, snd2 = wav.read(folder2 + "/" + fileName2 + '.wav')

s = 2048

pxx, freqs, bins, _ = plt.specgram(snd, NFFT=s, Fs=sampFreq, noverlap=s/2,
                                 sides='onesided',
                                   window=signal.hann(s),
                                   scale_by_freq=True,
                                   mode='magnitude')

pxx2, freqs2, bins2, _ = plt.specgram(snd2, NFFT=s, Fs=sampFreq, noverlap=s/2,
                                 sides='onesided',
                                   window=signal.hann(s),
                                   scale_by_freq=True,
                                   mode='magnitude')

#dB calculation
y_axis = 20*np.log10(np.mean(pxx, axis=1))
y_axis2 = 20*np.log10(np.mean(pxx2, axis=1))

area_1 = np.trapz(y_axis[:50], freqs[:50])
area_2 = np.trapz(y_axis2[:50], freqs2[:50])
auc = area_2/area_1

x_h_list = freqs[:50].tolist()
y_h_list = y_axis[:50].tolist()
x_cf_list = freqs2[:50].tolist()
y_cf_list = y_axis2[:50].tolist()
to_plot = {'x_healthy' : x_h_list,
           'y_healthy' : y_h_list,
           'x_cf' : x_cf_list,
           'y_cf' : y_cf_list,
           'tr' : auc
          }
json.dumps(to_plot)

fig = plt.figure()
plt.title('Magnitude vs Frequency')
plt.plot(freqs[:50], y_axis[:50], 'g', label="12791 mL")
plt.plot(freqs2[:50], y_axis2[:50], 'b', label="2450 mL")
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.xlabel('Frequency (Hz)')
plt.ylabel('Magnitude (dB)')
plt.xlim(0,200)
plt.ylim(-20,200)
plt.show()
#fig.savefig(folder + '/' + fileName +'.png', bbox_inches='tight')
#print("Saved!")
#plt.close()