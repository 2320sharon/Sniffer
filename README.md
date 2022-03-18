# Sniffer 🐕
<img src="https://user-images.githubusercontent.com/61564689/159071698-5332b923-1e98-4082-95a1-bbf5b04ce318.gif" align="right"
     alt="Sniffer Logo" width="560" height="450">
"Sniff out the good and bad imagery in your dataset."

- A python application for sorting through imagery.
- Only sorts jpgs in the `images` directory
- Saves the sorted jpgs in two directories called `good_images` and `bad_images` within the program's directory when `File Mode` is activated
- Saves the outputs as a csv into the programs current working directory when `CSV Mode` is activated

## Running the Program :computer:

- There are two ways to run the program, from the command line or from within a jupyter notebook.

#### Jupyter Notebook Method

1. `conda activate Sniffer`
2. `cd <location where you saved Sniffer>`
3. `jupyter notebook`

#### Command Prompt Method

1. `conda activate Sniffer`
2. `cd <location where you saved Sniffer>`
3. `panel serve Sniffer.ipynb`
4. Copy the local host text into your browser of choice `http://localhost:5006/Sniffer`

## Installation Guide

1. `conda env create --file install/Sniffer.yaml`
2. `conda activate Sniffer`

## :open_mouth: Updates Coming Soon :open_mouth:

1. Hotkeys - in development
2. Hosting :globe_with_meridians:
