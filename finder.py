import datetime
import glob

# every datetime object is formatted this way
FORMAT = "%Y-%m-%d %H:%M:%S"
# end of every last free time period is set to (start + MAX_TIME)
MAX_TIME = 15*365


class Finder:
    """
    A class used to load timetables from text files and find the soonest date when required number of people
    have required amount of free time

    path: str
        path to text files
    minutes: int
        required amount of free time expressed in minutes
    people: int
        required amount of people
    current_time: datetime
        reference point in time formatted in format %Y-%m-%d %H:%M:%S


    __load_timetables():
        private method used to read all timetables from files
        and processing them to obtain timetable of free time periods

    search():
        method used to find the soonest date based on free time periods
    """

    def __init__(self, path, minutes, people, current_time):
        self.path = path
        self.minutes = minutes
        self.people = people
        self.current_time = current_time
        self.timetable_list = self.__load_timetables()

    def __print_timetable_list(self):
        """
        Function used in debugging
        """
        for timetable in self.timetable_list:
            for period in timetable:
                for boundary in period:
                    print(boundary, end=" ")
                print(", ", end="")
            print("\n")
        print("")

    def __load_timetables(self):
        """
        Function gets busy periods, rewrites them to two date object lists.
        Then calculates free time periods based on busy time periods.
        :return: list of free time periods
        :rtype: list
        """

        # result list of free time periods
        free_time_timetable = []

        # files in working directory
        timetables = glob.glob(self.path + "/*.txt")

        # read all files in working directory
        for timetable_file, file_cnt in zip(timetables, range(len(timetables))):

            # list of busy periods (temporary)
            busy_time_timetable = []
            # list of free periods (stored for further processing)
            free_time_timetable.append([])

            # save all lines to busy_time_timetable
            with open(timetable_file, "r") as timetable:

                # convert every line to datetime tuple (start, end)
                for line in timetable:
                    # remove leading and ending whitespaces
                    line = line.rstrip()

                    # split lines into dates
                    dates = line.split(" - ")

                    # busy whole day
                    if len(dates) == 1:
                        start = datetime.datetime.strptime(dates[0] + " 00:00:00", FORMAT)
                        end = datetime.datetime.strptime(dates[0] + " 23:59:59", FORMAT)
                    # exact ranges of busy time
                    else:
                        start = datetime.datetime.strptime(dates[0], FORMAT)
                        end = datetime.datetime.strptime(dates[1], FORMAT)

                    # if dates are not set chronologically, swap them
                    if end < start:
                        tmp = start
                        start = end
                        end = tmp

                    busy_time_timetable.append([start, end])

            # prepare free time periods and put them to corresponding list free_time_timetable
            for period, period_cnt in zip(busy_time_timetable, range(len(busy_time_timetable))):
                # for first period
                if period_cnt == 0:
                    start = self.current_time
                    end = period[0] + datetime.timedelta(seconds=-1)
                # any other
                elif period_cnt < len(busy_time_timetable):
                    start = busy_time_timetable[period_cnt - 1][1] + datetime.timedelta(seconds=1)
                    end = period[0] + datetime.timedelta(seconds=-1)

                # check if difference between dates is not less or equal to 0
                # and check if difference is greater or equal to required minutes
                # and check if busy period ends after or 'now'
                # otherwise don't even care about these periods
                if start < end and end >= self.current_time and (end - start).seconds/60 >= self.minutes:
                    free_time_timetable[file_cnt].append([start, end])

            # file was empty or end of last busy period is earlier than 'now' set 'now'
            if len(busy_time_timetable) == 0 or busy_time_timetable[-1][1] < self.current_time:
                # set start
                start = self.current_time
            else:
                start = busy_time_timetable[-1][1] + datetime.timedelta(seconds=1)
            end = start + datetime.timedelta(days=MAX_TIME)

            # add last period
            free_time_timetable[file_cnt].append([start, end])

            # sort timetable list by starting free time dates
            # first sort by ending date, then by starting date
            # double sort is required to obtain entirely sorted list
            free_time_timetable[file_cnt] = sorted(free_time_timetable[file_cnt],
                                                   key=lambda x: x[1], reverse=False)
            free_time_timetable[file_cnt] = sorted(free_time_timetable[file_cnt],
                                                   key=lambda x: x[0], reverse=False)

        # sort people by first date in timetable (twice as well)
        free_time_timetable = sorted(free_time_timetable, key=lambda x: x[0][1], reverse=False)
        free_time_timetable = sorted(free_time_timetable, key=lambda x: x[0][0], reverse=False)
        return free_time_timetable

    def search(self):
        """
        Function checks every combination of free time periods and return the soonest date
        when required number of people have required amount of free time
        :return: soonest date
        :rtype: datetime object
        """

        # timetable_list size
        timetable_list_size = len(self.timetable_list)

        # every iterator in iterators points to index in person's list in timetable_list
        # indicates current free time period in timetable_list[person]
        iterators = [0] * timetable_list_size

        # store current free time periods as first element of every list in timetable_list
        current_elements = [element[0] for element in self.timetable_list]

        # search until not found
        # stop condition is not required because every list in timetable_list contain
        # at least one x year long free time period (just long enough)
        while True:

            # temporary store double sorted list of current elements
            tmp_list = sorted(current_elements, key=lambda x: x[1], reverse=False)
            tmp_list = sorted(tmp_list, key=lambda x: x[0], reverse=False)

            # search for date
            # base_period is a period whose start date we use as a reference to find other matching periods
            # base_iter is an index in tmp_list used to avoid comparing base_period with itself
            for base_period, base_iter in zip(tmp_list, range(len(tmp_list))):
                # curr_min is soonest date
                curr_min = base_period[0]
                # counter of matching periods
                matching_elements = 1

                # period is used to compare with base_period
                for period, period_iter in zip(tmp_list, range(len(tmp_list))):
                    # avoid comparing base_period and period (they may be this same object)
                    if base_iter != period_iter:
                        # start of period must be before curr_min
                        # end of period must be after curr_min
                        # and time diff must be equal or greater than required amount of minutes
                        diff = period[1] - curr_min
                        diff_minutes = (diff.days * 24 * 60) + (diff.seconds / 60)
                        # diff = int(diff_seconds / 60)
                        if period[0] <= curr_min < period[1] and diff_minutes >= self.minutes:
                            matching_elements += 1
                            # if required number of people is reached return curr_min date
                            # as it is the soonest date when ALL of this people have free time
                            if matching_elements >= self.people:
                                return curr_min

            # get next elements of currently stored periods in corresponding lists
            # find next soonest date and update this value in current_elements
            list_of_next_elements = []
            # get all available 'next' elements and their indexes
            for timetable, timetable_iter in zip(self.timetable_list, range(timetable_list_size)):
                # iterate periods to the end of timetable
                if iterators[timetable_iter] < len(timetable) - 1:
                    list_of_next_elements.append((timetable[iterators[timetable_iter] + 1], timetable_iter))

            # no more options
            if len(list_of_next_elements) == 0:
                return "[!] Could not find a match"

            # get minimum value, in this case double sort is not required as we need only first values to be sorted
            # min_element contains tuple (period, index in current_elements)
            min_element = sorted(list_of_next_elements, key=lambda x: x[0], reverse=False)[0]

            # update value
            current_elements[min_element[1]] = min_element[0]
            # increase iterator
            iterators[min_element[1]] += 1
