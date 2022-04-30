import glob
import os.path


def validate_input(path, minutes, people):
    """
    Function checks if minutes and people variables are positive values and path exists and contains .txt files

    :return: Function returns None if no error occurs or error message
    """

    # check if values are negative
    if minutes <= 0:
        return "[!] Number of minutes must not be a negative value"
    if people <= 0:
        return "[!] Number of people must not be a negative value"

    # check if path exists
    if not os.path.exists(path):
        return "[!] Directory '%s' not found" % path

    # check if there is any .txt file
    files = glob.glob(os.path.normpath(path + "/*.txt"))
    if len(files) == 0:
        return "[!] No files to read in '%s' directory" % path

    # check if number of files is greater or equal to required number of people
    num_of_files = len(files)
    if people > num_of_files:
        return "[!] Insufficient number of calendar files. Expected at least %d files (%d available in directory '%s')" \
               % (people, num_of_files, path)
      
    return None
