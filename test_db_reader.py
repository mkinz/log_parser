import unittest
import db_sd_reader
import argparse
import sqlite3
import os
from pytest import fixture
from unittest import mock


class TestDBreader:

    def get_namespace(self):
        #return argparse.Namespace(date='2020-04-15 23:30:51', ordrnum='0MKMK', db_name='test.db', table_name='test', time=99)
        return argparse.Namespace(date=None, ordrnum=None, db_name='test.db', table_name='test', time=-1)


    @fixture()  #set up for sqlite db
    def conn(self):
        return sqlite3.connect("test.db")

    @fixture()  #set up cursor for connection
    def cursor(self):
        return mock.MagicMock(spec=sqlite3.Cursor)

    def test_arg_parser(self):
        parser = argparse.ArgumentParser()
        result = db_sd_reader.arg_parser(['test.db', 'test' ], parser)
        my_namespace = self.get_namespace()
        assert my_namespace == result


    def test_read_from_db(self, cursor):
        expected_output = ["hello"]
        cursor.fetchall.return_value = expected_output
        data_from_database = db_sd_reader.read_from_db(self.get_namespace(), cursor)
        cursor.execute.assert_called_once_with("select * from test where time >= -1 order by time desc")
        cursor.fetchall.assert_called_once()

        assert expected_output == data_from_database

    def test_read_from_db_with_ordrnum(self, cursor):
        ns = self.get_namespace()
        ns.ordrnum = 25
        expected_output = [ns.ordrnum]

        cursor.fetchall.return_value = expected_output
        data_from_database = db_sd_reader.read_from_db(ns, cursor)
        cursor.execute.assert_called_once_with(f"select * from {ns.table_name} where ordrnum = '{ns.ordrnum}'")
        cursor.fetchall.assert_called_once()

        assert expected_output == data_from_database

if __name__ == '__main__':
    unittest.main()