import sqlite3
import argparse

def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('db_name', type=str, help='Database file name')
    parser.add_argument('table_name', type=str, help='Table name in database')
    parser.add_argument('-t', '--time', default=-1, type=int, help='Show orders for transfer time greater than this many seconds')
    args = parser.parse_args()
    return args

def read_from_db():
    args = arg_parser()
    conn = sqlite3.connect(args.db_name)
    c = conn.cursor()
    c.execute("select * from {} where time >= {} order by time desc".format(args.table_name, args.time))
    data = c.fetchall()
    for date, mops, time in data:
        print date, mops, time
    return

read_from_db()
