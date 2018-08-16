# Tabla

## Setup
The following assumes you have the pip package manager and your python PATH variable points to python2.7: 
https://pypi.org/project/pip/
```
pip install -r requirements.txt
cd tools/utilFunctions_C
python compileModule.py build_ext --inplace
```

For information about essentia see:
http://essentia.upf.edu/documentation/installing.html

### Processing Audio Files:

To process raw data, place the patient directory in "raw_audio" directory. From the root of the repository run:
`python process_audio.py`

To extract features from the dataset and process patient metadata run either or both of:
`python run_features_HF.py; python run_expanded_features_HF.py`

The CSV outputs can be found in the features directory and used for analysis.

### Scraping data from the Eko website:
- Go to: https://github.com/rydub/tabla/blob/master/misc/scraping.js
- Copy contents of file
- Login to Eko and go to patient profile (the patient data you want to download)
- Open Developer Console (Chrome) or Web Console (Firefox)
- Go to the "Console" tab
- Paste the contents of the scraping file into the console and hit [ENTER]
- Type in `scrapeAudio("<patient id>")` and hit [ENTER]
- Wait for "Successs! ..." and copy output
- Open terminal and paste output into terminal and hit [ENTER]
