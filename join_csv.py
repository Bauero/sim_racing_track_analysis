#! /usr/local/bin/python3.11
from os import walk, path, curdir
from tkinter.filedialog import askdirectory
from tkinter import Tk
import pandas as pd


def concatenate_files(input_directory, store_directory : str = "", \
                      output_file_name : str = 'concatenated', 
                      verbose : bool = False):
    """
    This function is responsible for finding and concatenating all files
    which are .csv files and combining them into one file

    input_directory: place from which function should start searching
    
    store_directory [optional]: place where final result will be sotred
    \t(by default file is stored in the same localzation as python file itself)
    """

    # Path to save the concatenated CSV file
    output_file = output_file_name + ".csv"

    # List to hold all DataFrames
    data_frames = []

    # if verbose: print(list(map(lambda x: filter(x.endswith("_cleaned_data.csv"), ), list(walk(input_directory)))))  # DEBUG

    elements = list(walk(input_directory))

    files_to_process = []

    for elem in elements:
        root, dirs, files = elem
        for f in files:
            if f.endswith("_cleaned_data.csv") and (root.split("/")[-3] == "Cleaned data"):
                files_to_process.append((root, f))

    columns_to_keep = ['Section', 'Time', 'Time_on_lap', 'STEERANGLE', 'THROTTLE', 'RPMS', 'G_LAT', 'G_LON', 'SPEED', 'BRAKE', 'LAP_BEACON']

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

    concatenated_df.to_csv(
    store_directory + "/" + output_file if store_directory else output_file,
    index=False
    )
    

    # def search_dir_recursivly(start_directory : str):
    #     """
    #     This funciton will recursivly search through all folders and
    #     for each file with extension .csv except 'concatenated.csv'
    #     add file name into variable data_frames
    #     """

    #     root, dirs, files  = list(walk(start_directory))[0]
    #     for filename in files:
    #         if filename.endswith('cleaned_data.csv') and filename != output_file:
    #             file_path = path.join(start_directory, filename)
    #             df = pd.read_csv(file_path)
                # df.insert(2, "'Numer Testu'", [f"'{root[-4:]}'" for _ in range(len(df.index))])
    #             data_frames.append(df)
    #     for dir in dirs:
    #         search_dir_recursivly(root+"/"+dir)


    # search_dir_recursivly(input_directory)

    # # Concatenate all DataFrames into a single DataFrame
    # concatenated_df = pd.concat(data_frames, ignore_index=True)

    # # Save the concatenated DataFrame to a CSV file
    # concatenated_df.to_csv(
    #     store_directory + "/" + output_file if store_directory else output_file,
    #     index=False
    #     )

    # if verbose: print("CSV files concatenated and saved as", output_file , 
    #       store_directory if store_directory else "") # DEBUG


# If file is execute separately (not imported) -> execute
if __name__ == "__main__":

    dir = None

    while dir == None:
        Tk().withdraw()
        dir = askdirectory(title="Select directory to look for files recursively")
        Tk().destroy()
        if dir == None:
            print("No directory selected - write C + Enter to cancel or just Enter to retry")
            a = input(">>> ").lower().strip()
            if a == 'c':
                exit()
        
    print(f"Operation successful - you've selected: {dir}")

    print("\n Press Enter to proceed to selection of save directory")

    savedir = None

    while savedir == None:
        Tk().withdraw()
        savedir = askdirectory(title="Select directory to look for files recursively")
        Tk().destroy()
        if savedir == None:
            print("No directory selected - write C + Enter to cancel or just Enter to retry")
            a = input(">>> ").lower().strip()
            if a == 'c':
                exit()

    # starts execution of funcitno from directory of file itself
    concatenate_files(dir, savedir, verbose = True)
