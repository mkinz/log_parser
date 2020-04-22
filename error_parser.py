import datetime
import os
import re
import argparse
import sys

### inputs ###
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', type=str, help='Input file to parse for data')
    args = parser.parse_args()
    return args


def check_input():
    args = parse_args()
    if not os.path.exists(args.input_file):
        print "input file doesn't exist!"
        sys.exit(0)
    pass


### regex definitions ###
def get_16_regex():
    regex = re.compile("\d{4}-\d{2}-\d{2}.*error.*-\s16.*", re.IGNORECASE)
    return regex


def get_40_regex():
    regex = re.compile("\d{4}-\d{2}-\d{2}.*error.*-\s40.*", re.IGNORECASE)
    return regex


def get_other_errors():
    regex = re.compile("\d{4}-\d{2}-\d{2}.*error.*-\s(?!40)(?!16)\d+.*", re.IGNORECASE)
    return regex


def get_success_regex():
    regex = re.compile('(\d{4}-\d{2}-\d{2}.\d{2}:\d{2}:\d{2}).*transfer complete for file: .*(.{5})/.*tar.gz.*\n.*transfer complete in (\d+) seconds.', re.IGNORECASE)
    return regex


### process data ###
def find_matches(regex):
    args = parse_args()
    found_stuff = []
    with open(args.input_file, "r") as f:
        my_data = f.read()
        for line in re.findall(regex, my_data):
            found_stuff.append(line)
    return found_stuff
       

### looping print function ###
def show_results(matches):
    for item in matches:
        print item


### main app ###
def main():

    today = datetime.date.today()
    print "Subject: Error logs for {}".format(today)
    
    # error code 16 
    error_code_16 = get_16_regex()
    match_16 = find_matches(error_code_16)
    show_results(match_16)
    print "Count of error code 16: {}\n".format(len(match_16))

    # error code 40
    error_code_40 = get_40_regex()
    match_40 = find_matches(error_code_40)
    show_results(match_40)
    print "Count of error code 40: {}\n".format(len(match_40))

    # other errors
    other_errors = get_other_errors()
    match_other_errors = find_matches(other_errors)
    show_results(match_other_errors)
    print "Count of other errors: {}\n".format(len(match_other_errors))
    
    # successful transfers
    transfer_success = get_success_regex()
    match_success = find_matches(transfer_success)
    print "Count of successful tar.gz files sent: {}\n".format(len(match_success))

    # math

    fl_16 = float(len(match_16))
    #print fl_16
    fl_40 = float(len(match_40))
    #print fl_40
    fl_16_and_40 = fl_16 + fl_40
    #print fl_16_and_40
    fl_other_errors = float(len(match_other_errors))
    #print fl_other_error
    fl_all_error = fl_16 + fl_40 + fl_other_errors
    #print fl_all_error
    fl_success = float(len(match_success))
    #print fl_success

    ec16_percent = (fl_16 / fl_success) * 100
    ec40_percent = (fl_40 / fl_success) * 100
    other_error_percent = (fl_other_errors / fl_success) * 100
    all_error_percent = (fl_all_error / fl_success) * 100
    #all_error_minus_ec_16_and_40 = ((fl_all_error - fl_16_and_40) / fl_success ) * 100
    
    print '#######################'
    print "Some useful statistics:"
    print '#######################'
    print "percent of error code 16 out of total sent: {}%".format(ec16_percent)
    print "percent of error code 40 out of total sent: {}%".format(ec40_percent)
    print "percent of other errors: {}%".format(other_error_percent)
    print "percent of ALL error out of total sent: {}%".format(all_error_percent)
    

if __name__=='__main__':
    check_input()
    main()
