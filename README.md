# Retriever for eBird Checklist Observations

A python script to retrieve more complete ebird checklist datasets, including observation-id's and other details.

These scripts require:
- Downloading/Installing [python](https://www.python.org/downloads/)
- Installing required python packages listed in [requirements.txt](requirements.txt)
  - In terminal/shell, install requirements by pasting this command: `pip -m install requirements.txt`

## How to setup:

1. Request an eBird API key from https://ebird.org/api/keygen

2. Clone (or download) this repo

3. Setup your `.env` file.
  - In this repo/directory, save a copy of the [.env.example](.env.example) file as `.env` and add your API key to it.

## How to run:

In terminal, run the script with this command:  `python3 ebird_api.py [checklist ID]`
  - e.g.:  `python3 ebird_api.py S196904601`
  
