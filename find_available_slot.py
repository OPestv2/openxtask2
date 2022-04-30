#!/bin/python
import datetime
import optparse
import os
import sys

import validator
from finder import Finder

if __name__ == "__main__":
    # store option names and corresponding variable names in dict
    option_names = {"minutes": "--duration-in-minutes", "people": "--minimum-people", "path": "--calendars"}
    try:
        parser = optparse.OptionParser("python3 find_available_slot.py --calendars PATH "
                                       "--duration-in-minutes MINUTES --minimum-people PEOPLE "
                                       "[--current-time TIME]")
        parser.add_option(option_names["minutes"], dest="minutes", type="int",
                          help="Define how many minutes people must be available")
        parser.add_option(option_names["people"], dest="people", type="int",
                          help="Define minimum number of people that must be available")
        parser.add_option(option_names["path"], dest="path", type="string",
                          help="Define directory of calendars")
        parser.add_option("--current-time", dest="time", type="string",
                          help="Define current time manually | Format: \"yyyy-mm-dd HH:MM:SS\"",
                          default=str(datetime.datetime.now()).split(".")[0])

        (options, args) = parser.parse_args()

        # check if any option in options dict is empty
        for key in option_names:
            if options.__dict__[key] is None or len(str(options.__dict__[key])) == 0:
                parser.print_usage()
                print("[!] Parameter '%s' is required" % option_names[key])
                sys.exit(0)

        # retrieve values
        minutes = options.minutes
        people = options.people
        path = options.path
        time = options.time
        try:
            time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        except ValueError as ve:
            print("[!] Incorrect format of --current-time value: %s" % ve)
            sys.exit(0)

        # add '/' separator before destination directory if not provided
        if not path.startswith("/"):
            path = "/" + path
        # normalize path
        path = os.path.normpath(os.path.dirname(os.path.abspath(__file__)) + path)
        # if script is running on system other than Windows remove '/' on the end if exists
        # on Windows os.path.normpath removes it
        if path.endswith("/"):
            path = path[:-1]

        # validate input
        result = validator.validate_input(path, minutes, people)
        if result is not None:
            print(result)
            sys.exit(0)

        finder = Finder(path, minutes, people, time)
        result = finder.search()
        print(result)

    except KeyboardInterrupt:
        print("Ctrl^C exit")
        sys.exit(0)
