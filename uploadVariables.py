import sys, argparse, os, re, requests, json
from requests.auth import HTTPBasicAuth

#parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputFolder', help='Custom input folder')
parser.add_argument('-t','--tenantAlias', help='The tenant alias to use', required=True)
parser.add_argument('-a','--apiKey', help='the API key for the tenant', required=True)
parser.add_argument('-l','--locales', help='locales to upload variables for',nargs='+', required=True)
args = parser.parse_args()

inputLocales = []

if args.apiKey: apiKey = args.apiKey
if args.tenantAlias: tenantAlias = args.tenantAlias
if args.locales: inputLocales = args.locales
if args.inputFolder: rootdir = args.inputFolder
else:
    rootdir = '.'

fullLocale = re.compile(r"[a-z-A-Z]")
fullLocale2 = re.compile(r"[a-z_A-Z]")
partLocale = re.compile(r"[a-z]")
cleanDir = re.compile(r"[./]")

def sendVariables(locale,translations):
    url = 'https://app.referralsaasquatch.com/api/v1/'+ tenantAlias +'/theme/'+ locale +'/variables/instance'

    headers = {'Content-Type' : 'application/json'}

    response = requests.put(url, auth=('', apiKey), data=json.dumps(translations), headers = headers)

    return response

def formatLocale(localeFolder):

    #if the locale matches the format `en-US`
    #print(localeFolder)
    if fullLocale.search(localeFolder) is not None:

        temp = localeFolder.split('-')
        tempLocale = temp[0]+ '_' + temp[1]

        #if the folder in question is on the list of locales to be uploaded
        for locale in inputLocales:
            if tempLocale == locale:
                return tempLocale

    #if the locale matches the format `en_US`
    elif fullLocale2.search(localeFolder) is not None:

        return localeFolder

    else: print("Folder naming format failed to meet criteria")

def main():

    #loop through each folder in the given folder
    for subdir, dirs, files in os.walk(rootdir):

        for file in files:
            #print(subdir, dirs)
            #subDir = cleanDir.sub("", subdir)
            subDir = subdir[-5:]
            #print(subDir, file)

            #check that the file is a json file, and thus should be read in
            if file.endswith('.json'):
                pathToFile = subdir + '/' + file
                #print("Path to file: {}".format(pathToFile))
                with open(pathToFile) as f:
                    translations = json.load(f)

                #lookup and return which desired locales match this folder
                locale = formatLocale(subDir)

                if locale:
                    try:
                        print("Sending variables for locale: {}".format(locale))
                        response = sendVariables(locale,translations)
                        response.raise_for_status()
                    except HTTPError as e:
                        print("Unable to send variables: {}".format(e))

                else: print("Unable to match folder: {} with a locale".format(subDir))

if __name__ == '__main__':
  main()
