#!/bin/python
import glob
import os
import unittestbusy_time_timetable = []

import validator


class InputValidationTest(unittest.TestCase):

    def test_correct_values(self):
        """
        Check no error for correct values
        """
        minutes = 30
        people = 2
        path = create_path("/in")

        err = validator.validate_input(path, minutes, people)
        self.assertEqual(err, None)

    def test_minutes_negative_value(self):
        """
        Check error for negative minutes value
        """
        minutes = -1
        people = 2
        path = create_path("/in")

        err = validator.validate_input(path, minutes, people)
        self.assertNotEqual(err, None)

    def test_people_negative_value(self):
        """
        Check error for negative people values
        """
        minutes = 30
        people = -2
        path = create_path("/in")

        err = validator.validate_input(path, minutes, people)
        self.assertNotEqual(err, None)

    def test_path_does_not_exist(self):
        """
        Check error for not existing path
        """
        minutes = 30
        people = 2
        path = create_path("/does_not_exist")

        err = validator.validate_input(path, minutes, people)
        self.assertNotEqual(err, None)

    def test_files_found_in_directory(self):
        """
        Check error if no .txt files exist in directory
        """
        minutes = 30
        people = 2
        path = create_path("/in")

        # count number of files
        num_of_files = len(glob.glob(path + "/*.txt"))

        err = validator.validate_input(path, minutes, people)
        if num_of_files > 0:
            self.assertEqual(err, None)
        else:
            self.assertNotEqual(err, None)

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
