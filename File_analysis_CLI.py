"""
This file contains menu to operate data_analysis file
"""
import os
from tkinter import Tk
from tkinter.filedialog import askdirectory
from additional.additional_commands import *
from statystical_analysis.data_analysis import data_analysis
from additional.constants import sign


#############################  INTERNAL FUNCITONS  #############################


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


def __modify_list_of_files(path, files_to_process):

    clean()

    print("Those are all detected files:\n")

    files_by_number = {}
    number = 0
    for dir in list(files_to_process.keys()):
        files = files_to_process[dir]
        for f in files:
            number += 1
            files_by_number[str(number)] = (dir, f)
            print(f"{number}.", __file_in_relative_loc(path, dir, f, True))

    print(c_yellow("\nIf you want to make changes before saving you " +
                       "can define which files to skip\n\n") +
              c_blue("For Example:\n") +
              "2,3,4 -> skip files 2, 3, 4\n"
              "[2,5] -> skip files from 2 to 5 => 2, 3, 4, 5\n"
              "1+[3,5]+8 -> skip files 1, 3, 4, 5, 8\n"
              f"\n(press '{c_green('Enter')}'"
              " to continue without skipping any files)")
    
    files_to_skip = []
    
    while True:
        ans = input("\nDefine files to remove\n>>> ").strip()
        if not ans:
            print(c_red("\nAll files will be saved ...\n"))
            break
        sections = ans.split("+")
        sections = [s.strip() for s in sections]

        error = False

        for s in sections:
            openP, closeP  = '[' in s, ']' in s
            if openP != closeP:
                print(c_red(f"Paranthesis not closed - '{s}'"))
                error = True
                break
            if openP == True:
                try:
                    begining, end = s.split(",")
                except ValueError as e:
                    print(c_red(e))
                    error = True
                    break
                
                begining = begining.strip()[1:]
                end = end.strip()[:-1]

                try:
                    begining = int(begining)
                except Exception as e:
                    print(c_red(f"Problem occured while converting beginning"
                                f" of range in {s}:\n{e}"))
                    error = True
                    break
                    
                try:
                    end = int(end)
                except Exception as e:
                    print(c_red(f"Problem occured while converting end"
                                f" of range in {s}:\n{e}"))
                    error = True
                    break
                
                files_to_skip += list(range(begining, end + 1))

            else:
                numbers = s.split(",")
                numbers = [n.strip() for n in numbers]
                for n in numbers:
                    try:
                        n = int(n)
                    except Exception as e:
                        print(c_red(f"{e}"))
                        error = True
                        break
                    files_to_skip.append(n)
        
        if not error: break
    
    if files_to_skip:
        print(c_red("\nSkipping files: "
                    f"{', '.join([str(a) for a in files_to_skip])}\n"))
        for f in files_to_skip:
            f = str(f)
            path_to_file = files_by_number[f][0]
            name_of_file = files_by_number[f][1]
            files_to_process[path_to_file].remove(name_of_file)
            if files_to_process[path_to_file] == []:
                files_to_process.pop(path_to_file)

    return files_to_process, number - len(files_to_skip)
            

def __multiple_file_analysis(v):

    full_success_counter = 0
    full_fail_counter = 0
    any_files_were_analyzed = False

    while True:
        clean()
        Tk().withdraw()
        path = askdirectory()

        clean()

        if not path:
            print(c_red("No place was selected!\n"))
            a = input("Do you want to try again? " + 
                    f"[{c_green('y')}\{c_red('N')}] >>> ").strip().lower()
            if not a or a == 'n':
                break
            continue
        
        files_to_process, number_of_files = __search_for_files_in_dir(path)

        if number_of_files == 0:
            print(c_red("In the following localization (including subfolders) "+ 
                        "there were no files to process!\n"))
            a = input("Do you want to try again? " + 
                     f"[{c_green('y')}\{c_red('N')}] >>> ").strip().lower()
            if a == 'y': continue
            break

        clean()
        print("In total " + 
            c_blue(f"{number_of_files} " + 
                    'files' if number_of_files > 1 else 'file') + 
            ' were found\n')
        
        if v:
            for dir in list(files_to_process.keys()):
                files = files_to_process[dir]
                for f in files:
                    print(__file_in_relative_loc(path, dir, f, True))
            print()

        print("Choose what you want to do:\n" + 
                f"Press '{c_blue('Enter')}' to continue\n" +
                f"Press '{c_cyan('m')+' + '+c_cyan('Enter')}' to modify list\n"+
                f"Press '{c_yellow('c')+ ' + ' +c_yellow('Enter')}' to cancel")
        a = input(">>> ").strip().lower()
        if a == 'c': break
        elif a == 'm':
            values = __modify_list_of_files(path, files_to_process)
            files_to_process, number_of_files = values

        clean()
        any_files_were_analyzed = any(files_to_process)
        print("File processing started ...")

        for dir in list(files_to_process.keys()):
            files = files_to_process[dir]
            amount = len(files) > 1
            for f in files:
                date, time = f.split("_")[0:2]
                save_path = dir
                if amount:
                    save_path = f"{dir}{sign}{date}_{time}"
                    if not os.path.exists(save_path):
                        os.mkdir(save_path)
                try:
                    if v:
                        print(f"\nProcessing file '{c_cyan(f)}'")
                    data_analysis(dir + sign + f, save_path, date, time)
                    if v:
                        print(c_green("Processing successful"))
                    full_success_counter += 1
                    continue
                except Exception as e:
                    full_fail_counter += 1
                    if v:
                        print(c_red("Processing failed"))
                    print(c_red(f"The following exception occured: \n{e}"))
                    odp = input(r"Do you want to continue? [y\N] ")
                    if odp == "n": break

        break
 
    if any_files_were_analyzed:
        if full_success_counter > 0 and full_fail_counter == 0:
            print(c_green("\nOperation finished successfully"))
        elif full_fail_counter > 0 and full_success_counter == 0:
            print(c_red("\nOperation fully failed"))
        else:
            print(c_yellow("\nOperation partially successful"))

    input("\nPress Enter to go back to main menu >>> ")


##############################  PUBLIC FUNCITONS  ##############################


def menu():
    """
    This function displays menu which allow to select how do you want do analyze
    data. You have 3 options:

    1. Analyze one specific folder in which contains at least one file for
    analysis (valid file, is file with name ending on '_cleaned_data.csv')

    You select this folder

    └> file_to_be_analyzed.csv


    2. This funciton is ment to process multiple folder - each one with each set
    of data - this is ment to be used with data obtained after preprocessing
    multiple files using option '3' in 'File_preparation_CLI'

    You select this folder

    └> Folder #1 with data

        └> File to be analyzed

    └> Folder #2 with data

        └> File to be analyzed
    
    └> Folder #3 with data

        └> File to be analyzed
    """

    verbose = False

    clean()
    print(c_pink("Welcome to data analysis program :)\n\n"))

    def hint():
        print(c_cyan("Here are the available options:\n"))
        print(c_blue("1") + " - analyze all files within selected folder\n")
        print(c_blue("2") + " - run commands with extensive description " + 
              "(currently set to " +
              str(c_green("True") if verbose else c_red("False")) +
              " )\n")
        print(c_blue("e") + " - " + c_red("exit"))

    tmp = True

    while True:

        if tmp:
            hint()
            odp  = input("\n\nChoose option >>> ").strip().lower()
            tmp = False
        else:
            odp  = input("\nChoose option ('h' for hint) >>> ").strip().lower()

        if len(odp) > 1:
            print(c_red("\nGiven value is too long !!!"))
            continue
        elif odp not in ["1","2","e","h"]:
            print(c_red("\nGiven value is not an option !!!"))
            continue
        else:
            clean()
            match odp:
                case "1":
                    __multiple_file_analysis(verbose)
                    tmp = True
                    clean()
                case "2":
                    verbose = not verbose
                    if verbose:
                        print(c_green(
                            "Now command will be executed with description\n"
                            ))
                    else:
                        print(c_red(
                            "Now command won't executed with extensive " + \
                                " description\n"
                            ))
                    tmp = True
                case "e":
                    break
                case "h":
                    clean()
                    
                    tmp = True

    clean()


if __name__ == "__main__":
    menu()
