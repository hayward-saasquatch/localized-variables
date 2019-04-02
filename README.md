# localized-variables

Processing localized SaaSquatch program variables

## Uploading Variables

Script for uploading localized variables from crowdin into SaaSquatch

### Usage
1. From the Settings page in the crowdin project, `Build & Download` the latest versions of the translations
2. Extract the translations ZIP file
3. Confirm that each locale's folder name include the required language and country information needed to upload it to SaaSquatch
4. Run the script. The extracted translations folder either needs to be in the same place as the script, or the `inputFolder` arguement needs to be included

`python3 uploadVariables.py -t test_alu125hh1si9w -a TEST_BHASKh5125Las5hL125oh3VbLmPxUSs -l cs_CZ de_CH de_DE dk_DK -i /folder/`
  
#### Options:
- `-t`,`--tenantAlias`: The tenant alias to use. Required.
- `-a`,`--apiKey`: The API key for the tenant. Required.
- `-l`,`--locales`: The locales to upload variables for. Optional. If this option is not included, all translations that are found will be pushed to SaaSquatch
- `-i`,`--inputFolder`: A custom input folder. Default is `.`

### Setup
The following steps outline how to setup a linux system to run this script (based on the information outlined in [this](https://docs.python-guide.org/dev/virtualenvs/#lower-level-virtualenv) guide)

1. Install Python 3.6+. For debian-based systems: `sudo apt-get install python3.6`
2. Install virtualenv to create an isolated python environment to run this script in `pip install virtualenv`
3. From the top level of the project folder, create a new virtual environment `virtualenv -p /usr/bin/python3.6 venv`. This example assumes the version of python you install was 3.6, so please plug in the version of python you used in step 1.
4. Activate your new virutal environment: `source venv/bin/activate`
5. Install the python packages you will need to run this script `pip install -r requirements.txt`

Once you are done working in the virtual environment (otherwise it will use this virtualenv for running python elsewhere in your system), you can deactivate for the time being using the command `deactivate`