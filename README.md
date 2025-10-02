# Shazam Dupe using Microservices

This project contains an microservices implementation of a Shazam-style service for song recognition

The files contain:
* 

## Running the Microservices
Start each Flask app at different terminal windows with commands:
- `python audd.py`
- `python shamzam_admin.py`
- `python shamzam_user.py`

Note: `audd.py` requires an environment variable `KEY` to be set and exported at the command line, being the API key for the AudD.io API

## Running the tests
Run the test suite with command:
- `python -m unittest tests.py`

## File Structure
The test suite requires the following file structure:
- All songs in folder named `wavs` in the same base directory as the python code e.g. "./wavs/"
- Note: these songs have not been uploaded for copyright reasons

Requirements:
- requests
- flask
- unittest
- sqlite3


I completed this project whilst undertaking the ECM3408 module at the University of Exeter

Grade: 80/100
