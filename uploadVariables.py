import sys, argparse, os, re, requests, json
from requests.auth import HTTPBasicAuth
from urllib.error import HTTPError

#parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('-i','--inputFolder', help='Custom input folder')
parser.add_argument('-t','--tenantAlias', help='The tenant alias to use', required=True)
parser.add_argument('-a','--apiKey', help='the API key for the tenant', required=True)
parser.add_argument('-l','--locales', help='locales to upload variables for',nargs='+')
args = parser.parse_args()

inputLocales = []

if args.apiKey: apiKey = args.apiKey
if args.tenantAlias: tenantAlias = args.tenantAlias
if args.locales: inputLocales = args.locales
if args.inputFolder: rootdir = args.inputFolder
else:
    rootdir = '.'

# fullLocale = re.compile(r"[a-z-A-Z]")
dashLocale = re.compile(r"[a-z]{2}-[A-Z]{2}")
underscoreLocale = re.compile(r"[a-z]{2}_[A-Z]{2}")
lowercaseDashLocale = re.compile(r"[a-z]{2}-[a-z]{2}")
lowercaseUnderscoreLocale = re.compile(r"[a-z]{2}_[a-z]{2}")
partLocale = re.compile(r"[a-z]{2}")
cleanDir = re.compile(r"[./]")

def sendVariables(locale,translations):
    url = 'https://app.referralsaasquatch.com/api/v1/'+ tenantAlias +'/theme/'+ locale +'/variables/instance'

    headers = {'Content-Type' : 'application/json'}

    response = requests.put(url, auth=('', apiKey), data=json.dumps(translations), headers = headers)

    return response
    
def getTranslations(fname, locale):
    try:
        # open the file
        with open(fname) as openFile:
            
            # load the translations in from the file
            translations = json.load(openFile)
            
            # print(translations)
            
            try:
                # send the translations to the SaaSquatch using the locale `locale`
                print("Sending variables for locale: {}".format(locale))
                response = sendVariables(locale,translations)
                response.raise_for_status()
            
            except HTTPError as e:
                print("Unable to send variables: {}".format(e))
                
    except IOError:
        print("Could not read file:", fname)

def main():
    
    fnames = []

    #loop through each folder in the given folder
    for root,d_names,f_names in os.walk(rootdir):    
        
        
        # loop through all files in all the folders in the directory (and subdirectories) `rootdir`
        for f in f_names:
            fnames.append(os.path.join(root, f))
            
            # build the complete file name with path, relitive to the top level directory
            fname = os.path.join(root, f)

            # print("fname = {}".format(fname))
            
            # pull out the name of the locale from the translation files parent directory
            dirname = fname.split('/')
            dirname = dirname[-2]
            
            # print("dirname: {} - filename: {}".format(dirname, fname))
            
            # if fname.endswith("source.json"):
            #     print("this is a folder with translations")
            # else: print("no translations found in folder")

            locale = None
            
            # if the folder name/locale format is `en-US`, then convert it to `en_US` 
            if dashLocale.match(dirname): 
                
                locale = dirname.replace("-", "_")
            
            # if the locale format is `en_US`, then leave the locale format as is
            elif underscoreLocale.match(dirname): 
                
                locale = dirname
            
            # if the locale format is `en-us`, then conver it to `en_US`
            elif lowercaseDashLocale.match(dirname): 
                
                locale = dirname.split("-")
                locale[-1] = locale[-1].upper()
                locale = locale[0] + "_" + locale[1]
            
            # if the locale format is `en_us`, then convert it to `en_US`
            elif lowercaseUnderscoreLocale.match(dirname): 
                
                locale = dirname.split("_")
                locale[-1] = locale[-1].upper()
                
                locale = locale[0] + "_" + locale[1]
            
            # if the locale format is `de`, then convert it to `de_DE`
            elif partLocale.match(dirname): 
                
                locale = dirname + "_" + dirname.upper()
                
                
            # print(locale)
            
            # if the folder name has a readable locale, and the contents of the folder includes a file called `source.json`
            if locale and fname.endswith("source.json"):
                
                # if there are locales explicitly passed in as an arguement, and this locale is on that list, or if there are no explicitly passed locales, send it to SaaSquatch
                if (len(inputLocales)>0 and locale in inputLocales) or len(inputLocales) == 0:
                    getTranslations(fname, locale)
                else:
                    print("Locale {} is not in the list of explicit locales: {}".format(inputLocales))
            # else:
            #     print("No locales found.")
            
if __name__ == '__main__':
  main()
