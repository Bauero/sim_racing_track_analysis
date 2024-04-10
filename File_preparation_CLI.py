"""
This file contains menu to operate data_preparation file
"""

import os
import csv
from data_preparation import *
from additional_commands import *
from tkinter import Tk
from tkinter import filedialog


def __clean():
    os.system('cls' if os.name == 'nt' else 'clear')


def __display_path(new_file, title):
    """
    This function allows to show title in fancy way, with custom title
    """
    
    print(c_green(f"{title}") + ":\n", end = "")
    length = 0
    parts_of_new_file = new_file.split(sign)
    parts_of_new_file = parts_of_new_file[1:] if parts_of_new_file[0] == "" \
        else parts_of_new_file
    for i in range(len(parts_of_new_file)):
        if i == len(parts_of_new_file) - 1:
            print(c_pink(f"{parts_of_new_file[i]}"), end = "")
        else:
            print(c_blue(f"{parts_of_new_file[i]}"), end = "")
        length += 1
        if i < len(parts_of_new_file) - 1:
            print("\n" + " " * length + "└> ", end = "")
    
    print("\n")


def __ask_menu(func, value):
    """
    This function allows to show T/F menu with 'cancel' option in nice way

    - `func` - this is function which prints out current setting of value
    which we are modyfying
    - `value` - current value of setting
    """

    while True:
        func()
        print()
        odp = input("Select new setting\n"  +
                     c_green("T - True\n")  +
                     c_red("F - False\n")   +
                     c_yellow("C - Cancel") + 
                     "\n\n>>> ").strip().lower()
        print()
        if odp == "t" or odp == "true":
            value = True ; break
        elif odp == "f" or odp == "false":
            value = False ; break
        elif odp == "c": break
    print(c_pink("After change:\n"))
    return value


def __interactive_config(file_path):
    """
    This is internal funciton which is responsible for configutation menu which
    allows to set all necessary parameters.

    `1` - This setting is responsible for creating an external file, with 
    information stored at the beginning. This include track name, laps times 
    summary, file data and file time. This can be a good option if you want 
    to see breef summary of data

    `2` - By default, all numbers are converted into float values. This is 
    recomended, if you want to process data in python. If you want to import 
    your data to Excel, you should keep this option turned off, as it produces
    bigger files and processing takes more time.

    `3` - This option describes which algorithm will be used to clear file from
    unnecessary data. By default hard-codec option is used. This means that
    first 14 lines will be removed (all lines till title row), and then first
    3 lines (usually line with units and 2 empty lines). This means that in our
    data we still would be able to find empty lines and lines with other text
    than title (title line is line with first name equal to 'Time', exacly).
    Hard-coded option is generally faster, as it doesn't parse all lines, but
    is not resiliant for some obvious loss

    `4` - This option allows to modify default delimiter which will be used
    while preprocessing file. This is useful, when we have file which uses
    different separator than ',' (default in csv - Coma Separated Value).
    Sometimes this is the reason why we cannot process the file corectly

    `5` -  This option allows to remove whole columns from data. It works, by 
    finding numbers of provided columns and then removes data from all rows
    which are located under those numbers (ex. 'time 2' - col. 45 - removes
    elements which are on position 45 from all rows). By default no columns
    are removed. You can can modify col. to remove using those methods.:
    - `f` - remove physical data (all columns which are mentioned in file 
    'physical_columns_to_remove.txt')
    - `u` - upload file with columns names (file must be formated like
    'physical_columns_to_remove.txt' - no additional lines, only enter on end)
    - `w` - allows to write column names manually (you write name of each 
    column, and press Enter. If you press Enter and don't write any name
    this is considered as 'save current conf' option)
    - `d` - set values back to default (no columns to remove)
    """
    
    confimed = False
    mk_file = False
    cov_val_fl = True
    h_cod_rem = True
    delimiter = ","
    col_to_rem = []

    if file_path:
        __display_path(file_path, "You've choosen the following file/directory")

    print(c_yellow("Before proceeding confirm current configuration:\n\n"))

    def conf_mkfile():
        # Conversion to str is necesary, because for whatever reason, this code
        # doesn't work properly without it on 3.11. In other examples it does
        # fine
        print(c_blue('1') + " - Write general race info in separate file = " +
              str(c_green("True") if mk_file else c_red("False")))
    
    def conf_cvf():
        print(c_blue('2') + " - Convert values using float ; not str = " +
              c_green("True") if cov_val_fl else c_red("False"))

    def conf_hcr():   
        print(c_blue('3') + " - Remove rows using hard-coded solution = " +
              c_green("True") if h_cod_rem else c_red("False"))

    def conf_del():
        print(c_blue('4') + " - Modify current delimiter. Current = " +
              f"'{delimiter}'")

    def conf_ctr():
        if not col_to_rem:
            print(c_blue('5') + " - Columns which will be removed from data: " +
                  c_red("No columns to remove ") + "( [] )")
        else:
            print(c_blue('5') + " - Those columns will be removed from data:\n[")
            for n, col in enumerate(col_to_rem):
                print(f"  '" + c_cyan(col) + 
                      f"'{',' if n+1 < len(col_to_rem) else ''}")
            print("]")

    def h():
        conf_mkfile()
        print()
        conf_cvf()
        print()
        conf_hcr()
        print()
        conf_del()
        print()
        conf_ctr()
        print()

    h()

    while not confimed:

        o = input("\nNumber + Enter => Modify config | Enter => Confirm " +
                  "current config\n(" +
                  f"'{c_pink('a')}' to {c_pink('display all configs')} | " +
                  f"'{c_blue('h')}' for {c_blue('help')} | " +
                  f"'{c_yellow('c')}' to {c_yellow('cancel')})\n\n>>> ")
        
        o = o.strip().lower()

        if o:
            __clean()
            match o:
                case "1":
                    mk_file = __ask_menu(conf_mkfile, mk_file)
                    __clean()
                    print(c_pink("After change:\n"))
                    conf_mkfile()
                    print("\n")
                case "2":
                    cov_val_fl = __ask_menu(conf_cvf, cov_val_fl)
                    __clean()
                    print(c_pink("After change:\n"))
                    conf_cvf()
                case "3":
                    h_cod_rem = __ask_menu(conf_hcr, h_cod_rem)
                    __clean()
                    print(c_pink("After change:\n"))
                    conf_hcr()
                case "4":
                    while True:
                        conf_del()
                        print()
                        odp = input("Choose what do you wan to do:\n" +
                            "s - set semicolon (;) as a separator\n" + 
                            "t - set tabulator (\\t) as separator\n" +
                            "e - set enter (\\n) as a separator\n" +
                            "w - write symbol which would be a separator\n" +
                            "d - set default (,)\n\n>>> ").strip().lower()
                        match odp:
                            case "s": delimiter = ";" ; break
                            case "t": delimiter = "\t" ; break
                            case "e": delimiter = "\n" ; break
                            case "d": delimiter = "," ; break
                            case "w":
                                delimiter = print("\nEnter new separator >>> ", 
                                            end="")
                                break
                    __clean()
                    print(c_pink("After change:\n"))
                    conf_del()
                case "5":
                    while True:
                        conf_ctr()
                        print()
                        odp = input("Choose what do you want to do:\n" +
                            "f - remove physical data\n" +
                            "u - upload config from file\n" +
                            "w - write names manually\n" +
                            "d - set value to default ""(no columns removed)\n\n" +
                            ">>> ").strip().lower()
                        print()
                        if odp == "d":
                            col_to_rem = [] ; break
                        elif odp == "f":
                            col_to_rem = physical_columns ; break
                        elif odp == "u":
                            Tk().withdraw()
                            file = filedialog.askopenfilename(
                                title="Choose file with columns to remove",
                                filetypes=[("Text file", "*.txt")])
                            
                            if not file:
                                print(c_red("No file was choosen !!!"))
                                ans = input(r"Do you want to try again? [y\N]" +
                                            "\n>>> ").strip().lower()
                                if ans == "y":
                                    __clean()
                                    continue
                                else:
                                    break
                            try:
                                f = open(file)
                                col_to_rem = [a.strip() for a in f.readlines()]
                                f.close()
                                break
                            except KeyError as e:
                                print(f"Data read failed - {e}")
                        elif odp == "w":
                            print("Write name of each column in new line. " +
                                  "Pressing Enter in empty line will save result")
                            tmp = []
                            while True:
                                ans = input(">>> ").strip()
                                if ans: tmp.append(ans)
                                else:
                                    col_to_rem = tmp
                                    break
                            break
                    __clean()
                    print(c_pink("After change:\n"))
                    conf_ctr()                           
                case "a":
                    __clean()
                    print(c_yellow("Current config after changes\n\n"))
                    h()
                case "h":
                    __clean()
                    print(__interactive_config.__doc__[125:], end = "")
                    input("\n\nPress Enter to continue >>> ")
                    __clean()
                    print(c_yellow("Current config after changes\n\n"))
                    h()
                case "c":
                    __clean()
                    a = input("Do you want to cancel process and go to main " +
                              f"menu? [{c_red('y')} \\ {c_green('N')}]" + 
                              "\n\n>>> ").strip().lower()
                    if a == "y":
                        return None
                    else:
                        __clean()
                        h()
        else:
            confimed = True

    return mk_file, cov_val_fl, h_cod_rem, delimiter, col_to_rem


def multiple_file_processing(data_to_process,
                               mk_file : bool,
                               cov_val_fl : bool,
                               h_cod_rem : bool, 
                               col_to_rem : bool,
                               processed_size : int, 
                               sum_of_sizes : int, 
                               v : bool,
                               delim : str = ",",
                               directory_choosen : str = "."):
    """
    This function allows to execute function `prepare data` multiple times

    - `mk_file` (bool) - Do you want to create additional file with information
    which are stored on the front of the file.

    - `cov_val_fl` (bool) - What conversion mechanism you want to use - float
    conversion (True) or string modification (False)

    - `h_cod_rem` (bool) - If line-removal is done using hard-coded solution

    - `sum_of_sizes` (int) - Value used to display progress in file conversion

    - `v` (bool) - Do you want to process file in 'verbose' mode

    - `delim` (str) - this param tells csv file preprocessor what delimiter was
    used in the file, to separate values

    - `directory_choosen` (str) - Directory path under which files will be saved
    """

    for n, elem in enumerate(data_to_process):
        file_name, file_path, size = elem.values()
        save_dir = directory_choosen if directory_choosen else file_path
        print(f"Processing file {n+1}/{len(data_to_process)} - '{file_name}' " +
              "...\n")
        try:
            full_csv_file_path = f"{file_path}" + \
                    f"{'' if file_path.endswith(sign) else sign}" +\
                    f"{file_name}"
            file = open(full_csv_file_path)
            csvreader = list(csv.reader(file, delimiter=delim))
            values = prepare_data(csvreader, 
                                    v, 
                                    cov_val_fl, 
                                    h_cod_rem, 
                                    col_to_rem)
            race_data, data_all_laps, data_for_best_lap, best_time_section, \
                processed_file = values
            
            time, date = race_data["log_time"], race_data["log_date"]

            time = time.replace("/","-").replace("\\","-").replace(":","-")
            date = date.replace(".","-").replace("/","-")

            # save_dir =  f"{save_dir}{sign}data_information_{date}_{time}"
            save_dir =  f"{save_dir}" + \
                        f"{sign if not save_dir.endswith(sign) else ''}" + \
                        f"{file_name.split('.')[0]}"

            if not os.path.exists(save_dir):
                os.mkdir(save_dir)

            save_laps_section_all_laps(save_dir, data_all_laps, 
                                        f"{date}_{time}_all_laps")
            save_laps_section_all_laps(save_dir, data_for_best_lap, 
                                        f"{date}_{time}_best_lap")
            save_data_best_sections(save_dir, best_time_section, 
                                        f"{date}_{time}_best_section")

            if mk_file:
                txt_file_name = f"{date}_{time}_file_summary.txt"
                new_file = f"{save_dir}" + \
                    f"{'' if save_dir.endswith(sign) else sign}" +\
                    f"{txt_file_name}"
                
                if v:
                    __display_path(new_file, 
                            "Writing information to .txt file under location")

                txt_file = open(new_file, "w")
                ts = display_track_summary(race_data,
                                             race_data['laps_start_end'])

                if v:
                    print(c_green("Writing information to file Sucessful\n"))
            
                txt_file.write(ts)
                
                txt_file.close()

            if v:
                print("-" * 80 + "\n")
                __display_path(full_csv_file_path, 
                            "Writing information to .csv file under location")

            save_data_csv(processed_file, date, time, save_dir)
            
            if v:
                print(c_green("Writing information to file Sucessful\n"))

            processed_size += size
            print("-" * 80 + "\n")
            print(f"File '{file_name}' processed - progress " +
                  f"{processed_size/sum_of_sizes:.1%}\n")
            print("\n" + "*" * 80 + "\n\n")
        except Exception as e:
            print(c_red(f"Couldn't process file {file_name} - {e}"))
            odp = input(r"Do you want to continue? [y\N] ")
            if odp == "n": break


def option1(v : bool):
    """
    This option is ment to allow to process one file individually. 
    
    1. You choose file

    2. You set parameters

    3. File is proceesed, and then you can return to main menu
    """
    Tk().withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    dir_path = sign.join(file_path.split(sign)[0:-1])

    __clean()

    ans = __interactive_config(file_path if v else '')
    if ans == None: return

    mk_file, cov_val_fl, h_cod_rem, delim, col_to_rem = ans

    __clean()

    print(c_green("Configutraiton saved !\n"))
    ans = input(
        c_yellow("Do you want to change place where files will be saved?") +
        "\nPress 'y' + Enter to change | Enter to " + 
        "continue\n>>> ").strip().lower()
    
    if ans == 'y':
        Tk().withdraw()
        dir_path = filedialog.askdirectory(mustexist=True, initialdir=dir_path)

    __clean()

    print("Processing file ...\n")

    csv_file = open(file_path)
    csvreader = list(csv.reader(csv_file, delimiter=delim))

    race_data = processed_file = None

    try:
        values = prepare_data(csvreader, 
                              v, 
                              cov_val_fl, 
                              h_cod_rem, 
                              col_to_rem)
        race_data, data_all_laps, data_for_best_lap, best_time_section, \
            processed_file = values
    except KeyError as e:
        print(c_red(f"Operation failed: {e}"))
        input("\nPress Enter to go back to main menu >>> ")
        return
    
    try:
        time, date = race_data["log_time"], race_data["log_date"]

        time = time.replace("/","-").replace("\\","-").replace(":","-")
        date = date.replace(".","-").replace("/","-")

        dir_path = f"{dir_path}{sign}data_information_{date}_{time}"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

        save_laps_section_all_laps(dir_path, data_all_laps, 
                                   f"{date}_{time}_all_laps")
        save_laps_section_all_laps(dir_path, data_for_best_lap, 
                                   f"{date}_{time}_best_lap")
        save_data_best_sections(dir_path, best_time_section, 
                                f"{date}_{time}_best_section")
        

        if mk_file:
            file_name = f"{date}_{time}_data_information"
            new_file = f"{dir_path}{sign}{file_name}.txt"
            
            if v:
                __display_path(new_file, 
                               "Writing information to file under location")

            new_file = open(new_file, "w")
            ts = display_track_summary(race_data, race_data['laps_start_end'])

            if v:
                print(c_green("Writing information to file Sucessful\n"))
            
            new_file.write(ts)

            new_file.close()

        save_data_csv(processed_file, date, time, dir_path)

    except Exception as e:
        print(c_red(f"Operation failed: {e}"))
        input("\nPress Enter to go back to main menu >>> ")
        return

    print("#" * 80 + "\n")
    input(c_green("Operation finished") + "\n\nPress Enter to continue >>> ")


def option2(v : bool):
    """
    This option is ment to process multiple files easier than option 1.

    - `i` - you go file by file (like option 1 on loop). This is handy if you
    want different configuration for different files or want to easily test
    impact of your configuration on the file
    - `g` - you select files and then, they are processed one by one. This is
    preferred if all files would have the same settings
    """
    
    __clean()
    mode = ''

    def h():
        print(
            "Choose if you want to run interactive mode (option 1 on " +
            "repeat) or you want\nto make one settings for all files" +
            f"({c_cyan('h')} for help | {c_yellow('c')} to cancel)\n\n" +
            f"{c_pink('i - interactive mode (set params for every file)')}\n" +
            f"{c_cyan('g - generall (set once, run for all')}\n"
        )

    h()

    while True:
        odp = input("\n>>> ").strip().lower()
        
        if odp == "i":
            mode = "i" ; break
        elif odp == "g":
            mode = "g" ; break
        elif odp == "h":
            __clean()
            print(option2.__doc__, end = '')
            input("\nPress Enter to continue >>> ")
            __clean()
            h()
        elif odp == "c":
            __clean()
            a = input("Do you want to cancel process and go to main " +
                        f"menu? [{c_red('y')} \\ {c_green('N')}]" + 
                        "\n\n>>> ").strip().lower()
            if a == "y":
                return None
            else:
                __clean()
                h()
        else:
            print(c_red("\nInvalid option !!!"))

    __clean()

    match mode:
        case "i":
            while True:
                __clean()
                option1(v)
                __clean()
                a = input(
                    "File was processed. Write 'c' + Enter to cancel, and go " +
                    "back to main menu\nor press Enter to continue \n\n>>> "
                    )
                if a.strip().lower() == "c": break
        case "g":

            ans = __interactive_config("")

            if ans == None: return

            mk_file, cov_val_fl, h_cod_rem, delim, col_to_rem = ans
                
            Tk().withdraw()
            files = filedialog.askopenfilenames(filetypes=[("CSV","*.csv")])

            data_to_process = []
            processed_size = 0
            sum_of_sizes = 0
            for file in files:
                size = int(os.stat(file).st_size)
                file_name = file.split(sign)[-1]
                file_path = file[:file.index(file_name)]
                data_to_process.append({
                    "file_name" : file_name,
                    "file_path" : file_path,
                    "size" : size
                })

                sum_of_sizes += size

            __clean()

            multiple_file_processing(data_to_process,
                                     mk_file,
                                     cov_val_fl, 
                                     h_cod_rem, 
                                     col_to_rem, 
                                     processed_size, 
                                     sum_of_sizes, 
                                     v,
                                     delim,
                                     file_path)
            
            print("#" * 80 + "\n")
            input(c_green("File processing finished") + 
                  "\n\nPress Enter to go back to the menu >>> ")


def option3(v : bool):
    """
    This option is for processing files in bulk

    1. You choose directory from which all files will be converted
    
    WARNING !!!

    Directory cannot contain folder 'processed_files' - if your directory
    contains folder with this name, delete it, or move it somewhere
    
    2. You will be asked for configuration, which will be used to process all
    files   
    """

    files_detected = None
    folder_choosen = False
    directory_choosen = ""

    while not folder_choosen:
        __clean()
        folder_choosen = True    
        Tk().withdraw()
        directory = filedialog.askdirectory(mustexist=True)
        __clean

        if not directory:
            print(c_red("No directory was choosen !!!"))
            ans = input("Press Enter to return to menu or write 'r' and press "+
                        "Enter to try again >>> ").strip().lower()
            if ans == "r":
                folder_choosen = False
                break
            else:
                return

        files = list(filter(lambda x: str(x).endswith(".csv"),
                            list(os.listdir(directory))))
        
        if not files:
            print(c_red("No CSV files detected in directory !!!"))
            ans = input("Press Enter to return to menu or write 'r' and press " +
                        "Enter to try again >>> ").strip().lower()
            if ans == "r":
                folder_choosen = False
                break
    
        if v:
            print("The following files were detected:")
            for a in files:
                print("'" + c_blue(a) + "'" )
            print()

        odp = input(f"Detected {c_blue(str(len(files)) + 'files')} " + 
                    r"- proceed? [y\N] >>> ").strip().lower()
        if odp == "n": folder_choosen = False
        else:
            files_detected = files
            directory_choosen = directory

    __clean()

    ans = __interactive_config(directory_choosen)

    if ans == None: return

    mk_file, cov_val_fl, h_cod_rem, delim, col_to_rem = ans
        

    __clean()

    data_to_process = []
    processed_size = 0
    sum_of_sizes = 0

    for file in files_detected:
        size = int(os.stat(directory_choosen + sign + file).st_size)
        data_to_process.append({
            "file_name" : file,
            "file_path" : directory,
            "size" : size
        })
        sum_of_sizes += size

    directory_choosen = directory_choosen + sign + "processed_data"
    os.mkdir(directory_choosen)

    __clean()

    multiple_file_processing(data_to_process,
                             mk_file,
                             cov_val_fl,
                             h_cod_rem, 
                             col_to_rem,
                             processed_size,
                             sum_of_sizes,
                             v,
                             delim,
                             directory_choosen)
    
    print("#" * 80 + "\n")
    input(c_green("\nFile processing finished\n\n") + 
          "Press Enter to go back to the menu >>> ")
                

def menu():
    """
    This function is just a menu which allows to run internal function in easy
    way, and be able to modify settings without programming knowledge.
    """

    verbose = False
    __clean()
    print(c_pink("Welcome to data preparation program :)\n\n"))

    def hint():
        print(c_cyan("Here are the available options:\n"))
        print(c_blue("1") + " - modify specific file\n")
        print(c_blue("2") + " - modify multiple files\n")
        print(c_blue("3") + " - modify all files in specified directory\n")
        print(c_blue("4") + " - run commands with extensive description " + 
              "(currently set to " +
              str(c_green("True") if verbose else c_red("False")) +
              " )\n")
        print(c_blue("5") + " - " + c_red("exit"))

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
        elif odp not in ["1","2","3","4","5","h"]:
            print(c_red("\nGiven value is not an option !!!"))
            continue
        else:
            __clean()
            match odp:
                case "1":
                    option1(verbose)
                    tmp = True
                    __clean()
                case "2":
                    option2(verbose)
                    tmp = True
                    __clean()
                case "3":
                    option3(verbose)
                    tmp = True
                    __clean()
                case "4":
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
                case "5":
                    break
                case "h":
                    __clean()
                    tmp = True

    __clean()
    exit()


if __name__ == "__main__":
    menu()
