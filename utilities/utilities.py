#/usr/bin/python3
#~/anaconda3/bin/python

"""A collection of file handling and other utility functions"""

import csv, logging, subprocess, os, time, sys, yaml, json

def error_log(filepath=None):
    """Initiates an error log."""
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
    """Gets a config file"""
    if cfg != None:
        cfg_file = yaml.load(open(cfg, 'r', encoding='utf-8'))
        return cfg_file
    else:
        cfg_file = yaml.load(open('config.yml', 'r', encoding='utf-8'))
        return cfg_file

def login(url=None, username=None, password=None):
    """Logs into the ArchivesSpace API"""
    import requests
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

def login_db():
    """Logs into the ArchivesSpace Database without SSH."""
    #If all credentials are present in config file...
    # if config.db_host and config.db_name and config.db_port and config.db_pw and config.db_un != '':
    #     print('Connecting you to the database...')
    #     connection = pymysql.connect(host=config.db_host,
    #                              port = int(config.db_port),
    #                              user=config.db_un,
    #                              password=config.db_pw,
    #                              db=config.db_name)
    #     print('Connected!')
    #     curse = connection.cursor()
    #     return curse
    # else:
    print('One or more login credentials missing from config.py file!')
    db_name = input('Please enter the database name: ')
    db_host = input('Please enter the database host name: ')
    db_port = input('Please enter the database port: ')
    db_un = input('Please enter the database username: ')
    db_pw = input('Please enter the database password: ')
    print('Connecting you to the database...')
    connection = pymysql.connect(host=db_host,
                             port = int(db_port),
                             user=db_un,
                             password=db_pw,
                             db=db_name)
    print('Connected!')
    curse = connection.cursor()
    return curse

#Open a CSV in reader mode
def opencsv(input_csv=None):
    """Opens a CSV in reader mode."""
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
    """Opens a CSV in DictReader mode."""
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
    """Opens a CSV in write mode."""
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
    """Opens a CSV in DictWriter mode."""
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
    """Used in ArchivesSpace API functions. Gets the update status of
    records - if update was successful adds to a counter, if not
    writes an error message to a log.

    TODO: Wrapper function"""
    if 'status' in rec_update:
        count_num += 1
        return count_num
    if 'error' in rec_update:
        logging.debug('error: could not update ' + str(rec_uri))
        logging.debug('log: ' + str(rec_update.get('error')))

def exception_protocol(rec_uri):
    """Used if an error is raised during execution of an ArchivesSpace
    function.
    
    TODO: Wrapper function."""
    print(rec_uri)
    print(traceback.format_exc())
    logging.debug(rec_uri)
    logging.exception('Error: ')

def readtxt(filepath=None):
    """Reads the lines of a text file."""
    filepath = input('Please enter path to input text file: ')
    filename = open(filepath, encoding='utf-8')
    read = filename.readlines()
    return read

def readjson(fp):
    """Loads a JSON file"""
    with open(fp) as jsonfile:
        data = json.load(jsonfile)
        return data

#check if the directory exists. If not, make dir
def setdirectory(dirpath=None):
    """Sets a directory. If directory doesn't exist, creates
    a directory."""
    if dirpath is None:
        directory = input('Please enter path to output directory: ')
    if os.path.isdir(directory):
        pass
    else:
        os.mkdir(directory)
    return directory

#add default args here
def openoutfile(filepath=None):
    """Opens a file in write mode."""
    filepath = open(filepath.strip(), 'a', encoding='utf-8')
    return filepath

def openinfile(filepath=None):
    """Opens a file in read mode."""
    filename = open(filepath.strip(), 'r', encoding='utf-8')
    return filename

def download_backups(rec_json, rec_uri, directory_path):
    """Download JSON backups of ArchivesSpace records before
    modifying them. Used in ArchivesSpace functions."""
    if 'error' in rec_json:
        logging.debug('error: could not retrieve ' + str(rec_uri))
        logging.debug(str(rec_json.get('error')))
    outfile = openjson(directory_path, rec_uri[1:].replace('/','_'))
    json.dump(rec_json, outfile)

def keeptime(start):
    """Calculates how long a function takes to run. Have to initiate
    the start time at the beginning of the function its used in.

    TODO: Wrapper function"""
    elapsedtime = time.time() - start
    m, s = divmod(elapsedtime, 60)
    h, m = divmod(m, 60)
    logging.debug('Total time elapsed: ' + '%d:%02d:%02d' % (h, m, s) + '\n')

def open_outfile(filepath):
    """Opens a file in a new window."""
    if sys.platform == "win32":
        os.startfile(filepath)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, filepath])

#REFACTOR
def copyfiles():
    """Copies files from one directory to another.

    Needs refactoring."""
    olddirectory = input('List the directory path to the files you want to copy: ')
    #make sure to include full path, i.e. C:\Users\username\Desktop\outputfolder
    newdirectory = input('List the output directory path: ')
    #include only the filename and extension (it already knows the directory); include comma and space between each file name
    files_to_copy = input('List the files you want to copy, including extension (i.e. file01.txt, file02.xml, etc.): ')
    #creates a list of filenames to compare to input directory
    files_list = list(map(str,files_to_copy.split(',')))
    new_files_list = [x.strip(' ') for x in files_list]
    #pulls input directory list
    directorylist = os.listdir(olddirectory)
    #readies the log file
    log = newdirectory + 'log.txt'
    logfile = open(log, 'w')
    #loops through input file list and copies matching files to new directory, or logs an error
    for i in new_files_list:
            if i in directorylist:
                    shutil.copy(olddirectory + '\\' + i, newdirectory)
                    print('Success! ' + i + ' has been moved to the new directory')
                    logfile.write(i + ' has been moved to the new directory' + '\n')
            else:
                    print('Error! ' + i + ' not found in directory')
                    logfile.write(i + ' not found in directory' + '\n')
    #closes log file
    logfile.close()
    #Done!
    print('Done! Check log file in output directory for details')

#reads a CSV and finds any rows that are in one CSV but not the other
def find_diffs():
    """Finds differences between two CSV files."""
    #csv with fewer lines - the "old" file
    csv_one = opencsv()
    #csv with more lines - the "new" file
    csv_two = opencsv()
    with open(csv_one, 'r', encoding='utf-8') as c1, open(csv_two, 'r', encoding='utf-8') as c2:
        file_one = c1.readlines()
        file_two = c2.readlines()
    #try modifying this so it only acts on one column...
    with open('/Users/aliciadetelich/Desktop/clustermatches.csv', 'w', encoding='utf-8') as outfile1, open('/Users/aliciadetelich/Desktop/clusterdiffs.csv', 'w', encoding='utf-8') as outfile2:
        for line in file_two:
    #        print(line)
            if line in file_one:
                outfile1.write(line)
            elif line not in file_one:
                outfile2.write(line)
    print('All Done! Check outfiles for results.')

def find_dupes():
    """Finds duplicate rows in two CSV files"""
    csv_in = opencsv()
    with open(csv_in, 'r', encoding='utf-8') as c:
        notes = c.readlines()
    with open('/Users/amd243/Desktop/dupes.csv', 'w', encoding='utf-8') as outfile:
        seen = set()
        for n in notes:
            if n in seen:
                print("duplicate: " + n)
                #outfile.write(n)
            else:
                #this actually returns anything that is NOT a duplicate...
                seen.add(n)
                outfile.write(n)
    print('All Done! Check outfile for results.')

#Takes 2 CSVs as input. Finds any columns that have changed in the 2nd CSV and adds those to a third CSV
#CSVs must have the same number of lines. Ideal for comparing two spreadsheets where only one
#column value has changed. Abstract so column numbers are arguments
def compare_columns(csv_one, csv_two, csvoutfile):
    """Takes 2 CSVs as input. Finds any columns that have changed in the 2nd CSV
    and adds those to a third CSV. CSVs must have the same number of lines.
    Ideal for comparing two spreadsheets where only one column value has changed."""
#    csv_one = opencsv()
#    csv_two = opencsv()
#    csvoutfile = opencsvsout()
    csv_one = sorted(csv_one, key=operator.itemgetter(6), reverse=True)
    csv_two = sorted(csv_two, key=operator.itemgetter(6), reverse=True)
    diff_rows = (row2 for row1, row2 in zip(csv_one, csv_two) if row1[2] != row2[2])
    csvoutfile.writerows(diff_rows)

# def compare_csvs():
#     """DO NOT USE"""
#     csv_one = opencsv()
#     csv_two = opencsv()
#     uri_list = []
#     for row in csv_one:
#         uri_list.append(row[0])
#     for row in csv_two:
#         uri = row[0]
#         ao_title = row[3]
#         extent_id = row[7]
#         if uri in uri_list:
#             for r in csv_one:
#                 uri_2 = r[0]
#                 ao_title_2 = r[4]
#                 extent_id = r[8]
#                 if uri_2 == uri:
#                     print(uri_2 + ' ' + uri)
#                     if ao_title != ao_title_2:
#                         print('AO Error! ' + uri)
#                     else:
#                         print(ao_title + ' ' + ao_title_2)
#                     if extent_id != extent_id_2:
#                         print('Extent Error! ' + uri)

def find_dupes_sorted():
    """Sorts a CSV file and then finds any duplicates in the first row."""
    csvin = opencsv()
    csvout1 = opencsvout()
    csvout2 = opencsvout()
    #csvin = sorted(csvin, key=operator.itemgetter(0), reverse=True)
    prev_row = next(csvin)
    print(prev_row)
    for row in csvin:
        print(row)
        print(prev_row)
        uri = row[0]
        extent_id = row[7]
        if uri == prev_row[0]:
            csvout1.writerow(prev_row)
            if extent_id == prev_row[7]:
                pass
            else:
                csvout1.writerow(row)
            prev_row = row
        else:
            csvout2.writerow(prev_row)
            prev_row = row

def compare_directories():
    """Compares two directories and returns a list of common files."""
    dirpath_1 = setdirectory()
    dirpath_2 = setdirectory()
    compare = filecmp.dircmp(dirpath_1, dirpath_2)
    l_only = compare.left_only
    r_only = compare.right_only
    common = compare.common_files
    return [common, l_only, r_only], dirpath_1, dirpath_2

#Compares columns for all common CSVs in 2 directories.
def compare_all_csvs():
    """Compares columns for all common CSVs in 2 directories."""
    data = compare_directories()
    outputdir = setdirectory()
    common_files = data[0][0]
    flist1 = os.listdir(data[1])
    flist2 = os.listdir(data[2])
    for file in common_files:
        csv_1 = opencsvs(data[1], file)
        csv_2 = opencsvs(data[2], file)
        #abstract headers...
        outfile = opencsvsout(outputdir, file, 'r_ps', 'r_title', 'ao_ps', 'ead_id', 'ao_title', 'ao_level', 'ao_uri', 'r_id', 'nltk')
        compare_columns(csv_1, csv_2, outfile)
    print('All Done!')


def match_columns(*headers):
    """Stores the first column of a CSV in a list. Loops through a second CSV
    and tries to match the first column with the list from the first CSV.
    If it matches it writes the data from the second CSV a 3rd CSV."""
    #uris to match
    items_to_match = opencsv()
    match_against = opencsv()
#     fob_1, output_csv = opencsvout()
#     output_csv.writerow(headers)
    fob_2, output_csv2 = opencsvout()
    output_csv2.writerow(headers)
    #read in the problem URIs, store in a list
    item_list = [row for row in items_to_match]
    for row in match_against:
        if row in item_list:
            pass
        else:
            output_csv2.writerow(row)
#
#
#         if row[0] not in item_list:
#
# #         if row[0] not in item_list:
# #             print(row[0])
# #             output_csv.writerow(row)
#         for item in item_list:
#             if row[0] == item[0]:
#                 if row[1] == item[1]:
#                     output_csv2.writerow(row)
    fob_2.close()

#Need to match eadids, series, boxes, and folders
# def match():
#     """DO NOT USE"""
#     #this refers to the CSV with all archival objects, correct?
#     problem_csv = opencsv()
#     #this refers to Kevin's CSV?
#     og_csv = opencsv()
#     output_csv = opencsvout()
#     #output_csv.writerow(headers)
#     data = []
#     #Puts all data into a list
#     for row in problem_csv:
#         data.append(row)
#     #Loops through each row of Kevin's CSV. Is there a better way to formulate these ifs?
#     for row in og_csv:
#         for item in data:
#             #matches the EAD IDs
#             if item[1] == row[2]:
#                 #Matches the series
#                 if item[5] == row[4].upper():
#                     #Matches the box number
#                     if item[6] == row[5]:
#                         #Matches the folder number
#                         if item[7] == row[6]:
#                             for i in item:
#                                 row.append(i)
#         output_csv.writerow(row)

def get_ranges():
    """Loops through a CSV file and writes any rows which have a column
    that includes '-' to a new CSV file."""
    csvfile = opencsv()
    csvoutfile = opencsvout()
    for row in csvfile:
        folders = row[8]
        if '-' in folders:
            csvoutfile.writerow(row)
        else:
            continue

def range_breakout():
    """Breaks out number ranges in a CSV file."""
    csvfile = opencsv()
    csvoutfile = opencsvout()
    for row in csvfile:
        ranges = row[8]
        try:
            split_ranges = ranges.split('-')
            low_range = int(split_ranges[0])
            high_range = int(split_ranges[1])
            all_ranges = list(range(low_range, high_range + 1))
            for i in all_ranges:
                newrow = []
                for item in row:
                    newrow.append(item)
                newrow.append(i)
                csvoutfile.writerow(newrow)
        except:
            row.append(row[8])
            print(ranges + ' is not a range')
            csvoutfile.writerow(row)

#@opencsv - have to write this still
def check_urls(r):
    """Checks response code of a list of URLs."""
    csvfile = opencsv()
    csvoutfile = opencsvout()
    for row in csvfile:
        url = row[int(r)]
        check_url = requests.get(url)
        row.append(check_url.status_code)
        csvoutfile.writerow(row)
