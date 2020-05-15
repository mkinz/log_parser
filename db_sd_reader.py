import sqlite3
import argparse
import sys


def arg_parser(args, parser):
    parser.add_argument('db_name', type=str, help='Database file name')
    parser.add_argument('table_name', type=str, help='Table name in database')
    parser.add_argument('-t', '--time', default=-1, type=int,
                        help='Show orders for transfer time greater than this many seconds')
    parser.add_argument('-o', '--ordrnum', type=str, help='Optional ordrnum')
    parser.add_argument('-d', '--date', type=str, help='Optional date')

    return parser.parse_args(args)


def connect_to_db(args):
    conn = sqlite3.connect(args.db_name)
    return conn


def get_cursor(conn):
    c = conn.cursor()
    return c


def read_from_db(args, cursor):
    # sql select if ordrnum is given
    if args.ordrnum:
        cursor.execute("select * from {} where ordrnum = '{}'".format(args.table_name, args.ordrnum))
    elif (args.date and args.time):
        cursor.execute(
            "select * from {} where date like ('%{}%') and time >= {} order by time desc".format(args.table_name,
                                                                                                 args.date, args.time))
    elif args.date:
        cursor.execute(
            "select * from {} where date like ('%{}%') order by time desc".format(args.table_name, args.date))
    # otherwise, select all
    else:
        cursor.execute("select * from {} where time >= {} order by time desc".format(args.table_name, args.time))

    # print out the data
    data = cursor.fetchall()
    return data


def main():
    # get command line arguments and feed them into the db reader func
    parser = arg_parser(args=sys.argv[1:], parser=argparse.ArgumentParser())

    connect_to_db(parser)
    get_cursor(connect_to_db(parser))

    for date, mops, time in read_from_db(parser, get_cursor(connect_to_db(parser))):
        print(date, mops, time)


if __name__ == '__main__':
    main()
