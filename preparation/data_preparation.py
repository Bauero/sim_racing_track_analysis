"""
This file contains funcitons which would allow to help clean csv files exported
from Motec software. By default this file can be use as a standalone app, but
it can be run by external program
"""


import csv
import json
from preparation.constants import sections, sign
from preparation.race_data_extraction_display import extract_general_data
from preparation.additional_commands import c_blue, c_green, c_cyan, c_yellow, \
                                            clean


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


def __remove_unnecessary_colums(file_object, 
                                columns_to_remove : list, 
                                verbose : bool = False):
    """
    This function allows to remove columns from data
    """    

    if not columns_to_remove:
        if verbose:
            print(c_yellow("No colums to remove - data left untouched"))
        return file_object        

    columns_to_remove = [file_object[0].index(i) for i in columns_to_remove]

    if verbose:
        print(c_yellow("The following columns will be removed:"))
        for i in range(len(columns_to_remove)):
            print(c_yellow(f"Column {i}") + " : " +\
                  c_cyan(f"'{columns_to_remove[i]}'"))

    columns_to_remove = sorted(columns_to_remove, reverse=True)

    for row in range(len(file_object)):
        for col in columns_to_remove:
            file_object[row].pop(col)

    if verbose:
        print(c_green(f"\nSuccessfully removed {len(columns_to_remove)} columns"))

    return file_object


def __convert_values_to_float(file_object):
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


def __add_time_distance_on_lap(file_object,
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
            dst = file_object[row][DISTANCE]
            if not values_in_float: dst = dst.replace(",",".")
            distance_offset = float(dst)
            if verbose:
                print(c_blue("Adding relative time and distance on lap ") + 
                      c_yellow(f"{int(lfdf)}"))

        if values_in_float:
            try: 
                tol = round(float(file_object[row][TIME]) - time_offset, 3)
            except ValueError:
                tol = round(float(file_object[row][TIME].replace(",",".")) - \
                            time_offset, 3)
            
            try:  dol = round(float(file_object[row][DISTANCE]) - \
                            distance_offset, 3)
            except ValueError:
                dol = round(float(file_object[row][DISTANCE].replace(",",".")) - \
                            distance_offset, 3)
       
        else:
            tol = str(round(
                float(file_object[row][TIME].replace(",",".")) - time_offset,
                3)).replace(".",",")
            dol = str(round(
                    float(file_object[row][DISTANCE].replace(",",".")) - \
                          distance_offset, 3)).replace(".",",")

        file_object[row].insert(TIME_ON_LAP,tol)
        file_object[row].insert(DISTANCE_ON_LAP,dol)

    return file_object


def __add_sections(file_object,
                               lap_info,
                               values_in_float,
                               verbose):
    """
    This funcition is responible for adding section columns after 'LAP_BEACON'
    """


    LAP_BEACON = file_object[0].index('LAP_BEACON')
    SECTION = LAP_BEACON + 1
    DISTANCE_ON_LAP = file_object[0].index('Distance_on_lap')

    current_section = "1"
    current_lap = int(float(file_object[1][LAP_BEACON].replace(",",".")))
    section_end = sections[current_section]["end"]
    file_object[0].insert(SECTION,"Section")

    if verbose: print(c_blue("\nAdding sections for lap ") + c_yellow('1'))

    for row in range(1, len(file_object)):
        if values_in_float:
            dist_on_lap = float(file_object[row][DISTANCE_ON_LAP])
            lap_in_row = file_object[row][LAP_BEACON]
        else:
            dist_on_lap = float(
                file_object[row][DISTANCE_ON_LAP].replace(",","."))
            lap_in_row = float(file_object[row][LAP_BEACON].replace(",","."))
        
        # For every new lap
        if int(lap_in_row) > current_lap:
            cls = file_object[row][LAP_BEACON]
            if not values_in_float: cls = float(cls.replace(",","."))
            current_lap = int(cls)
            current_section = "1"
            section_end = sections[current_section]["end"]

            if verbose:
                print(c_blue("Adding sections for lap ") +\
                      c_yellow(f"{current_lap}"))

        # For every new section
        if dist_on_lap > section_end:
            current_section = str(int(current_section) + 1)
            section_end = sections[current_section]["end"]

        file_object[row].insert(SECTION,
                                current_section if not values_in_float else \
                                int(current_section))
        
    return file_object


def __add_additional_columns(file_object,
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

    file_object = __add_time_distance_on_lap(file_object, 
                                             lap_info, 
                                             values_in_float,
                                             verbose)

    # Adding column to indicate which section is driver in

    file_object = __add_sections(file_object,
                                 lap_info,
                                 values_in_float,
                                 verbose)

    if verbose: print(c_green("\nAdding new columns completed\n"))

    return file_object


##############################  PUBLIC FUNCITONS  ##############################


def prepare_data(file_path, verbose : bool = False,
                 convert_values_with_float_conversion : bool = True,
                 hard_codec_row_removal : bool = True,
                 column_remove_list : list = [],
                 delim : str = ','):
    """
    This is general function which is responsible for data preparation

    This function returns race informaiton in form of a dictionary
    """

    try:
        file = open(file_path)
        file_object = list(csv.reader(file, delimiter=delim))
    except FileNotFoundError:
        return None, None  

    # Initial file processing

    if verbose: print("-" * 80 + "\n")
    race_info = extract_general_data(file_object, verbose)

    if verbose: print("-" * 80 + 
                      "\n\nRemoving unnecessary data from oryginal data " +
                      "(don't impact source file)\n")
    file_object = __remove_unnecessary_rows(file_object, 
                                            hard_codec_row_removal,
                                            verbose)
    
    if verbose:
        print("\n\n" + "-" * 80 + "\n\nRemoving columns\n")
    file_object = __remove_unnecessary_colums(file_object,
                                              column_remove_list, 
                                              verbose)

    # Fill out missing values

    if verbose:
        print("\n" + "-" * 80 + "\n\nFilling out empty cells with zeros\n")

    for row in range(1,len(file_object)):
        if convert_values_with_float_conversion:
            file_object[row] = [x if x != '' else 0.0 for x in file_object[row]]
        else:
            file_object[row] = [x if x != '' else "0" for x in file_object[row]]

    if verbose:
        print(c_green("Filling complete"))

    # Convert values according to the setting

    if convert_values_with_float_conversion:
        if verbose: print("\n" + "-" * 80 + "\n\nConverting values usign " + 
                        "float funtion")
        file_object = __convert_values_to_float(file_object)
    else:
        if verbose: print("\n" + "-" * 80 + "\n\nConverting values by " + 
                        " modyfing strings")
        file_object = __even_out_comma_notation_str(file_object)
    
    if verbose:
        print(c_green("\nConverting complete"))

    # Add additional columns

    if verbose:
        print("\n" + "-" * 80 + "\n\nAdding additional data\n")

    file_object = __add_additional_columns(file_object,
                                     race_info['laps_start_end'], 
                                     convert_values_with_float_conversion,
                                     verbose)
    
    return race_info, file_object        


def return_formatted_date_and_time(race_data):
    time, date = race_data["log_time"], race_data["log_date"]

    time = time.replace("/","-").replace("\\","-").replace(":","-")
    date = date.replace(".","-").replace("/","-")

    return time, date


def prepare_data_combined(file_path, verbose : bool = False,
                 convert_values_with_float_conversion : bool = False,
                 hard_codec_row_removal : bool = True,
                 column_remove_list : list = [],
                 delim : str = ','):
    """
    This funciton does the same things as prepare_data, however it does all
    operations in one loop, so it should run faster ...
    
    except, that it doesn' - most likely due to checking all rows, every time. 
    Nevertheless, instead of 1.40s it averages around 2.15s which is a shame
    for me and the time spend on this. Hovever, I leave it here, as a form of
    tl;dr for ppl which prefer to see one funciton does all the work, instead of
    jumping between calls

    PS. funciton works, but I never use it as it's slower
    """

    try:
        file = open(file_path)
        file_object = list(csv.reader(file, delimiter=delim))
    except FileNotFoundError:
        return None, None

    if verbose: print("-" * 80 + "\n")
    race_info = extract_general_data(file_object, verbose)

    new_file_object = []
    current_lap = 1
    laps_start_end = race_info["laps_start_end"]
    current_lap_end = race_info["laps_start_end"]["1"]["end"]
    time_offset = 0
    distance_offset = 0
    section = 1
    section_end = sections[str(section)]["end"]

    columns_to_avoid = []

    for row in file_object:

        if row == []: continue
        if len(row) < 10: continue
        if row[0] == "s": continue
        if row[0] == "Time":
            title_row = ["Time", "Time_on_lap",
                        "Distance", "Distance_on_lap",
                        "LAP_BEACON", "Section"]
            for c in row[::-1]:
                if c in set(title_row + column_remove_list):
                    index = row.index(c)
                    columns_to_avoid.append(index)
                    row.pop(index)

            title_row += row

            new_file_object.append(title_row)
            continue

        time = row[0]
        distance = row[1]
        
        # If row contains values in str
        if type(time) == str:
            time = round(float(time.replace(",",".")), 3)
        if type(distance) == str:
            distance = int(float(distance.replace(",",".")))

        # Reset lap
        if current_lap_end < time:
            current_lap += 1
            section = 1
            time_offset = time
            distance_offset = distance
            current_lap_end = laps_start_end[str(current_lap)]["end"]

        time_on_lap = round(time - time_offset, 3)
        distance_on_lap = int(distance - distance_offset)

        # Reset section
        if distance_on_lap > section_end:
            section += 1
            section_end = sections[str(section)]["end"]

        new_row = [time, time_on_lap, distance, distance_on_lap, 
                current_lap, section]
        
        if not convert_values_with_float_conversion:
            new_row = [str(v).replace(".",",") for v in new_row]
        
        for c in columns_to_avoid:
            row.pop(c)

        for element in row:
            if element == "":
                new_row.append(0 if convert_values_with_float_conversion 
                                else "0")
            elif convert_values_with_float_conversion:
                if "," in element:
                    new_row.append(round(float(element.replace(",",".")), 3))
                elif "." in element:
                    new_row.append(round(float(element), 3))
                else:
                    new_row.append(int(element))
            else:
                new_row.append(element.replace(".",","))
        
        new_file_object.append(new_row)

    return race_info, new_file_object


def remove_laps(file_object, laps : list):
    """
    This funciton allows to specify laps which should be removed, if those laps
    contain poor results, and shouldn't be taken into account in further analysis
    """

    LAPS = file_object[0].index("LAP_BEACON")
    title_row = file_object[0]

    def laps_match(r):
        l = r[LAPS]
        if type(l) == str:
            l.replace(",",".")
        l = int(float(l))
        return not l in laps

    filtered_file = list(filter(laps_match, file_object[1:]))
    filtered_file.insert(0, title_row)

    return filtered_file


def save_data_csv(file_object,
                  race_data,
                  special_path : str,
                  save_to_excel_format : bool = False,
                  custom_cleaned_data_filename : str = "",
                  custom_data_summary_filename : str = ""):
    """
    This function is responsible for storage of modified file into a new file
    """
    if not (custom_cleaned_data_filename or custom_data_summary_filename):
        log_date, log_time = return_formatted_date_and_time(race_data)

    if not custom_cleaned_data_filename:
        track_data = f"{log_date}_{log_time}_cleaned_data.csv"
    else:
        track_data = custom_cleaned_data_filename

    if not custom_data_summary_filename:
        data_summary = f"{log_date}_{log_time}_race_data.json"
    else:
        data_summary = custom_cleaned_data_filename

    if special_path:
        track_data = f"{special_path}{sign}{track_data}"
        data_summary = f"{special_path}{sign}{data_summary}"

    with open(track_data,'w') as track_file:
        csv.writer(track_file, lineterminator="\n" ).writerows(file_object)

    with open(data_summary, 'w') as data_file:
        data_file.write(json.dumps(race_data))


if __name__ == "__main__":
    clean()
    print("This file contains functios, not CLI program :)\n")
    print("To open CLI program open run:\n")
    print(f"'python .{sign}File_preparation_CLI.py' or")
    print(f"'python3 .{sign}File_preparation_CLI.py' or")
    print(f"'python3.11 .{sign}File_preparation_CLI.py'\n")
    print("... depending the system you are using\n")
