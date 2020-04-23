import sqlite3
import argparse
import sys

def arg_parser(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('db_name', type=str, help='Database file name')
    parser.add_argument('table_name', type=str, help='Table name in database')
    parser.add_argument('-t', '--time', default=-1, type=int, help='Show orders for transfer time greater than this many seconds')
    parser.add_argument('-o', '--ordrnum', default=-1, type=str, help='Option to select a specific order')
    return parser.parse_args()
    

def read_from_db(args):
    conn = sqlite3.connect(args.db_name)
    c = conn.cursor()

    # sql select of ordrnum is given
    if args.ordrnum:
        c.execute("select * from {} where ordrnum = '{}'".format(args.table_name, args.ordrnum))
    # otherwise, select all
    else:
        c.execute("select * from {} where time >= {} order by time desc".format(args.table_name, args.time))
    
    data = c.fetchall()
    for date, mops, time in data:
        print date, mops, time
    return

def main():
    parser = arg_parser(sys.argv[1:])
    read_from_db(parser)

if __name__ == '__main__':
    main()