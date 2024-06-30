#! /usr/local/bin/python3.11
import pandas as pd
from os import walk
from constants import sign
from additional_commands import clean, c_blue, c_green


def proper_file(root, file) -> bool:
    """
    This funciton is used for filtering files. While contcatenating files, we
    run `os.walk` command, which finds multiple files. This function defines
    which files should classify as the one for concatenation

    This fuction yields `True` only for files with names ending on 
    `_cleaned_data.csv`, and those which are stored in such a file structure 
    where the 3 folder from the top is called 'Cleaned data'

    Example
    -------
    if (>>>) is the starting directory, then

    >>> /"Cleaned data"/"folder 2"/"folder 3"/"sth_cleaned_data.csv" = True
    >>> /"folder 1"/"folder 2"/"folder 3"/"sth_cleaned_data.csv" = False
    >>> /"Cleaned data"/"folder 2"/"folder 3"/"different_file.csv" = False
    >>> /"sth_cleaned_data.csv"   <- \   !!! Raises Error !!!
    """
    
    return file.endswith("_cleaned_data.csv") and \
            (root.split("/")[-3] == "Cleaned data")

def proper_file_simplified(root, file) -> bool:
    """
    This funciton is used for filtering files. While contcatenating files, we
    run `os.walk` command, which finds multiple files. This function defines
    which files should classify as the one for concatenation

    This fuction yields `True` only for files with names ending on 
    `_cleaned_data.csv`

    Example
    -------
    if (>>>) is the starting directory, then

    >>> /"Cleaned data"/"folder 2"/"folder 3"/"sth_cleaned_data.csv" = True
    >>> /"Cleaned data"/"folder 2"/"folder 3"/"different_file.csv" = False
    """
    
    return file.endswith("_cleaned_data.csv")


def concatenate_files(input_directory, 
                      function_to_filter_files,
                      columns_to_keep : list = []) -> pd.DataFrame:
    """
    This function is responsible for finding and concatenating all files
    which are .csv files and combining them into one file

    input_directory: place from which function should start searching
    
    store_directory [optional]: place where final result will be sotred
    \t(by default file is stored in the same localzation as python file itself)
    """

    # List to hold all DataFrames
    data_frames = []
    files_to_process = []
    elements = list(walk(input_directory))

    for elem in elements:
        root, dirs, files = elem
        for f in files:
            if function_to_filter_files(root, f):
                files_to_process.append((root, f))

    file_no = 1

    for pair in files_to_process:
        root, filename = pair
        time = filename.split("_")[0]
        date = filename.split("_")[1]
        racer = root.split("/")[-2]
        df = pd.read_csv(f"{root}/{filename}", usecols = columns_to_keep)
        df.insert(5, 
                  "LAP_ID",
                  [f"{date}_{time}_{racer}" for _ in range(len(df.index))])
        df.insert(6, "LAP_NO", [file_no for _ in range(len(df.index))])
        data_frames.append(df)
        file_no += 1
    
    concatenated_df = pd.concat(data_frames, ignore_index=True)

    return concatenated_df


if __name__ == "__main__":

    from tkinter.filedialog import askdirectory
    from tkinter import Tk

    columns_to_keep = ['Section', 'Time', 'Time_on_lap', 'STEERANGLE', 
                       'THROTTLE', 'RPMS', 'G_LAT', 'G_LON', 'SPEED', 'BRAKE', 
                       'LAP_BEACON', "Distance", "Distance_on_lap"]

    dir = ""
    savedir = ""
    output_file = "concatenated.csv"

    clean()

    while not dir:
        Tk().withdraw()
        dir = askdirectory(
            title="Select directory to look for files recursively")
        Tk().destroy()
        if not dir:
            print("No directory selected - write C + Enter to " +
                  "cancel or just Enter to retry")
            a = input(">>> ").lower().strip()
            if a == 'c':
                print("Stopping execution as no directory for search selected")
                exit()
        
    clean()
    print(f"Operation successful - you've selected: {c_blue(dir)}")
    input("\nPress Enter to proceed to selection of save directory")

    while not savedir:
        Tk().withdraw()
        savedir = askdirectory(
            initialdir = dir,
            title="Select directory to save concatenated file")
        Tk().destroy()
        if not savedir:
            print("No directory selected - write C + Enter to " +
                  "cancel or just Enter to retry")
            a = input(">>> ").lower().strip()
            if a == 'c':
                print("Stopping execution as no save directory selected")
                exit()

    clean()

    # starts execution of funcitno from directory of file itself
    concat_file = concatenate_files(dir, proper_file, columns_to_keep)

    # save file in the selected directory
    concat_file.to_csv(savedir + sign + output_file, index=False)

    print(c_green("Operaiton successful"))
    input("\nPress Enter to exit >>> ")
