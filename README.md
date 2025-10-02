# Shazam Dupe using Microservices

This project contains an microservices implementation of a Shazam-style service for song recognition

The files contain:
* `audd.py` - a microservice endpoint for calling an external song recognition API
* `database.py` - wrapper for the database
* `repository.py` - song database schema definition
* `shamzam_admin.py` - the admin microservice endpoints for the app, to add and remove from the database
* `shamzam_user.py` - the user microservice endpoints for the app, to query the microservice
* `tests.py` - a series of unit tests (technically end-to-end tests) for the collection of microservices
* `utils.py` - utility functions
* `./Docs/`
  > * `Designs.pdf` - the design document for the endpoints
  > * `GenAI_Statement.pdf` - a statement about the usage of GenAI

## Running the Microservices
Start each Flask app at different terminal windows with commands:
- `python audd.py`
- `python shamzam_admin.py`
- `python shamzam_user.py`

Note: `audd.py` requires an environment variable `KEY` to be set and exported at the command line, being the API key for the [AudD.io API](https://audd.io)

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
