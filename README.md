# openxtask2


## Files overview

### find_available_slot.py
This is the main file used to run the script. It parses the parameters, passes them to validator and
runs _search()_ method from _Finder_ class.

### validator.py
This script takes and validates three parameters _path_, _minutes_ and _people_ 
required to find the solution.

### finder.py
This file contains _Finder_ class which loads timetables of events from files under given path and 
calculates periods of free time from retrieved periods of busy time. On this basis,
it finds the soonest date when required number of people are available for required amount of time.
> Event is a period of busy time defined in calendar file. Each single line specifies one event.

## Usage

To start script use [find_available_slot.py](find_available_slot.py) file.  
Run `python find_available_slot.py -h` to get info about syntax.

### Syntax
```bash
python find_available_slot.py 
        --calendars PATH --duration-in-minutes MINUTES 
        --minimum-people PEOPLE [--current-time TIME]
```
| Arguments                     | Description                                                                      |
|-------------------------------|----------------------------------------------------------------------------------|
| --calendars=PATH              | Define directory of calendar files.                                              |
| --duration-in-minutes=MINUTES | Define how many minutes people must be available                                 |
| --minimum-people=PEOPLE       | Define minimum number of people that must be available                           |
| --current-time=TIME           | Define current time manually that will be the reference point in the calculation |

#### PATH
Path to calendars must be under openxtask2 project directory. 
For example ```--calendars /in/calendars``` path tells the script to look for files in
```.../openxtask2/in/calendars``` directory.

Calendar files must be text files with ```.txt``` extension.
Calendar file must follow the rules:
* Event dates must be expressed by one of the following formats:
  * ```YYYY-mm-dd HH:MM:SS - YYYY-mm-dd HH:MM:SS``` 
    * Spaces before and after dash ```-``` separating both dates is required
  * ```YYYY-mm-dd```
* One event per line allowed
* Provide non-overlaping dates and in chronological order
* It is required to add leading zeros ```0``` to values that are one character long. 
For example: 2022-**0**4-**0**3

#### PEOPLE
This argument must not be greater than number of available calendar files.

#### TIME
This parameter is **not required** and by default sets the current time to _now_. 
Time must be expressed by following format: ```YYYY-mm-dd HH:MM:SS```. 
Make sure to put this string in quotes ```""``` as it contains space character.


## Testing

### Test files overview

#### validator_tests.py
This script allows to test user input validation. Test cases:
* MINUTES and PEOPLE arguments are non-positive values
* PATH does not exist
* no files found under PATH
* insufficient number of calendar files in relation to the number of PEOPLE

#### finder_tests.py
This script allows to test correctness of the result of the _Finder.search()_ method 
and uses example calendar files located under ```.../openxtask2/tests/in/``` path in three directories: ```/empty_file```, ```/multiple_calendars``` and ```/reversed_dates```. 
Test cases:
* The event consists of non-chronologically set dates
* One of calendar files is empty
* Multiple calendars and variable number of people and minutes

### Usage
To run tests use [finder_tests.py](tests/finder_tests.py) or [validator_tests.py](tests/validator_tests.py) file.
Navigate to ```.../openxtask2``` directory and run tests using following commands:

```text
python -m unittest tests/validator_tests.py
python -m unittest tests/finder_tests.py
```

***
> Script created with Python 3.9

Created by Jakub Sieczka ([Opestv2 GitHub](https://github.com/OPestv2 "OPest Github"))