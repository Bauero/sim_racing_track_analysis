"""
This file contains funcitons which would allow to help clean csv files exported
from Motec software. By default this file can be use as a standalone app, but
it can be run by external program
"""

import csv
import os
import tkinter as tk
from tkinter import filedialog

sign = '\\' if os.name == 'nt' else '/'
to_remove = ['SUS_TRAVEL_LF',
            'SUS_TRAVEL_RF',
            'SUS_TRAVEL_LR',
            'SUS_TRAVEL_RR',
            'BRAKE_TEMP_LF',
            'BRAKE_TEMP_RF',
            'BRAKE_TEMP_LR',
            'BRAKE_TEMP_RR',
            'TYRE_PRESS_LF',
            'TYRE_PRESS_RF',
            'TYRE_PRESS_LR',
            'TYRE_PRESS_RR',
            'TYRE_TAIR_LF',
            'TYRE_TAIR_RF',
            'TYRE_TAIR_LR',
            'TYRE_TAIR_RR',
            'WHEEL_SPEED_LF',
            'WHEEL_SPEED_RF',
            'WHEEL_SPEED_LR',
            'WHEEL_SPEED_RR',
            'BUMPSTOPUP_RIDE_LF',
            'BUMPSTOPUP_RIDE_RF',
            'BUMPSTOPUP_RIDE_LR',
            'BUMPSTOPUP_RIDE_RR',
            'BUMPSTOPDN_RIDE_LF',
            'BUMPSTOPDN_RIDE_RF',
            'BUMPSTOPDN_RIDE_LR',
            'BUMPSTOPDN_RIDE_RR',
            'BUMPSTOP_FORCE_LF',
            'BUMPSTOP_FORCE_RF',
            'BUMPSTOP_FORCE_LR',
            'BUMPSTOP_FORCE_RR']


def __display_track_summary(track_summary, laps_start_end):

    ts = ''

    # display all stats except laps data (displayed separately below)
    for stats in track_summary:
        if stats == 'beacon_makers' or stats == 'laps_start_end':
            continue
        ts += f"{stats.capitalize():20} : {track_summary[stats]}\n"

    ts += "\nLap times\n\n" # line separator for clear display of data

    # display each lap times
    for i in range(len(laps_start_end)):
        start, end = laps_start_end[str(i + 1)].values()
        ts += f'Lap {(i + 1)} : {start:08.3f} - {end:08.3f}   =   {(end - start):.3f}s\n'
    
    ts.strip()

    return ts


def __extract_general_data(file_object, verbose : bool = False) -> dict:
    """
    This funciton is responsible for removal of first rows in data which are
    responsible for storage of additional informaiton such as car model,
    track
    name,
    distance. Those data are removed from the initial table but can later
    be accessed via external variable
    """

    # Read all information which are stored in the beginning of the file
    track_summary = {
    'format' : file_object[0][1],
    'venue' : file_object[1][1],
    'vehicle' : file_object[2][1],
    'driver' : file_object[3][1],
    'device' : file_object[4][1],
    'comment' : file_object[5][1],
    'log_date' : file_object[6][1],
    'log_time' : file_object[7][1],
    'start_time' : file_object[7][5],
    'sample_rate' : file_object[8][1],
    'end_time' : file_object[8][5],
    'duration' : file_object[9][1],
    'range' : file_object[10][1],
    'beacon_makers' : ...
    }

    # Add beacon makers in readable form (list of floats)
    beacon_makers = file_object[11][1].strip().split(" ")
    beacon_makers = [float(i) for i in beacon_makers]
    track_summary['beacon_makers'] = beacon_makers

    # Prepare dict of dicts which contains start end end of each lap
    # Lap 1 : 0.000 - 107.154
    # Lap 2 : 107.154 - 446.093
    # etc.
    laps_start_end = {}
    tmp_start = float(track_summary['start_time'])
    for i in range(len(beacon_makers)):
        laps_start_end[str(i + 1)] = {"start" : tmp_start, "end" : beacon_makers[i]}
        tmp_start = beacon_makers[i]
    track_summary['laps_start_end'] = laps_start_end

    # Display informaiton in the console if 'verbose' param set to 'True'

    
    if verbose:
        print(__display_track_summary())
        
    return track_summary


def __remove_unnecessary_rows(file_object, hard_coded : bool = True, verbose : bool = False):
    """
    This function is calles to remove data which are not important in our program
    aka. empty rows,
    or rows which contains not important information [like units]

    Function contains two different solutions. By default (hard_coded == True)
    function would simply erase all 14 first rows (leaving first row as titles)
    and then remove rows 2-4 which contains units and 2 empty rows. However any
    changes to rows, as well as empty rows wouldn't be detected. 
    
    Therefore one can run this function with option 'hard_coded' set to False.
    Then function will automatically parse file to remove any empty rows and rows
    which are not column's title's row (the one, which in first column has 
    'Time' value)
    """

    if not hard_coded:
        if verbose: counter = 0

        for row in range(len(file_object) - 1,-1,-1):
        
            row = file_object[row]

            # remove all empty rows
            if row == []:
                if verbose:
                    print(f"Removing row {str(row)[:80]}")
                    counter += 1
                file_object.remove(row)
            else:

                # Skip names of columns
                if row[0] == "Time" : continue
                try:
                    float(row[0])
                except:
                    if verbose:
                        print(f"Removing row {str(row)[:80]}")
                        counter += 1
                    file_object.remove(row)

        if verbose:
            print(f"\nRemoved {counter} rows from the table")

    # Hard-coded solution - less flexible but faster
    else:
        if verbose: 
            print("Removing first 14 rows from data")
        file_object = file_object[14:]

        if verbose:
            print(f"Removing 2,3, and 4 row - first one is title : {file_object[0][:20]}")
        file_object.pop(1)
        file_object.pop(1)
        file_object.pop(1)
    
    return file_object


def __remove_unnecessary_colums(file_object, custom_to_remove : list, 
                                verbose : bool = False):
    """
    This function allows to remove unnecessary columns which are not
    necessary for our data analysis
    """    

    columns_to_remove = [file_object[0].index(i) for i in to_remove]

    if verbose:
        print("The following columns will be removed:")
        for i in range(len(to_remove)):
            print(f"Column {columns_to_remove[i]} : '{to_remove[i]}'")

    columns_to_remove = sorted(columns_to_remove, reverse=True)

    for row in range(len(file_object)):
        for col in columns_to_remove:
            file_object[row].pop(col)


    if verbose:
        print(f"\nSuccessfully removed {len(to_remove)} columns")

    return file_object


def __convert_values_to_float(file_object):
    """
    The purpose of this function is to convert all values to float
    """

    for row in range(1,len(file_object)):
        if row:
            file_object[row] = list(map(float, file_object[row]))

    return file_object


def __even_out_comma_notation_str(file_object):
    """
    This funciton is responsible for converting each value to string
    """

    # This is alternative solution to the nested in loop below
    # It is commented out because it explains better what is done
    # But is around ~30% slower

    # def convert(value):
    #     if '.' in value:
    #         value.replace('.',',')
    #         return value
    #     elif ',' in value:
    #         return value
    #     else:
    #         return value +',0'

    for row in range(1,len(file_object)):
        # file_object[row] = [convert(a) for a in file_object[row]]
        file_object[row] = [a.replace('.',',') if '.' in a else 
                                a if ',' in a else a+',0' 
                                    for a in file_object[row]]
    return file_object


def __fill_missing_lap_data(file_object, lap_info : list[list], verbose : bool = False):
    import math
    column = file_object[0].index('LAP_BEACON')

    lap = "1"
    last_time = lap_info[lap]['end']
    if verbose:
        print(f"Filling out rows in lap {lap}")

    for row in range(1,len(file_object)):
        if float(file_object[row][0]) <= last_time:
            file_object[row][column] = lap
        else:
            lap = str(int(lap) + 1)
            try:
                last_time = lap_info[lap]['end']
            except:
                last_time = math.inf
            file_object[row][column] = lap
            if verbose:
                print(f"Filling out rows in lap {lap}")

    if verbose:
        print("Filling out rows completed")

    return file_object


def prepare_data(file_object, verbose : bool = False,
                 convert_values_with_float_conversion : bool = False,
                 hard_codec_row_removal : bool = True,
                 column_remove_list : list = to_remove,
                 ):
    """
    This is general function which is responsible for data preparation

    This function returns race informaiton in form of a dictionary
    """
    race_info = __extract_general_data(file_object, verbose)
    if verbose: print()
    file_object = __remove_unnecessary_rows(file_object, hard_codec_row_removal, verbose)
    if verbose: print()
    file_object =__remove_unnecessary_colums(file_object, column_remove_list, verbose)
    if verbose: print()

    file_object = __fill_missing_lap_data(file_object, race_info['laps_start_end'], verbose)

    if convert_values_with_float_conversion:
        file_object = __convert_values_to_float(file_object)
    else:
        file_object = __even_out_comma_notation_str(file_object)
    
    return race_info, file_object


def save_data_csv_coma_format(file_object, log_date : str, log_time : str, special_path : str):
    """
    This function is responsible for storage of modified file into a new file
    """
    import csv
    
    if special_path:
        file_path = f"{special_path}{sign}cleaned_data_{log_date.replace('-','_')}_"+\
        f"{log_time.replace(':','_')}.csv"
    else:
        file_path = f"cleaned_data_{log_date.replace('-','_')}_{log_time.replace(':','_')}.csv"


    new_file = open(file_path,'w')

    csvwriter = csv.writer(new_file)
    csvwriter.writerows(file_object)

    new_file.close()


def __clean():
    os.system('cls' if os.name == 'nt' else 'clear')


def __ask_menu(func, value):
    while True:
        func()
        print()
        odp = input("Select new setting\n\033[92mT - True\n\033[91mF - False\033[0m\n\033[93mC - Cancel\033[0m\n\n>>> ").strip().lower()
        print()
        if odp == "t" or odp == "true":
            value = True ; break
        elif odp == "f" or odp == "false":
            value = False ; break
        elif odp == "c": break
        print()
    return value


def __interactive_config():
    confimed = False
    mk_file = False
    cov_val_fl = False
    h_cod_rem = True
    col_to_rem = []

    print("\nBefore proceeding confirm current configuration:\n\n\n")

    def conf_mkfile():
        if mk_file:
            print(f"(1) Make separate file with informaiton read from beginning of the file = \033[92m{mk_file}\033[0m")
        else:
            print(f"(1) Make separate file with informaiton read from beginning of the file = \033[91m{mk_file}\033[0m")
    def conf_cvf():
        if cov_val_fl:
            print(f"(2) Perform conversion of values using float funtion instad of str modification (which is preferred) = \033[92m{cov_val_fl}\033[0m")
        else:
            print(f"(2) Perform conversion of values using float funtion instad of str modification (which is preferred) = \033[91m{cov_val_fl}\033[0m")
    def conf_hcr():    
        if h_cod_rem:
            print(f"(3) Remove rows using hard-coded colution (faster but can leave empty rows in the datataset if they are not in the usual place) = \033[92m{h_cod_rem}\033[0m")
        else:
            print(f"(3) Remove rows using hard-coded colution (faster but can leave empty rows in the datataset if they are not in the usual place) = \033[91m{h_cod_rem}\033[0m")
    def conf_ctr():
        # print("(4) \"Columns which will be removed from data\":", col_to_rem)
        if not col_to_rem:
            print("(4) Columns which will be removed from data: \033[91m No columns to remove \033[0m ( [] )")
        else:
            print("(4) Columns which will be removed from data:\n[")
            for n, col in enumerate(col_to_rem):
                print(f"  '" + "\033[96m" + col + "\033[0m" + f"'{',' if n+1 < len(col_to_rem) else ''}")
            print("]")

    conf_mkfile()
    print()
    conf_cvf()
    print()
    conf_hcr()
    print()
    conf_ctr()
    print()

    while not confimed:

        o = input("\nTo confirm this configuration press Enter - to modify " +
                  "element write numer and press Enter ('h' to write all) >>> ").strip()

        if o:
            __clean()
            match o:
                case "1":
                    mk_file = __ask_menu(conf_mkfile, mk_file)
                    print("\nAfter change:")
                    conf_mkfile()
                case "2":
                    cov_val_fl = __ask_menu(conf_cvf, cov_val_fl)
                    print("\nAfter change:")
                    conf_cvf()
                case "3":
                    h_cod_rem = __ask_menu(conf_hcr, h_cod_rem)
                    print("\nAfter change:")
                    conf_hcr()
                case "4":
                    while True:
                        conf_ctr()
                        print()
                        odp = input("Choose what do you want to do:\n" +
                                    "r - remove physical data\n" +
                                    "d - set value to default (no columns removed)\n" +
                                    "u - upload config from file\n" +
                                    "w - write names manually\n\n" +
                                    ">>> ").strip().lower()
                        print()
                        if odp == "d":
                            col_to_rem = [] ; break
                        elif odp == "r":
                            col_to_rem = to_remove ; break
                        elif odp == "u":
                            input("You have to select '.txt' file which has names " +
                                  "of all columns which you want to remove in separate " +
                                  "lines\n\nPress Enter to find a File >>> ")
                            file = filedialog.askopenfilename(
                                filetypes=[("Text file", "*.txt")])
                            try:
                                f = open(file)
                                col_to_rem = [a.strip() for a in f.readlines()]
                                f.close()
                                break
                            except KeyError as e:
                                print(f"Data read failed - {e}")
                        elif odp == "w":
                            print("Write name of each column in new line. Pressing Enter " +
                                  "in empty line will save result")
                            tmp = []
                            while True:
                                ans = input(">>> ").strip()
                                if ans: tmp.append(ans)
                                else:
                                    col_to_rem = tmp
                                    break
                            break
                    print("\nAfter change:")
                    conf_ctr()                           
                case "h":
                        print("\nAll current configuration\n\n")
                        conf_mkfile()
                        print()
                        conf_cvf()
                        print()
                        conf_hcr()
                        print()
                        conf_ctr()
                        print()
        else:
            confimed = True

    return mk_file, cov_val_fl, h_cod_rem, col_to_rem


def __multiple_file_processing(data_to_process, mk_file, cov_val_fl, h_cod_rem, 
                               col_to_rem, processed_size, sum_of_sizes, v,
                               directory_choosen : str = ""):
    for elem in data_to_process:
        file_name, file_path, size = elem.values()
        save_dir = directory_choosen if directory_choosen else file_path
        print(f"Processing '{file_name}' ...")
        try:
            file = open(file_path + sign + file_name)
            csvreader = list(csv.reader(file))
            race_data, processed_file = prepare_data(csvreader, mk_file, v, cov_val_fl, h_cod_rem, col_to_rem)
            save_data_csv_coma_format(processed_file,race_data['log_date'], race_data['log_time'], save_dir)
            processed_size += size
            print(f"File '{file_name}' processed - progress {processed_size/sum_of_sizes:.1%}\n")
        except Exception as e:
            print(f"\033[91m Couldn't process file {file_name} - {e}\033[0m")
            odp = input(r"Do you want to continue? [y\N] ")
            if odp == "n": break


def option1(v : bool):

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
    root.destroy()

    __clean()
    if v:
        print(f"\nYou've choosen file {file_path.split(sign)[-1]}")
        print(f"Full path to file {file_path}")

    mk_file, cov_val_fl, h_cod_rem, col_to_rem = __interactive_config()

    __clean()

    ans = input(r"Do you want to store file in the same place as the oryginal file? [y\n] >>> ")
    ans = ans.strip().lower()
    path = sign.join(file_path.split(sign)[0:-1])
    if ans == 'n':
        path = filedialog.askdirectory(mustexist=True, initialdir=path)

    __clean()

    print("Processing file ...")

    file = open(file_path)
    csvreader = list(csv.reader(file))

    race_data = processed_file = None

    try:
        race_data, processed_file = prepare_data(csvreader, v, cov_val_fl, h_cod_rem, col_to_rem)
    except KeyError as e:
        print(f"\033[91mOperation failed: {e}\033[0m")
        input("\nPress Enter to go back to main menu >>> ")
        return
    
    try:
        if mk_file:
            new_file = f"{path}/data_information_{race_data['log_date'].replace('-','_')}_{race_data['log_time'].replace(':','_')}.txt"
            
            if v:
                print(f"Creting file '{new_file}'")

            new_file = open(new_file, "w")
            ts = __display_track_summary(race_data,race_data['laps_start_end'])

            if v:
                print("Printing all information from the file:\n")
                new_file.write(ts)
                print(ts,'\n')
            else:
                new_file.write(ts)
            
            new_file.close()

        save_data_csv_coma_format(processed_file,race_data['log_date'],race_data['log_time'], path)
    except Exception as e:
        print(f"\033[91mOperation failed: {e}\033[0m")
        input("\nPress Enter to go back to main menu >>> ")
        return

    input("\n\033[92mOperation finished\033[0m\n\nPress Enter to continue >>> ")

def option2(v : bool):
    __clean()
    mode = ''
    while True:
        odp = input("Choose if you want to run interactive mode (option 1 on " +
                    "repeat) or you want to make one settings for all files\n\n" + 
                "\033[95mi - interactive mode (set params to all files individually)\033[0m\n" +
                "\033[96mg - generall (set once, run for all)\033[0m\n\n>>> ").strip().lower()
        
        if odp == "i":
            mode = "i" ; break
        elif odp == "g":
            mode = "g" ; break

    __clean()

    match mode:
        case "i":
            while True:
                option1(v)
                __clean()
                a = input("Continue (press Enter) or Finish (write 'c' and Enter)\n\n>>> ")
                if a.strip().lower() == "c": break
        case "g":
            mk_file, cov_val_fl, h_cod_rem, col_to_rem = __interactive_config()

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

            __multiple_file_processing(data_to_process, mk_file, cov_val_fl, h_cod_rem, 
                               col_to_rem, processed_size, sum_of_sizes, v)
            
            input("\n\033[92mFile processing finished\033[0m\n\nPress Enter to go back to the menu >>> ")


def option3(v : bool):
    
    files_detected = None
    folder_choosen = False
    directory_choosen = ""

    while not folder_choosen:
        __clean()
        folder_choosen = True
        input("Press Enter to look for a directory from which you would like to process all files: >>> ")

        directory = filedialog.askdirectory(mustexist=True)
        
        if not directory:
            print("\033[91mNo directory was choosen !!!\033[0m")
            ans = input("Press Enter to return to menu or write 'r' and press " +
                        "Enter to try again >>> ").strip().lower()
            if ans == "r":
                folder_choosen = False
                break

        files = list(filter(lambda x: str(x).endswith(".csv"),list(os.listdir(directory))))
        
        if not files:
            print("\033[91mNo CSV files detected in directory !!!\033[0m")
            ans = input("Press Enter to return to menu or write 'r' and press " +
                        "Enter to try again >>> ").strip().lower()
            if ans == "r":
                folder_choosen = False
                break
    
        if v:
            for a in files:
                print(a)
            print()

        odp = input(fr"Detected {len(files)} files - proceed? [y\N] >>> ").strip().lower()
        if odp == "n": folder_choosen = False
        else:
            files_detected = files
            directory_choosen = directory

    __clean()

    mk_file, cov_val_fl, h_cod_rem, col_to_rem = __interactive_config()

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

    __multiple_file_processing(data_to_process, mk_file, cov_val_fl, h_cod_rem, 
                               col_to_rem, processed_size, sum_of_sizes, v, directory_choosen)
        
    input("\n\033[92mFile processing finished\033[0m\n\nPress Enter to go back to the menu >>> ")
                

def menu():

    verbose = False

    print("Welcome to data preparation program.\n")
    def hint():
        print("Here are the available options:")
        print("1 - modify specific file")
        print("2 - modify multiple files")
        print("3 - modify all files in specified directory")
        print("4 - toggle verbose option (all operation explicitly described - " +
            "off by default)")
        print("5 - exit", end = "\n")

    tmp = True

    while True:
        
        if tmp:
            hint()
            odp  = input("\nChoose option: ").strip().lower()
            tmp = False
        else:
            odp  = input("\nChoose option ('h' for hint): ").strip().lower()

        if len(odp) > 1:
            print("Given value is too long !!!")
            continue
        elif odp not in ["1","2","3","4","5","h"]:
            print("Given value is not an option !!!")
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
                        print("\nNow command will be executed with description")
                    else:
                        print("\nNow command won't executed with description")
                case "5":
                    break
                case "h":
                    hint()
                   
    print("Exiting app ...")
    exit()


if __name__ == "__main__":
    menu()
