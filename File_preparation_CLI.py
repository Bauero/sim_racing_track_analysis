"""
This file contains menu to operate data_preparation file
"""

import os
from data_preparation import *
from tkinter import Tk
import csv
from tkinter import filedialog


def __clean():
    os.system('cls' if os.name == 'nt' else 'clear')


def __display_path(new_file, title):
    """
    This function allows to show title in fancy way, with custom title
    """
    
    print("\033[92m" + f"{title}" +"\033[0m:\n\033[94m", end = "")
    length = 0
    parts_of_new_file = new_file.split(sign)
    parts_of_new_file = parts_of_new_file[1:] if parts_of_new_file[0] == "" \
        else parts_of_new_file
    for i in range(len(parts_of_new_file)):
        if i == len(parts_of_new_file) - 1:
            print("\033[95m", end ="")
        print(f"{parts_of_new_file[i]}", end = "")
        length += 1
        if i < len(parts_of_new_file) - 1:
            print("\n" + " " * length + "└> ", end = "")
    print("\033[0m\n")


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
        odp = input("Select new setting\n\033[92mT - True\n\033[91mF - " +
                    "False\033[0m\n\033[93mC - Cancel\033[0m\n\n>>> ")\
                        .strip().lower()
        print()
        if odp == "t" or odp == "true":
            value = True ; break
        elif odp == "f" or odp == "false":
            value = False ; break
        elif odp == "c": break
    print("\033[95mAfter change:\033[0m\n")
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

    print("\033[93mBefore proceeding confirm current configuration:\033[0m\n\n")

    def conf_mkfile():
        print("\033[94m1\033[0m - Write general race info in separate file = " +
              str("\033[92m" if mk_file else "\033[91m") +
              f"{mk_file}\033[0m")
    
    def conf_cvf():
        print("\033[94m2\033[0m - Convert values using float ; not str = " +
              str("\033[92m" if cov_val_fl else "\033[91m") +
              f"{cov_val_fl}\033[0m")

    def conf_hcr():    
        print("\033[94m3\033[0m - Remove rows using hard-coded solution = " +
              str("\033[92m" if h_cod_rem else "\033[91m") +
              f"{h_cod_rem}\033[0m")

    def conf_del():
        print("\033[94m4\033[0m - Modify current delimiter. Current = '" +
              f"{delimiter}\033[0m'")

    def conf_ctr():
        if not col_to_rem:
            print("\033[94m5\033[0m - Columns which will be removed from data: " +
                  "\033[91m No columns to remove \033[0m ( [] )")
        else:
            print("\033[94m5\033[0m - Columns which will be removed from data:\n[")
            for n, col in enumerate(col_to_rem):
                print(f"  '" + "\033[96m" + col + "\033[0m" + 
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
                  "current config\n" +
                  "('\033[95ma\033[0m' to \033[95mdisplay all configs\033[0m" +
                  " | '\033[96mh\033[0m' for \033[96mhelp\033[0m" + 
                  " | '\033[93mc\033[0m' to \033[93mcancel\033[0m)\n\n>>> ")
        
        o = o.strip().lower()

        if o:
            __clean()
            match o:
                case "1":
                    mk_file = __ask_menu(conf_mkfile, mk_file)
                    __clean()
                    print("\033[95mAfter change:\033[0m\n")
                    conf_mkfile()
                    print("\n")
                case "2":
                    cov_val_fl = __ask_menu(conf_cvf, cov_val_fl)
                    __clean()
                    print("\033[95mAfter change:\033[0m\n")
                    conf_cvf()
                case "3":
                    h_cod_rem = __ask_menu(conf_hcr, h_cod_rem)
                    __clean()
                    print("\033[95mAfter change:\033[0m\n")
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
                    print("\033[95mAfter change:\033[0m\n")
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
                            col_to_rem = to_remove ; break
                        elif odp == "u":
                            Tk().withdraw()
                            file = filedialog.askopenfilename(
                                title="Choose file with columns to remove",
                                filetypes=[("Text file", "*.txt")])
                            
                            if not file:
                                print("\033[91mNo file was choosen !!!\033[0m")
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
                    print("\033[95mAfter change:\033[0m\n")
                    conf_ctr()                           
                case "a":
                    __clean()
                    print("\033[93mCurrent config after changes\033[0m\n\n")
                    h()
                case "h":
                    __clean()
                    print(__interactive_config.__doc__[125:], end = "")
                    input("\n\nPress Enter to continue >>> ")
                    __clean()
                    print("\033[93mCurrent config after changes\033[0m\n\n")
                    h()
                case "c":
                    __clean()
                    a = input("Do you want to cancel process and go to main " +
                              "menu? [\033[91my\033[0m\\\033[92mN\033[0m]" + 
                              "\n>>> ").strip().lower()
                    if a == "y":
                        return None
                    else:
                        __clean()
                        h()
        else:
            confimed = True

    return mk_file, cov_val_fl, h_cod_rem, delimiter, col_to_rem


def __multiple_file_processing(data_to_process,
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

    __clean()

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
            race_data, processed_file = prepare_data(csvreader, 
                                                     v, 
                                                     cov_val_fl, 
                                                     h_cod_rem, 
                                                     col_to_rem)
            
            if mk_file:
                txt_file_name = "data_information_" +\
                            f"{race_data['log_date'].replace('-','_')}_" +\
                            f"{race_data['log_time'].replace(':','_')}.txt"
                new_file = f"{directory_choosen}" + \
                    f"{'' if directory_choosen.endswith(sign) else sign}" +\
                    f"{txt_file_name}"
                
                if v:
                    __display_path(new_file, 
                            "Writing information to .txt file under location")

                txt_file = open(new_file, "w")
                ts = display_track_summary(race_data,
                                             race_data['laps_start_end'])

                if v:
                    print("\033[92mWriting information to file Sucessful\033[0m\n")
            
                txt_file.write(ts)
                
                txt_file.close()
            
            if v:
                print("-" * 80 + "\n")
                __display_path(full_csv_file_path, 
                            "Writing information to .csv file under location")

            save_data_csv_coma_format(processed_file,
                                      race_data['log_date'], 
                                      race_data['log_time'], save_dir)
            
            if v:
                print("\033[92mWriting information to file Sucessful\033[0m\n")

            processed_size += size
            print("-" * 80 + "\n")
            print(f"File '{file_name}' processed - progress " +
                  f"{processed_size/sum_of_sizes:.1%}\n")
            print("\n" + "*" * 80 + "\n\n")
        except Exception as e:
            print(f"\033[91mCouldn't process file {file_name} - {e}\033[0m")
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

    print("\033[92mConfigutraiton saved !\033[0m\n")
    ans = input("\033[93mDo you want to change place where files will be " + 
                "saved?\033[0m\nPress 'y' + Enter to change | Enter to " + 
                "continue\n>>> ").strip().lower()
    
    if ans == 'n':
        Tk().withdraw()
        dir_path = filedialog.askdirectory(mustexist=True, initialdir=dir_path)

    __clean()

    print("Processing file ...\n")

    csv_file = open(file_path)
    csvreader = list(csv.reader(csv_file, delimiter=delim))

    race_data = processed_file = None

    try:
        race_data, processed_file = prepare_data(csvreader, 
                                                 v, 
                                                 cov_val_fl, 
                                                 h_cod_rem, 
                                                 col_to_rem)
    except KeyError as e:
        print(f"\033[91mOperation failed: {e}\033[0m")
        input("\nPress Enter to go back to main menu >>> ")
        return
    
    try:
        if mk_file:
            file_name = "data_information_" +\
                        f"{race_data['log_date'].replace('-','_')}_" +\
                        f"{race_data['log_time'].replace(':','_')}"
            new_file = f"{dir_path}{sign}{file_name}.txt"
            
            if v:
                __display_path(new_file, 
                               "Writing information to file under location")

            new_file = open(new_file, "w")
            ts = display_track_summary(race_data, race_data['laps_start_end'])

            if v:
                print("\033[92mWriting information to file Sucessful\033[0m\n")
            
            new_file.write(ts)
            
            new_file.close()

        save_data_csv_coma_format(processed_file,
                                  race_data['log_date'],
                                  race_data['log_time'], 
                                  dir_path)
    except Exception as e:
        print(f"\033[91mOperation failed: {e}\033[0m")
        input("\nPress Enter to go back to main menu >>> ")
        return

    print("#" * 80 + "\n")
    input("\033[92mOperation finished\033[0m\n\nPress Enter to continue >>> ")


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
            " ('\033[96mh\033[0m' for \033[96mhelp" +
            "\033[0m | '\033[93mc\033[0m' to \033[93mcancel\033[0m)" +

            "\n\n\033[95mi - interactive mode " +
            "(set params to all files individually)\033[0m\n" +
            
            "\033[96mg - generall (set once, run for all)\033[0m"
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
                        "menu? [\033[91my\033[0m\\\033[92mN\033[0m]" + 
                        "\n>>> ").strip().lower()
            if a == "y":
                return None
            else:
                __clean()
                h()
        else:
            print("\n\033[91mInvalid option !!!\033[0m")

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

            __multiple_file_processing(data_to_process,
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
            input("\033[92mFile processing finished\033[0m\n\nPress Enter" +
                  " to go back to the menu >>> ")


def option3(v : bool):
    """
    This option is for processing files in bulk

    1. You choose directory from which all files will be converted
    \033[91mWarning\033[0m
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
            print("\033[91mNo directory was choosen !!!\033[0m")
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
            print("\033[91mNo CSV files detected in directory !!!\033[0m")
            ans = input("Press Enter to return to menu or write 'r' and press " +
                        "Enter to try again >>> ").strip().lower()
            if ans == "r":
                folder_choosen = False
                break
    
        if v:
            print("The following files were detected:")
            for a in files:
                print("'\033[94m" + a + "\033[0m'" )
            print()

        odp = input(f"Detected \033[94m{len(files)} files\033[0m " + 
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

    __multiple_file_processing(data_to_process,
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
    input("\n\033[92mFile processing finished\033[0m\n\nPress " +
          "Enter to go back to the menu >>> ")
                

def menu():
    """
    This function is just a menu which allows to run internal function in easy
    way, and be able to modify settings without programming knowledge.
    """

    verbose = False
    __clean()
    print("\033[95mWelcome to data preparation program :)\033[0m\n\n")
    def hint():
        print("\033[96mHere are the available options:\033[0m\n")
        print("\033[94m1\033[0m - modify specific file\n")
        print("\033[94m2\033[0m - modify multiple files\n")
        print("\033[94m3\033[0m - modify all files in specified directory\n")
        if verbose:
            print("\033[94m4\033[0m - run commands with extensive description " +
                  "(currently set to \033[92mTrue\033[0m)\n")
        else:
            print("\033[94m4\033[0m - run commands with extensive description " +
                  "(currently set to \033[91mFalse\033[0m)\n")
        print("\033[94m5\033[0m - \033[91mexit\033[0m")

    tmp = True

    while True:
        
        if tmp:
            hint()
            odp  = input("\n\nChoose option >>> ").strip().lower()
            tmp = False
        else:
            odp  = input("\nChoose option ('h' for hint) >>> ").strip().lower()

        if len(odp) > 1:
            print("\n\033[91mGiven value is too long !!!\033[0m")
            continue
        elif odp not in ["1","2","3","4","5","h"]:
            print("\n\033[91mGiven value is not an option !!!\033[0m")
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
                    __clean()
                case "4":
                    verbose = not verbose
                    if verbose:
                        print("\n\033[92mNow command will be executed with " +
                              "description\033[0m")
                    else:
                        print("\n\033[91mNow command won't executed with " +
                              "description\033[0m")
                case "5":
                    break
                case "h":
                    __clean()
                    hint()

    __clean()
    exit()


if __name__ == "__main__":
    menu()
