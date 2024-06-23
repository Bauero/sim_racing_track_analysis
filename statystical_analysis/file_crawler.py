import os
from statystical_analysis.additional_commands import *
from constants import sign
from tkinter import Tk
from tkinter.filedialog import askdirectory


def __file_in_relative_loc(base_folder,
                           directory_of_file, 
                           file, 
                           color : bool = False):
    if color:
        return c_blue(directory_of_file.replace(base_folder, '...')) + \
                      sign + c_pink(file)
    return directory_of_file.replace(base_folder, '...') + sign + file


def __search_for_files_in_dir(path):
    
    file_structure = os.walk(path)
    files_to_process = {}
    counter = 0

    for record in file_structure:
        fpath, folders, files = record
        for f in files:
            if f.endswith("_cleaned_data.csv"):
                if fpath not in files_to_process.keys():
                    files_to_process[fpath] = []
                files_to_process[fpath].append(f)
                counter += 1

    return files_to_process, counter


def __multiple_file_analysis():
    while True:
        clean()
        Tk().withdraw()
        path = askdirectory()

        if not path:
            clean()
            print(c_red("No place was selected!\n"))
            a = input("Do you want to try again? " + 
                    f"[{c_green('y')}\{c_red('N')}] >>> ").strip().lower()
            if not a or a == 'n':
                break
            continue
        files_to_process, number_of_files = __search_for_files_in_dir(path)

        if files_to_process:
            clean()
            print("In total " + 
                c_blue(f"{number_of_files} " + 
                        'files' if number_of_files > 1 else 'file') + 
                ' were found:\n')
            
            for dir in list(files_to_process.keys()):
                files = files_to_process[dir]
                amount = c_green('True') if len(files) > 1 else c_red('False')
                for f in files_to_process[dir]:
                    print(__file_in_relative_loc(path, dir, f, True), amount)
            break

        else:
            print(c_red("In the following localization (including subfolders) "+ 
                        "there were no files to process!\n"))
            a = input("Do you want to try again? " + 
                     f"[{c_green('y')}\{c_red('N')}] >>> ").strip().lower()
            if a == 'n': break


__multiple_file_analysis()
