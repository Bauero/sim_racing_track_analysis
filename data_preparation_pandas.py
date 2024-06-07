"""
This file holds allows to perform data preparation using pandas library. It does
all the same things as '`data_preparation.py`'. However, everything is done
using pandas

WHY? - (tldr: alternative solution for practice)
pandas, as more advanded library, provides many tools and simple syntax. 
So, to learn new library, I've redo my solution using it. Therefore, there's no
other 'hidden' benefit to using this file that 'data_preparation.py' in file
preparation - moreover, from my experience, it seems that my custom solution 
seems to perform sligltly better than this implementation in Pandas. 
"""

import pandas as pd
import csv
import json
from constants import sign, sections
from additional_commands import clean
from race_data_extraction_display import *


#############################  INTERNAL FUNCITONS  #############################


def __remove_unnecessary_rows(df):
    df = df.drop(index=0)
    df = df.reset_index(drop=True)
    return df


def __remove_unnecessary_colums(df, columns_to_remove):

    columns_to_keep = df.columns
    for col in columns_to_remove:
        columns_to_keep.pop(col)
    df = df[columns_to_keep]
    return df


def __convert_values_to_float(df):

    def convert_if_needed(value):
        if type(value) == str:
            if "," in value:
                return float(value.replace(",","."))
        return value

    df = df.applymap(convert_if_needed)
    df = df.astype(float)
    return df


def __remove_nans(df):
    df = df.fillna(0.0)
    return df


def __add_lap_no(df, laps):
    def assign_lap(time):
        for lap, times in laps.items():
            if times["start"] <= time <= times["end"]:
                return lap
        return None

    df['LAP_BEACON'] = df['Time'].apply(assign_lap)
    return df


def __add_time_distance_on_lap(df, laps):
    distance_offset = 0.0
    time_offset = 0.0
    current_lap = 1

    def add_time_distance_on_lap(row):
        nonlocal distance_offset
        nonlocal time_offset
        nonlocal current_lap
        nonlocal laps
        
        time = row['Time']
        distance = row['Distance']
        lap = row['LAP_BEACON']
        
        if lap != current_lap:
            current_lap = lap
            distance_offset = distance
            time_offset = time

        track_time = round(time - time_offset,3)
        track_dist = round(distance - distance_offset,1)

        return track_time, track_dist

    df['Time_on_lap'], df['Distance_on_lap'] = \
        zip(*df.apply(add_time_distance_on_lap, axis=1))
    return df


def __add_sections(df, sections):
    current_lap = 1
    current_section = 1
    max_for_section = sections["1"]["end"]

    def add_sections(row):
        nonlocal sections
        nonlocal current_lap
        nonlocal current_section
        nonlocal max_for_section

        distance = row['Distance_on_lap']
        lap = int(row['LAP_BEACON'])

        if lap > current_lap:
            current_section = 1
            current_lap = lap
            max_for_section =  sections[str(current_section)]["end"]
        if distance > max_for_section:
            current_section += 1
            max_for_section =  sections[str(current_section)]["end"]

        return current_section
        
    df['Section'] = df.apply(add_sections, axis=1)
    return df


def __reorder_columns(df):
    all_columns = list(df.columns)

    columns_from_left = ['Time', 'Time_on_lap', 'Distance','Distance_on_lap',  
            'LAP_BEACON', 'Section']

    for col in columns_from_left:
        all_columns.pop(all_columns.index(col))

    df = df.reindex(columns = columns_from_left + all_columns)
    return df


##############################  PUBLIC FUNCITONS  ##############################


def prepare_data(file_path, verbose : bool = False,
                 convert_values_with_float_conversion : bool = False,
                 hard_codec_row_removal : bool = True,
                 column_remove_list : list = [],
                 delim : str = ','):
    """
    This is general function which is responsible for data preparation

    This function returns race informaiton in form of df
    """

    try:
        with open(file_path) as file:
            file_object = list(csv.reader(file, delimiter=delim))
            race_info = extract_general_data(file_object, verbose)
    except FileNotFoundError:
        return None, None

    laps = race_info['laps_start_end']
    
    df = pd.read_csv(file_path, skip_blank_lines=True, skiprows=14)
    df = __remove_unnecessary_rows(df)
    df = __remove_unnecessary_colums(df, column_remove_list)
    df = __convert_values_to_float(df)
    df = __remove_nans(df)

    df = __add_lap_no(df, laps)
    df = __add_time_distance_on_lap(df, laps)
    df = __add_sections(df, sections)
    df = __reorder_columns(df)

    return race_info, df


def return_formatted_date_and_time(race_data):
    time, date = race_data["log_time"], race_data["log_date"]

    time = time.replace("/","-").replace("\\","-").replace(":","-")
    date = date.replace(".","-").replace("/","-")

    return time, date


def remove_laps(df, laps : list):
    laps = [str(l) for l in laps]
    rows_to_remove = df[df['LAP_BEACON'].isin(laps)].index
    df.drop(rows_to_remove, inplace=True)
    return df


def save_data_csv(file_object,
                  race_data,
                  special_path : str,
                  save_values_as_float : bool = True,
                  custom_cleaned_data_filename : str = "",
                  custom_data_summary_filename : str = ""):
    
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

    file_object.to_csv(track_data,
                       lineterminator = "\n",
                       decimal = "." if save_values_as_float else ',',
                       index=False)

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
