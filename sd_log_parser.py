# log parser

import re
import sqlite3
import argparse
import sys
import os

# get input args
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='Input file to parse for data')
    parser.add_argument('db_name', type=str, help='Database file name')
    parser.add_argument('table_name', type=str, help='Table name in database')
    args = parser.parse_args()
    return args


# define the regex with group capture for mops order and time
def get_regex():
    regex = re.compile('(\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2}).*transfer complete for file:.*(.{5})/.*tar.gz.*\n.*transfer complete in (\d+) seconds.', re.IGNORECASE)
    return regex


# open file, find regex matches, and return list of matches
def find_matches(): 
    args = parse_args()
    found_stuff = []
    with open(args.input_file, "r") as f:
        mydata = f.read()
        my_regex = get_regex()
        for date,order,time in re.findall(my_regex, mydata):
            found_stuff.append((date, order, time))
    
    res = list(set(found_stuff)) #remove duplicates
    return res


def get_database_name():
    # check to see if database name ends with .db; if not, set it
    args = parse_args()    
    database_name = args.db_name
    if not database_name.endswith(".db"):
        database_name = args.db_name + ".db"
    return database_name


# db creation for sorting and viewing data
def create_write_db(matched_data):
    args = parse_args() 
    myDB = get_database_name()
    
    # create db, table
    conn = sqlite3.connect(myDB) 
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS {} 
            (date TEXT, ordrnum TEXT, time INTEGER )'''.format(args.table_name))

    # write to db
    for date, order, time in matched_data:
        c.execute("INSERT INTO {} (date, ordrnum, time) VALUES (?, ?, ?)".format(args.table_name),(date, order, time))

    conn.commit()
    conn.close()
    print "Successfully parsed {} and wrote {} entries to the database.\nPlease use db_sv_reader.py to read data in database.".format(args.input_file, len(matched_data))
    print "Database name: " + myDB
    print "Table name: " + args.table_name
    return



def check_input_args():
    args = parse_args()
    myDB = get_database_name() 
    # prevent a dot character from being in the table name
    if "." in args.table_name:
        print "Cannot have . in table name!"
        sys.exit(0)

    # catch if input file does not exist
    elif not os.path.exists(args.input_file):
        print "{} does not exist!".format(args.input_file)
        print "Check spelling and try again."
        sys.exit(0)

    # catch if database file already exists to prevent overwriting 
    elif os.path.exists(myDB):
        print "{} already exists. Please choose a new db name to prevent data overwriting.".format(myDB)
        sys.exit(0)
    
    else:
        pass 



def main():
    check_input_args()
    create_write_db(find_matches())


if __name__=='__main__':
    main()

