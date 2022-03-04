# Sniffer 🐕 
<img src="https://user-images.githubusercontent.com/61564689/156675558-6fd4f957-39f0-4c85-be30-58ebb3622a56.gif" align="right"
     alt="Lotus logo by Freepik" width="550" height="400">
"Sniff out good and bad images in your dataset"
- A python application for sorting through geospatial imagery.
- Only sorts jpgs in the `images` directory
- Saves the sorted jpgs in a directory called `sorted_images` within the program's directory

## Running the Program

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

1. `conda env create --file install/geotinder.yaml`
2. `conda activate GeoTinder`
