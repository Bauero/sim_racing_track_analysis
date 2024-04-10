"""
This file contains funcitons which would allow to help clean csv files exported
from Motec software. By default this file can be use as a standalone app, but
it can be run by external program
"""


import os
import csv
from math import inf
from additional_commands import c_blue, c_green, c_pink, c_cyan, c_yellow

sign = '\\' if os.name == 'nt' else '/'
physical_columns  = ['SUS_TRAVEL_LF',
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
sections = {
    "1"	: {"name" : "Str 1",    "start" :   0,      "end" :	670},
    "2"	: {"name" : "Turn 1",   "start" :	670,    "end" :	900},
    "3"	: {"name" : "Turn 2",   "start" :	900,    "end" :	990},
    "4"	: {"name" : "Str 2-3",  "start" :	990,    "end" :	1030},
    "5"	: {"name" : "Turn 3",   "start" :	1030,   "end" :	1330},
    "6"	: {"name" : "Str 3-4",  "start" :	1330,   "end" :	1580},
    "7"	: {"name" : "Turn 4",   "start" :	1580,   "end" :	1880},
    "8"	: {"name" : "Str 4-5",  "start" :	1880,   "end" :	2000},
    "9"	: {"name" : "Turn 5",   "start" :	2000,   "end" :	2200},
    "10": {"name" : "Str 5-6",  "start" :	2200,   "end" :	2430},
    "11": {"name" : "Turn 6",   "start" :	2430,   "end" :	2580},
    "12": {"name" : "Str 6-7",  "start" :	2580,   "end" :	2770},
    "13": {"name" : "Turn 7",   "start" :	2770,   "end" :	2980},
    "14": {"name" : "Str 7-8",  "start" :	2980,   "end" :	3310},
    "15": {"name" : "Turn 8",   "start" :	3310,   "end" :	3520},
    "16": {"name" : "Str 8-9",  "start" :	3520,   "end" :	3530},
    "17": {"name" : "Turn 9",   "start" :	3530,   "end" :	3620},
    "18": {"name" : "Turn 10",  "start" :	3620,   "end" :	3840},
    "19": {"name" : "Str 10-11","start" :   3840,   "end" :	3880},	
    "20": {"name" : "Turn 11",  "start" :	3880,   "end" :	4020},
    "21": {"name" : "Turn 12",  "start" :	4020,   "end" :	4120},
    "22": {"name" : "Turn 13",  "start" :	4120,   "end" :	4200},
    "23": {"name" : "Turn 14",  "start" :	4200,   "end" :	4400},
    "24": {"name" : "Str 14-0", "start" :	4400,   "end" :	inf}
}


#############################  INTERNAL FUNCITONS  #############################


def __remove_unnecessary_rows(file_object, hard_coded : bool = True, 
                              verbose : bool = False):
    """
    This function is calles to remove data which are not important in our 
    program aka. empty rows, or rows which contains not important information 
    [like units]

    Function contains two different solutions. By default (hard_coded == True)
    function would simply erase all 14 first rows (leaving first row as titles)
    and then remove rows 2-4 which contains units and 2 empty rows. However any
    changes to rows, as well as empty rows wouldn't be detected. 
    
    Therefore one can run this function with option 'hard_coded' set to False.
    Then function will automatically parse file to remove any empty rows and 
    rows which are not column's title's row (the one, which in first column has 
    'Time' value)
    """

    if not hard_coded:
        if verbose: counter = 0

        for row in range(len(file_object) - 1,-1,-1):
        
            row = file_object[row]

            # remove all empty rows
            if row == []:
                if verbose:
                    ending = " ..." if len(str(row)) > 67 else ""
                    print(c_yellow(f"Removing row {str(row)[:64]}") + ending)
                    counter += 1
                file_object.remove(row)
            else:

                # Skip names of columns
                if row[0] == "Time" : continue
                try:
                    float(row[0])
                except:
                    if verbose:
                        ending = " ..." if len(str(row)) > 67 else ""
                        print(c_yellow(f"Removing row {str(row)[:64]}") + \
                               ending)
                        counter += 1
                    file_object.remove(row)

        if verbose:
            print(c_yellow(f"\nRemoved {counter} rows from the table"))

    # Hard-coded solution - less flexible but faster
    else:
        if verbose: 
            print(c_yellow("Removing first 14 rows from data"))
        file_object = file_object[14:]

        if verbose:
            print(c_yellow("Removing 2,3, and 4 row - first one is title : \n"))
            ending = " ..." if len(str(file_object[0])) > 76 else ""
            print(c_blue(str(file_object[0])[:76] + ending), end = "")

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
            print(c_yellow("No colums to remove - data left untouched"))
        return file_object        

    columns_to_remove = [file_object[0].index(i) for i in custom_to_remove]

    if verbose:
        print(c_yellow("The following columns will be removed:"))
        for i in range(len(physical_columns)):
            print(c_yellow(f"Column {columns_to_remove[i]}") + " : " +\
                  c_cyan(f"'{physical_columns[i]}'"))

    columns_to_remove = sorted(columns_to_remove, reverse=True)

    for row in range(len(file_object)):
        for col in columns_to_remove:
            file_object[row].pop(col)


    if verbose:
        print(c_green(f"\nSuccessfully removed {len(physical_columns)} columns"))

    return file_object


def convert_values_to_float(file_object):
    """
    The purpose of this function is to convert all values to float (except
    first row)
    """

    for row in range(1,len(file_object)):
        new_row = []
        for value in file_object[row]:
            try: new_row.append(float(value))
            except ValueError: new_row.append(float(value.replace(",",".")))
        file_object[row] = new_row

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


def __add_missing_laps_numbers(file_object,
                       lap_info,
                       verbose):
    """
    This function is responible for adding appriopriate number of lap into 
    'LAP_BEACON' column, based on 'BEACONS_MAREKRS'
    """


    LAP_BEACON = file_object[0].index('LAP_BEACON')
    TIME = file_object[0].index('Time')
    
    lap = "1"
    last_time = lap_info[lap]['end']
    if verbose:
        print(c_blue(f"Adding row numbers for lap ") + c_yellow(f"{lap}"))
    
    curr_time = None

    for row in range(1,len(file_object)):

        try: curr_time = float(file_object[row][TIME])
        except ValueError: 
            curr_time = float(file_object[row][TIME].replace(",","."))

        if curr_time <= last_time:
            file_object[row][LAP_BEACON] = lap
        else:
            lap = str(int(lap) + 1)
            last_time = lap_info[lap]['end']
            file_object[row][LAP_BEACON] = lap
            if verbose:
                print(c_blue("Adding row numbers for lap ") + \
                      c_yellow(f"{lap}"))


    return file_object


def __add_data_for_each_lap(file_object,
                            lap_info,
                            values_in_float,
                            verbose):
    """
    This funciton is responible for adding 2 important columns - 'Time_on_lap'
    and 'Distance_on_lap'. 
    """


    LAP_BEACON = file_object[0].index('LAP_BEACON')
    TIME = file_object[0].index('Time')
    TIME_ON_LAP = TIME + 1
    DISTANCE = file_object[0].index('Distance')
    DISTANCE_ON_LAP = DISTANCE + 1 + (TIME < DISTANCE)

    distance_offset = 0.0
    time_offset = 0.0
    current_lap = 1

    file_object[0].insert(TIME_ON_LAP,"Time_on_lap")
    file_object[0].insert(DISTANCE_ON_LAP,"Distance_on_lap")
    full_laps = list(lap_info.keys())

    if verbose:
        print(c_blue("\nAdding relative time and distance on lap ") + 
              c_yellow("1"))

    for row in range(1, len(file_object)):
        lap_from_data = file_object[row][LAP_BEACON]
        
        try: lfdf = float(lap_from_data)
        except ValueError:
            lfdf = float(lap_from_data.replace(",","."))

        if lfdf > current_lap:
            current_lap = lfdf
            if lap_from_data in full_laps:
                time_offset = lap_info[lap_from_data]["start"]
            else:
                time_offset = lap_info[str(int(lfdf-1))]["end"]
            distance_offset = float(file_object[row][DISTANCE])
            if verbose:
                print(c_blue("Adding relative time and distance on lap ") + 
                      c_yellow(f"{int(lfdf)}"))


        try: tol = round(float(file_object[row][TIME]) - time_offset, 3)
        except ValueError:
            tol = round(float(file_object[row][TIME].replace(",",".")) - \
                        time_offset, 3)
        
        try:  dol = round(float(file_object[row][DISTANCE]) - \
                          distance_offset, 3)
        except ValueError:
            dol = round(float(file_object[row][DISTANCE].replace(",",".")) - \
                        distance_offset, 3)
       
        if not values_in_float:
            tol = f"{tol}"
            dol = f"{dol}"

        file_object[row].insert(TIME_ON_LAP,tol)
        file_object[row].insert(DISTANCE_ON_LAP,dol)

    return file_object


def __add_sections_and_analyze(file_object,
                               lap_info,
                               values_in_float,
                               verbose):
    """
    This funcition is responible for adding section columns after 'LAP_BEACON' 
    and measuring other statistics, like min, max and average speed on each
    section, and for best section accross all laps. Additionally, function
    returns also section data, for best lap
    """


    LAP_BEACON = file_object[0].index('LAP_BEACON')
    SECTION = LAP_BEACON + 1
    TIME = file_object[0].index('Time')
    DISTANCE_ON_LAP = file_object[0].index('Distance_on_lap')

    current_section = "1"
    current_lap = int(float(file_object[1][LAP_BEACON]))
    section_end = sections[current_section]["end"]
    file_object[0].insert(SECTION,"Section")

    data_all_laps = { "1" : {  "1" : {}  } }

    best_time_section = {k : {"best_time" : inf} for k in sections.keys()}
    time_per_lap = {
        k : lap_info[k]["end"] - lap_info[k]["start"] for k in lap_info.keys()
    }

    best_time_lap = sorted(list(time_per_lap.items()), key = lambda x : x[1])[0]

    speeds_in_section = []
    sp_col = file_object[0].index("SPEED")-1
    start_time_section = 0

    def __update_speeds(start_time_section, 
                        speeds_in_section,
                        data_all_laps,
                        current_lap,
                        current_section
                        ):
        
        section_max = max(speeds_in_section)
        section_min = min(speeds_in_section)
        section_avg = round(sum(speeds_in_section) / len(speeds_in_section),
                                2)

        scl = str(current_lap)

        data_all_laps[scl][current_section]["max"] = section_max
        data_all_laps[scl][current_section]["min"] = section_min
        data_all_laps[scl][current_section]["avg"] = section_avg

        speeds_in_section = []

        time_in_row = round((float(file_object[row][TIME]) + \
                        float(file_object[row-1][TIME])) / 2, 4)
        time_diff = round(time_in_row - start_time_section, 4)
        
        if time_diff < best_time_section[current_section]["best_time"]:
            best_time_section[current_section]["best_time"] = time_diff
            best_time_section[current_section]["max"] = section_max
            best_time_section[current_section]["min"] = section_min
            best_time_section[current_section]["avg"] = section_avg
            start_time_section = time_in_row

    if verbose:
        print(c_blue("\nAdding sections for lap ") + c_yellow('1'))

    for row in range(1, len(file_object)):
        dist_on_lap = float(file_object[row][DISTANCE_ON_LAP])
        speed = float(file_object[row][sp_col])
        lap_in_row = file_object[row][LAP_BEACON]
        
        # For every new lap

        if int(lap_in_row) > current_lap:

            __update_speeds(start_time_section, 
                            speeds_in_section,
                            data_all_laps,
                            current_lap,
                            current_section
                            )

            cls = file_object[row][LAP_BEACON]
            current_lap = int(cls)

            current_section = "1"
            section_end = sections[current_section]["end"]

            data_all_laps[str(current_lap)] = {
                "1" : {}
            }

            if verbose:
                print(c_blue("Adding sections for lap ") +\
                      c_yellow(f"{current_lap}"))

        # For every new section

        if dist_on_lap > section_end:

            __update_speeds(start_time_section, 
                            speeds_in_section,
                            data_all_laps,
                            current_lap,
                            current_section
                            )

            current_section = str(int(current_section) + 1)
            section_end = sections[current_section]["end"]

            data_all_laps[str(current_lap)][current_section] = {}

        speeds_in_section.append(speed)
        file_object[row].insert(SECTION,
                                current_section if not values_in_float else \
                                int(current_section))
    else:
        __update_speeds(start_time_section, 
                        speeds_in_section,
                        data_all_laps,
                        current_lap,
                        current_section
                        )

    data_for_best_lap = {best_time_lap[0] : data_all_laps[best_time_lap[0]]}

    return file_object, data_all_laps, data_for_best_lap, best_time_section


def __fill_missing_data(file_object,
                            lap_info : dict[dict], 
                            values_in_float : bool,
                            verbose : bool = False):
    """
    This function fills out missing data. It should contain other functions
    which directly puts additioal columns, or modify exising ones (except 
    removing them - this is done ealier)
    """

    # Adding missing lap numbers

    file_object = __add_missing_laps_numbers(file_object, 
                                             lap_info, 
                                             verbose)

    # Adding additional columsn - Time_on_lap and Distance_on_lap

    file_object = __add_data_for_each_lap(file_object, 
                                          lap_info, 
                                          values_in_float,
                                          verbose)

    # Adding column to indicate which section is driver in

    values = __add_sections_and_analyze(file_object,
                                        lap_info,
                                        values_in_float,
                                        verbose)

    file_object, data_all_laps, data_for_best_lap, best_time_section = values

    if verbose:
        print(c_green("\nAdding new columns completed"))

    return file_object, data_all_laps, data_for_best_lap, best_time_section


##############################  PUBLIC FUNCITONS  ##############################


def display_track_summary(track_summary, laps_start_end, color : bool = False):
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
            ts += c_pink(f"{stats.capitalize():20}") + \
                 " : "  +  f"{track_summary[stats]}\n"
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
            ts += c_blue(f'Lap {(i + 1)}')        + ' : ' +\
                  c_green(f'{start:08.3f}')       + ' - ' + \
                  c_cyan(f'{end:08.3f}')          + '   =   ' +\
                  c_green(f'{(end - start):.3f}') + '\n'
        else:
            ts += f'Lap {(i + 1)} : {start:08.3f} - {end:08.3f}   =   ' +\
                  f'{(end - start):.3f}s\n'
    
    ts.strip()

    return ts


def extract_general_data(file_object, verbose : bool = False) -> dict:
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
        laps_start_end[str(i + 1)] = {"start" : tmp_start, 
                                      "end" : beacon_makers[i]}
        tmp_start = beacon_makers[i]
    else:
        if float(track_summary['end_time']) > float(beacon_makers[-1]):
            laps_start_end[str(i + 2)] = {"start" : beacon_makers[i], 
                                    "end" : float(track_summary['end_time'])}
    track_summary['laps_start_end'] = laps_start_end

    # Display informaiton in the console if 'verbose' param set to 'True'

    if verbose:
        print(display_track_summary(track_summary, laps_start_end, True))
        
    return track_summary


def prepare_data(file_object, verbose : bool = False,
                 convert_values_with_float_conversion : bool = False,
                 hard_codec_row_removal : bool = True,
                 column_remove_list : list = physical_columns,
                 ):
    """
    This is general function which is responsible for data preparation

    This function returns race informaiton in form of a dictionary
    """
    if verbose: print("-" * 80 + "\n")
    race_info = extract_general_data(file_object, verbose)

    if verbose: print("-" * 80 + 
                      "\n\nRemoving unnecessary data from oryginal data " +
                      "(don't impact source file)\n")
    file_object = __remove_unnecessary_rows(file_object, hard_codec_row_removal,
                                            verbose)
    
    if verbose:
        print("\n\n" + "-" * 80 + "\n\nRemoving columns\n")
    file_object =__remove_unnecessary_colums(file_object, column_remove_list, 
                                             verbose)

    # Fill out missing values

    for row in range(1,len(file_object)):
        if convert_values_with_float_conversion:
            file_object[row] = [x if x != '' else 0.0 for x in file_object[row]]
        else:
            file_object[row] = [x if x != '' else "0" for x in file_object[row]]

    if convert_values_with_float_conversion:
        if verbose: print("\n" + "-" * 80 + "\n\nConverting values usign float " +
                          "funtion\n")
        file_object = convert_values_to_float(file_object)
    else:
        if verbose: print("\n" + "-" * 80 + "\n\nConverting values by modyfing " +
                          "strings\n")
        file_object = __even_out_comma_notation_str(file_object)
    
    if verbose:
        print("\n" + "-" * 80 + "\n\nAdding missing data\n")

    values = __fill_missing_data(file_object,
                                     race_info['laps_start_end'], 
                                     convert_values_with_float_conversion,
                                     verbose)
    file_object, data_all_laps, data_for_best_lap, best_time_section = values
    
    return race_info, data_all_laps, data_for_best_lap, best_time_section, \
            file_object


def save_data_csv_coma_format(file_object, log_date : str, log_time : str, 
                              special_path : str):
    """
    This function is responsible for storage of modified file into a new file
    """
    if special_path:
        file_path = f"{special_path}{sign}{log_date}_{log_time}_cleaned_data.csv"
    else:
        file_path = f"{log_date}_{log_time}_cleaned_data.csv"


    new_file = open(file_path,'w')

    csvwriter = csv.writer(new_file)
    csvwriter.writerows(file_object)

    new_file.close()


def save_laps_section_all_laps(path, data, title):
    
    f = open(f"{path}{sign}{title}.csv","w")
    file = csv.writer(f)
    file.writerow(["Lap","Section","Max","Min","Avg"])
    for lap in data:
        for section in data[lap]:
            file.writerow(
                [lap,
                section,
                str(data[lap][section]["max"]).replace(".",","),
                str(data[lap][section]["min"]).replace(".",","),
                str(data[lap][section]["avg"]).replace(".",",")])
    f.close()


def save_data_best_sections(path, data, title):
    
    f = open(f"{path}{sign}{title}.csv","w")
    file = csv.writer(f)
    file.writerow(["Section","Max","Min","Avg","Best Time"])
    for section in data:
        file.writerow(
            [section,
             str(data[section]["max"]).replace(".",","),
             str(data[section]["min"]).replace(".",","),
             str(data[section]["avg"]).replace(".",","),
             str(data[section]["best_time"]).replace(".",",")])
    f.close()


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    print("This file contains functios, not CLI program :)\n")
    print("To open CLI program open run:\n")
    print(f"'python .{sign}File_preparation_CLI.py' or")
    print(f"'python3 .{sign}File_preparation_CLI.py' or")
    print(f"'python3.11 .{sign}File_preparation_CLI.py'\n")
    print("... depending the system you are using\n")
