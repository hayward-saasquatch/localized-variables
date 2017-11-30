# localized-variables

Processing localized SaaSquatch program variables

## Uploading Variables

Script for uploading localized variables from crowdin into SaaSquatch

### Usage
`python3 uploadVariables.py -t test_alu125hh1si9w -a TEST_BHASKh5125Las5hL125oh3VbLmPxUSs -l cs_CZ de_CH de_DE dk_DK -i /folder/`
  
#### Options:
- `-t`,`--tenantAlias`: The tenant alias to use. Required.
- `-a`,`--apiKey`: The API key for the tenant. Required.
- `-l`,`--locales`: The locales to upload variables for. Optional.
- `-i`,`--inputFolder`: A custom input folder. Default is `.`