import datetime
import glob


class Finder:
    def __init__(self, path, minutes, people):
        self.path = path
        self.minutes = minutes
        self.people = people
        # self.current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.current_time = datetime.datetime.strptime("2022-07-01 09:00:00", "%Y-%m-%d %H:%M:%S")
        self.timetable_list = self.__load_timetables()
        # print(self.timetable_list)

    def search(self):
        pass

    def __load_timetables(self):
        """
        Function retrieves free time periods from calendar
        :return: list of free time periods
        :rtype: list
        """
        timetable_list = []
        timetable_files = glob.glob(self.path + "/*.txt")

        # number of current file
        file_cnt = 0
        # read all files
        for timetable_file in timetable_files:
            # one person timetable
            timetable_list.append([])
            # save end of last busy time period
            start_freetime_period = self.current_time
            end_freetime_period = None

            # save all lines
            with open(timetable_file, "r") as timetable:
                print(timetable.name)
                all_lines = [line.rstrip() for line in timetable]

            # to check when it is last line
            # line_counter = 0
            for line, line_cnt in zip(all_lines, range(0, len(all_lines), 1)):

                # divide line into date strings and remove spaces at start and end of them
                dates = [date.strip() for date in line.split(" - ")]
                print(f"[{line_cnt}] > ", dates)

                # busy whole day
                if len(dates) == 1:
                    # set end of free time to day before at 23:59:59
                    end_freetime_period = (datetime.datetime.strptime(dates[0] + " 23:59:59", "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=-1))

                    # difference between end free time date and start free time date in minutes
                    diff = (end_freetime_period - start_freetime_period).seconds / 60

                    # end of free time date must be higher than now and difference between start and end must be greater equal to specified amount of minutes
                    if end_freetime_period > start_freetime_period and diff != 0 and diff > self.minutes:
                        # add period
                        timetable_list[file_cnt].append([start_freetime_period.strftime("%Y-%m-%d %H:%M:%S"), end_freetime_period.strftime("%Y-%m-%d %H:%M:%S")])

                    # set start of free time to next day at 00:00:00
                    start_freetime_period = (datetime.datetime.strptime(dates[0] + " 00:00:00", "%Y-%m-%d %H:%M:%S") + datetime.timedelta(days=1))
                # busy for some time
                else:
                    end_freetime_period = (datetime.datetime.strptime(dates[0], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=-1))

                    # difference between end free time date and start free time date in minutes
                    diff = (end_freetime_period - start_freetime_period).seconds/60

                    # end of free time date must be higher than now and difference between start and end must be greater equal to specified amount of minutes
                    if end_freetime_period > start_freetime_period and diff > self.minutes:
                        timetable_list[file_cnt].append([start_freetime_period.strftime("%Y-%m-%d %H:%M:%S"), end_freetime_period.strftime("%Y-%m-%d %H:%M:%S")])

                    start_freetime_period = (datetime.datetime.strptime(dates[1], "%Y-%m-%d %H:%M:%S") + datetime.timedelta(seconds=1))

                # if it was last line in calendar add last free time period
                if line_cnt == len(all_lines) - 1:
                    # add some days to end of free time period
                    end_freetime_period = (end_freetime_period + datetime.timedelta(days=5*365))
                    timetable_list[file_cnt].append([start_freetime_period.strftime("%Y-%m-%d %H:%M:%S"), end_freetime_period.strftime("%Y-%m-%d %H:%M:%S")])
            print(timetable_list)
        return timetable_list


