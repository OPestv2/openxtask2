#!/bin/python
import glob
import os
import unittest
import random

import validator


class InputValidationTest(unittest.TestCase):

    def setUp(self):
        self.minutes = 30
        self.people = 2
        self.path = create_path("/in")

    def test_correct_values(self):
        """
        Check no error for correct values
        """

        err = validator.validate_input(self.path, self.minutes, self.people)
        self.assertEqual(err, None)

    def test_minutes_negative_value(self):
        """
        Check error for negative minutes value
        """
        minutes = -1

        err = validator.validate_input(self.path, minutes, self.people)
        self.assertNotEqual(err, None)

    def test_people_negative_value(self):
        """
        Check error for negative people values
        """
        people = -2

        err = validator.validate_input(self.path, self.minutes, people)
        self.assertNotEqual(err, None)

    def test_path_does_not_exist(self):
        """
        Check error for not existing path
        """
        rand = random.randint(10000000, 99999999)
        path = create_path(f"/{rand}")

        err = validator.validate_input(path, self.minutes, self.people)
        self.assertNotEqual(err, None)

    def test_files_not_found_in_directory(self):
        """
        Check error if no .txt files exist in directory
        """
        rand = random.randint(10000000, 99999999)
        path = create_path(f"/{rand}")
        # create empty, temporary directory
        os.mkdir(path)

        err = validator.validate_input(path, self.minutes, self.people)
        self.assertNotEqual(err, None)

        # remove directory
        os.rmdir(path)

    def test_files_found_in_directory(self):
        """
        Check number of .txt files in existing directory
        """
        rand = random.randint(10000000, 99999999)
        path = create_path(f"/{rand}")
        # create empty, temporary directory
        os.mkdir(path)

        number_of_files = 3
        filenames = []

        # create files
        for i in range(number_of_files):
            filename = str(random.randint(10000000, 99999999)) + ".txt"
            while filename in filenames:
                filename = str(random.randint(10000000, 99999999)) + ".txt"
            filenames.append(filename)
            with open(os.path.normpath(path + "/" + filename), "w"):
                pass

        # check
        err = validator.validate_input(path, self.minutes, self.people)
        self.assertEqual(err, None)

        # remove files
        for filename in filenames:
            os.remove(os.path.normpath(path + "/" + filename))
        # remove directory
        os.rmdir(path)

    def test_insufficient_calendar_files_in_directory(self):
        """
        Check number of .txt files in existing directory
        """
        rand = random.randint(10000000, 99999999)
        path = create_path(f"/{rand}")
        # create empty, temporary directory
        os.mkdir(path)

        number_of_files = 3
        filenames = []

        # create files
        for i in range(number_of_files):
            filename = str(random.randint(10000000, 99999999)) + ".txt"
            while filename in filenames:
                filename = str(random.randint(10000000, 99999999)) + ".txt"
            filenames.append(filename)
            with open(os.path.normpath(path + "/" + filename), "w"):
                pass

        # check
        err = validator.validate_input(path, self.minutes, number_of_files+1)
        self.assertNotEqual(err, None)

        # remove files
        for filename in filenames:
            os.remove(os.path.normpath(path + "/" + filename))
        # remove directory
        os.rmdir(path)


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


if __name__ == "__main__":
    unittest.main()
