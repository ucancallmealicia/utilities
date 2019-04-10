#/usr/bin/python3
#~/anaconda3/bin/python

'''a collection of file handling and other functions'''

import csv, logging, subprocess, os, time, sys, yaml

def error_log(filepath=None):
    if sys.platform == "win32":
        if filepath == None:
            logger = '\\Windows\\Temp\\error_log.log'
        else:
            logger = filepath
    else:
        if filepath == None:
            logger = '/tmp/error_log.log'
        else:
            logger = filepath
    logging.basicConfig(filename=logger, level=logging.DEBUG,
                        format='%(asctime)s %(levelname)s %(name)s %(message)s')
    return logger

def get_config(cfg=None):
    if cfg != None:
        cfg_file = yaml.load(open(cfg, 'r', encoding='utf-8'))
        return cfg_file
    else:
        cfg_file = yaml.load(open('config.yml', 'r', encoding='utf-8'))
        return cfg_file

def login(url=None, username=None, password=None):
    import requests, json
    try:
        if url is None and username is None and password is None:
            url = input('Please enter the ArchivesSpace API URL: ')
            username = input('Please enter your username: ')
            password = input('Please enter your password: ')
        auth = requests.post(url+'/users/'+username+'/login?password='+password).json()
        #if session object is returned then login was successful; if not it failed.
        if 'session' in auth:
            session = auth["session"]
            h = {'X-ArchivesSpace-Session':session, 'Content_Type': 'application/json'}
            print('Login successful!')
            logging.debug('Success!')
            return (url, h)
        else:
            print('Login failed! Check credentials and try again.')
            logging.debug('Login failed')
            logging.debug(auth.get('error'))
            #try again
            u, heads = login()
            return u, heads
    except:
        print('Login failed! Check credentials and try again!')
        logging.exception('Error: ')
        u, heads = login()
        return u, heads

#Open a CSV in reader mode
def opencsv(input_csv=None):
    try:
        if input_csv is None:
            input_csv = input('Please enter path to CSV: ')
        if input_csv == 'quit':
            quit()
        file = open(input_csv, 'r', encoding='utf-8')
        csvin = csv.reader(file)
        headline = next(csvin, None)
        return headline, csvin
    except:
        logging.exception('Error: ')
        logging.debug('Trying again...')
        print('CSV not found. Please try again. Enter "quit" to exit')
        h, c = opencsv()
        return h, c

#Open a CSV in dictreader mode
def opencsvdict(input_csv=None):
    try:
        if input_csv is None:
            input_csv = input('Please enter path to CSV: ')
        if input_csv == 'quit':
            quit()
        file = open(input_csv, 'r', encoding='utf-8')
        csvin = csv.DictReader(file)
        return csvin
    except:
        logging.exception('Error: ')
        logging.debug('Trying again...')
        print('CSV not found. Please try again. Enter "quit" to exit')
        c = opencsvdict()
        return c

#Open a CSV file in writer mode
def opencsvout(output_csv=None):
    try:
        if output_csv is None:
            output_csv = input('Please enter path to output CSV: ')
        if output_csv == 'quit':
            quit()
        fileob = open(output_csv, 'a', encoding='utf-8', newline='')
        csvout = csv.writer(fileob)
        logging.debug('Outfile opened: ' + output_csv)
        return (fileob, csvout)
    except Exception:
        logging.exception('Error: ')
        print('Error creating outfile. Please try again. Enter "quit" to exit')
        f, c = opencsvout()
        return (f, c)

def opencsvdictout(output_csv=None, col_names=None):
    try:
        if output_csv is None:
            output_csv = input('Please enter path to CSV: ')
        file = open(output_csv, 'a', newline='', encoding='utf-8')
        if col_names != None:
            csvin = csv.DictWriter(file, col_names)
            csvin.writeheader()
        else:
            csvin = csv.DictWriter(file)
        return csvin
    except:
        logging.exception('Error: ')
        logging.debug('Trying again...')
        print('CSV not found. Please try again.')
        c = self.opencsvdictout()
        return c

def record_status(rec_update, rec_uri, count_num):
    if 'status' in rec_update:
        count_num += 1
        return count_num
    if 'error' in rec_update:
        logging.debug('error: could not update ' + str(rec_uri))
        logging.debug('log: ' + str(rec_update.get('error')))

def opentxt():
    filepath = input('Please enter path to output text file: ')
    filename = open(filepath, 'a', encoding='utf-8')
    return filename

#check if the directory exists. If not, make dir
def setdirectory():
    directory = input('Please enter path to output directory: ')
    if os.path.isdir(directory):
        pass
    else:
        os.mkdir(directory)
    return directory

def openjson(directory, filename):
    filepath = open(directory + '/' + filename + '.json', 'a', encoding='utf-8')
    return filepath

def read_json(fp):
    with open(fp) as jsonfile:
        data = json.load(jsonfile)
        return data

def openxml(directory, filename):
    filepath = open(directory + '/' + filename.strip() + '.xml', 'w', encoding='utf-8')
    return filepath

def download_backups(rec_json, rec_uri, directory_path):
    if 'error' in rec_json:
        logging.debug('error: could not retrieve ' + str(rec_uri))
        logging.debug(str(rec_json.get('error')))
    outfile = openjson(directory_path, rec_uri[1:].replace('/','_'))
    json.dump(rec_json, outfile)

def keeptime(start):
    elapsedtime = time.time() - start
    m, s = divmod(elapsedtime, 60)
    h, m = divmod(m, 60)
    logging.debug('Total time elapsed: ' + '%d:%02d:%02d' % (h, m, s) + '\n')

def open_outfile(filepath):
    if sys.platform == "win32":
        os.startfile(filepath)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filepath])