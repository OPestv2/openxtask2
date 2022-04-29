import optparse
import sys

from Finder import Finder

if __name__ == "__main__":
    # store option names and corresponding variable names in dict
    option_names = {"minutes": "--duration-in-minutes", "people": "--minimum-people", "path": "--calendars"}
    try:
        parser = optparse.OptionParser("python3 find_available_slot.py --calendars PATH "
                                       "--duration-in-minutes MINUTES --minimum-people PEOPLE")
        parser.add_option(option_names["minutes"], dest="minutes", type="int",
                          help="Define how many minutes people should be available")
        parser.add_option(option_names["people"], dest="people", type="int",
                          help="Define minimum number of people that must be available")
        parser.add_option(option_names["path"], dest="path", type="string",
                          help="Define directory of calendars")

        (options, args) = parser.parse_args()

        # check if any option in options dict is empty
        for key in option_names:
            if options.__dict__[key] is None:
                parser.print_usage()
                print("[!] Parameter '%s' is required" % option_names[key])
                sys.exit(0)

        finder = Finder()


    except KeyboardInterrupt:
        print("Ctrl^C exit")
        sys.exit(0)
