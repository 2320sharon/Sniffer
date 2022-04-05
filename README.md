# Sniffer 🐕


[![Python 3.6](https://img.shields.io/badge/python-3.6-blue.svg)](https://www.python.org/downloads/release/python-360/)
[![Python 3.7](https://img.shields.io/badge/python-3.7-red.svg)](https://www.python.org/downloads/release/python-370/)
<br>
![Action Badge](https://github.com/2320sharon/Sniffer/actions/workflows/sniffer-action.yml/badge.svg)

<img src="https://user-images.githubusercontent.com/61564689/161645555-2b59559a-68a8-47dc-b11c-24f4e9a244f6.gif" align="right"
     alt="Sniffer Logo" width="560" height="450">

"Sniff out the good and bad imagery in your dataset."

- A python application for sorting through imagery.
- Only sorts jpgs in the `images` directory
- Saves the sorted jpgs in two directories called `good_images` and `bad_images` within the program's directory when `File Mode` is activated
- Saves the outputs as a csv into the programs current working directory when `CSV Mode` is activated


## Running the Program :computer:

- There are two ways to run the program, from the command line or from within a jupyter notebook.

#### Jupyter Notebook Method 🪐

1. `conda activate Sniffer`
2. `cd <location where you saved Sniffer>`
3. `jupyter notebook`

#### Command Prompt Method

1. `conda activate Sniffer`
2. `cd <location where you saved Sniffer>`
3. `panel serve Sniffer.ipynb`
4. Copy the local host text into your browser of choice `http://localhost:5006/Sniffer`


## How to Use Hotkeys ⌨️
I recommend using hotkeys in the [localhost](#command-prompt-method) version of Sniffer. Sometimes jupyter notebooks will create and delete cells when you type `a` and `d`. That being said hotkeys will still work in jupyter notebook.
### Sniffer's Hotkeys
`a` = good image
</br>
`d` = bad image
<br>
`s` = undo last action

## Installation Guide 🧰

1. `conda env create --file install/Sniffer.yaml`
2. `conda activate Sniffer`

## Quick Disclaimer
Currently sniffer only works with images with the `.jpg` extension. Other file types are not supported.
####  Unsupported File Types
- :x: `.jpeg` 
- :x: `.PNG`


## :open_mouth: Updates Coming Soon :open_mouth:

1. Support for `.png`s
2. Support for `.jpeg`s
3. Hosting :globe_with_meridians:
4. A wiki full of examples and troubleshooting tips

