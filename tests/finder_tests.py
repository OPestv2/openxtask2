#!/bin/python
import datetime
import os
import unittest

from finder import Finder

FORMAT = "%Y-%m-%d %H:%M:%S"

class FinderTest(unittest.TestCase):

    def setUp(self):
        self.current_time = create_date("2022-07-01 09:00:00")


    def test_calendar_with_reversed_dates(self):
        """
        Check protection against incorrectly defined dates in file.
        Second date is earlier that the first one
        Such date occurs in /tests/in/reversed_dates/calendar2.txt
        """
        finder = Finder(create_path('/tests/in/reversed_dates'), 30, 2, self.current_time)
        result = finder.search()
        self.assertEqual(result.strftime(FORMAT), "2022-07-02 13:00:00")

    def test_empty_calendar(self):
        """
        Check if one free-time period is retrieved from empty file and processed
        Such empty file is /tests/in/empty_file/calendar1.txt
        """
        finder = Finder(create_path('/tests/in/empty_file'), 30, 2, self.current_time)
        result = finder.search()
        self.assertEqual(result.strftime(FORMAT), "2022-07-02 13:00:00")

    def test_multiple_calendars_for_different_number_of_people_and_minutes(self):
        """
        Check script handles multiple calendars and returns correct result
        for different number of people and minutes
        Input files are in directory /tests/in/multiple_calendars
        """
        finder = Finder(create_path('/tests/in/multiple_calendars'), 30, 5, self.current_time)
        result = finder.search()
        self.assertEqual(result.strftime(FORMAT), "2022-07-06 00:00:00")

        finder = Finder(create_path('/tests/in/multiple_calendars'), 300, 4, self.current_time)
        result = finder.search()
        self.assertEqual(result.strftime(FORMAT), "2022-07-06 00:00:00")

        finder = Finder(create_path('/tests/in/multiple_calendars'), 20, 4, self.current_time)
        result = finder.search()
        self.assertEqual(result.strftime(FORMAT), "2022-07-03 19:00:01")

    def test_current_time_with_empty_calendar(self):
        pass

def create_path(path):
    """
    Function creates absolute path using project path and directory specified by user.
    Provides leading '/' separating project path and user input, normalizes string and removes ending '/'.
    :param path: directory specified by user
    :type path: str
    :return: Normalized absolute path
    :rtype: str
    """
    if not path.startswith("/"):
        path = "/" + path
    path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + "/.." + path)
    # if script is running on system other than Windows remove '/' on the end if exists
    # on Windows os.path.normpath removes it
    if path.endswith("/"):
        path = path[:-1]
    return path

def create_date(date):
    """
    Function creates and returns datetime object set on 'date' time
    :param date: datetime string in format "yyyy-mm-dd HH:MM:SS"
    :type date: str
    :return: Function returns datetime object
    :type: datetime object
    """
    return datetime.datetime.strptime(date, FORMAT)

if __name__ == "__main__":
    unittest.main()
