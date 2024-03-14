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


def __display_track_summary(track_summary, laps_start_end, color : bool = False):
    """
    This is helper function - it is used to prepare, and return track data
    in readable form (to be stored in file or displayed in console)
    """

    ts = ''

    # line separator for clear display of data
    if color:
        ts += "General informaiton about data\n\n"
    else:
        ts += "General informaiton about data\n\n"

    # display all stats except laps data (displayed separately below)
    for stats in track_summary:
        if stats == 'beacon_makers' or stats == 'laps_start_end':
            continue
        if color:
            ts += f"\033[95m{stats.capitalize():20}\033[0m : " +\
                  f"{track_summary[stats]}\n"
        else:
            ts += f"{stats.capitalize():20} : {track_summary[stats]}\n"

    # line separator for clear display of data
    if color:
        ts += "\nLap times\n\n"
    else:
        ts += "\nLap times\n\n"

    # display each lap times
    for i in range(len(laps_start_end)):
        start, end = laps_start_end[str(i + 1)].values()
        if color:
            ts += f'\033[94mLap {(i + 1)}\033[0m : \033[92m{start:08.3f}' +\
            f'\033[0m - \033[96m{end:08.3f}\033[0m   =   ' +\
            f'\033[92m{(end - start):.3f}\033[0ms\n'
        else:
            ts += f'Lap {(i + 1)} : {start:08.3f} - {end:08.3f}   =   ' +\
                  f'{(end - start):.3f}s\n'
    
    ts.strip()

    return ts


def __extract_general_data(file_object, verbose : bool = False) -> dict:
    """
    This funciton is responsible for removal of first rows in data which are
    responsible for storage of additional informaiton such as car model,
    track, name, distance. Those data are removed from the initial table but 
    can later be accessed via external variable
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
        print(__display_track_summary(track_summary, laps_start_end, True))
        
    return track_summary


def __remove_unnecessary_rows(file_object, hard_coded : bool = True, 
                              verbose : bool = False):
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
                    print("\033[93mRemoving row \033[96m", end = "")
                    ending = " ..." if len(str(row)) > 67 else ""
                    print(f"{str(row)[:64]}" + "\033[0m" + ending)
                    counter += 1
                file_object.remove(row)
            else:

                # Skip names of columns
                if row[0] == "Time" : continue
                try:
                    float(row[0])
                except:
                    if verbose:
                        print("\033[93mRemoving row \033[96m", end = "")
                        ending = " ..." if len(str(row)) > 67 else ""
                        print(f"{str(row)[:64]}" + "\033[0m" + ending)
                        counter += 1
                    file_object.remove(row)

        if verbose:
            print("\033[93m" + f"\nRemoved {counter} rows from the table" + 
                  "\033[0m")

    # Hard-coded solution - less flexible but faster
    else:
        if verbose: 
            print("\033[93mRemoving first 14 rows from data\033[0m")
        file_object = file_object[14:]

        if verbose:
            print("\033[93mRemoving 2,3, and 4 row - first one is title : \033[0m\n")
            ending = " ..." if len(str(file_object[0])) > 76 else ""
            print("\033[94m" + str(file_object[0])[:76] + ending + "\033[0m", 
                  end = "")
        file_object.pop(1)
        file_object.pop(1)
        file_object.pop(1)
    
    return file_object


def __remove_unnecessary_colums(file_object, custom_to_remove : list, 
                                verbose : bool = False):
    """
    This function allows to remove columns from data
    """    

    if not custom_to_remove:
        if verbose:
            print("\033[93mNo colums to remove - data left untouched\033[0m")
        return file_object        

    columns_to_remove = [file_object[0].index(i) for i in custom_to_remove]

    if verbose:
        print("\033[93mThe following columns will be removed:\033[0m")
        for i in range(len(to_remove)):
            print("\033[93m" + f"Column {columns_to_remove[i]}" + 
                  "\033[0m : \033[96m" + f"'{to_remove[i]}'" + "\033[0m")

    columns_to_remove = sorted(columns_to_remove, reverse=True)

    for row in range(len(file_object)):
        for col in columns_to_remove:
            file_object[row].pop(col)


    if verbose:
        print("\033[92m" + f"\nSuccessfully removed {len(to_remove)} columns" + 
              "\033[0m")

    return file_object


def __convert_values_to_float(file_object):
    """
    The purpose of this function is to convert all values to float (except
    first row)
    """

    for row in range(1,len(file_object)):
        if row:
            file_object[row] = list(map(float, file_object[row]))

    return file_object


def __even_out_comma_notation_str(file_object):
    """
    This funciton is responsible for converting each value into 'number float';
    It allows to process data in programs like Excel easily, but the result
    file is bigger, because everything is treated as text
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


def __fill_missing_lap_data(file_object, lap_info : list[list], 
                            verbose : bool = False):
    """
    This function fills out missing data.

    Currently it only fills missing laps
    """
    
    import math
    column = file_object[0].index('LAP_BEACON')

    lap = "1"
    last_time = lap_info[lap]['end']
    if verbose:
        print("\033[94m" + f"Filling out rows in lap " + "\033[0m\033[93m" + 
              f"{lap}" + "\033[0m")

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
                print("\033[94m" + f"Filling out rows in lap " + 
                      "\033[0m\033[93m" + f"{lap}" + "\033[0m")

    if verbose:
        print("\n\033[92mFilling out rows completed\033[0m")

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
    if verbose: print("-" * 80 + "\n")
    race_info = __extract_general_data(file_object, verbose)

    if verbose: print("-" * 80 + 
                      "\n\nRemoving unnecessary data from oryginal data " +
                      "(don't impact source file)\n")
    file_object = __remove_unnecessary_rows(file_object, hard_codec_row_removal,
                                            verbose)
    
    if verbose:
        print("\n\n" + "-" * 80 + "\n\nRemoving columns\n")
    file_object =__remove_unnecessary_colums(file_object, column_remove_list, 
                                             verbose)
    
    if verbose:
        print("\n" + "-" * 80 + "\n\nAdding missing data\n")
    file_object = __fill_missing_lap_data(file_object,
                                          race_info['laps_start_end'], 
                                          verbose)

    if convert_values_with_float_conversion:
        if verbose: print("\n" + "-" * 80 + "\n\nConverting values usign float " +
                          "funtion\n")
        file_object = __convert_values_to_float(file_object)
    else:
        if verbose: print("\n" + "-" * 80 + "\n\nConverting values by modyfing " +
                          "strings\n")
        file_object = __even_out_comma_notation_str(file_object)
    
    return race_info, file_object


def save_data_csv_coma_format(file_object, log_date : str, log_time : str, 
                              special_path : str):
    """
    This function is responsible for storage of modified file into a new file
    """
    import csv
    
    if special_path:
        file_path = f"{special_path}{sign}cleaned_data_" +\
                    f"{log_date.replace('-','_')}_{log_time.replace(':','_')}.csv"
    else:
        file_path = f"cleaned_data_{log_date.replace('-','_')}_" +\
                    f"{log_time.replace(':','_')}.csv"


    new_file = open(file_path,'w')

    csvwriter = csv.writer(new_file)
    csvwriter.writerows(file_object)

    new_file.close()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("This file contains functios, not CLI program :)\n")
    print("To open CLI program open run:\n")
    print(f"'python .{sign}File_preparation_CLI.py' or")
    print(f"'python3 .{sign}File_preparation_CLI.py' or")
    print(f"'python3.11 .{sign}File_preparation_CLI.py'\n")
    print("... depending the system you are using\n")