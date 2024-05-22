"""
This file would contain funcitons which are necessary to perform data analysis
of preprocessed file. If this file is run as an stanalone file, it expects you
to select directory in which there are located files with data. Files are 
expected to have names in form of '`data_time_cleaned_data.csv`'
"""

import csv
from constants import sections, inf, sign
from tkinter.filedialog import askdirectory


#############################  INTERNAL FUNCITONS  #############################


def __analyze_speed_time_per_seciton(file_object, values_in_float):
    """
    This funcition is responible for adding section columns after 'LAP_BEACON' 
    and measuring other statistics, like min, max and average speed on each
    section, and for best section accross all laps. Additionally, function
    returns also section data, for best lap
    """

    # Define variables with numbers of columns
    LAP_BEACON = file_object[0].index('LAP_BEACON')
    TIME = file_object[0].index('Time')
    DISTANCE_ON_LAP = file_object[0].index('Distance_on_lap')
    SPEED = file_object[0].index("SPEED")

    # Define auxiliary variables
    current_section = list(sections.keys())[0]
    current_lap = int(float(file_object[1][LAP_BEACON].replace(",",".")))
    section_end = sections[current_section]["end"]
    speeds_in_section = []
    start_time_section = 0
    start_time_lap = 0

    # Define variables for storing analysis data
    data_all_laps = {}
    best_time_lap = {'lap' : None , 'time' : inf}
    best_time_section = {k : {"best_time" : inf} for k in sections.keys()}

    # Lists that holds standard deviation for specific stats
    # x = ["std max", "std min", "std avg", "std time"]
    # std_of_variables = {k : {d : [] for d in x} for k in sections.keys()}
    std_of_variables = dict()
    for sec in sections.keys():
        std_of_variables[sec] = { 
            "std max": [],
            "std min": [],
            "std avg": [], 
            "std time": []
        }
    
    def current_time(values_in_float):
        if values_in_float:
            time_in_row = round((float(file_object[row][TIME]) + \
                            float(file_object[row-1][TIME])) / 2, 4)
        else:
            t1 = float(file_object[row][TIME].replace(",","."))
            t2 = float(file_object[row-1][TIME].replace(",","."))
            time_in_row = round((t1+t2)/2, 4)
        return time_in_row

    def update_best_time_lap():
        nonlocal current_lap
        curr_time = current_time(values_in_float)
        time_diff = curr_time - start_time_lap
        if time_diff < best_time_lap['time']:
            best_time_lap['time'] = time_diff
            best_time_lap["lap"] = current_lap

    def update_data_for_section():
        
        nonlocal start_time_section
        nonlocal speeds_in_section
        nonlocal current_section
        nonlocal current_lap

        # Calculate stats for the past section
        section_max = max(speeds_in_section)
        section_min = min(speeds_in_section)
        section_avg = round(sum(speeds_in_section) / len(speeds_in_section), 2)

        scl = str(current_lap)
        if not scl in data_all_laps.keys():
            data_all_laps[scl] = {}

        if not current_section in data_all_laps[scl].keys():
            data_all_laps[scl][current_section] = {}

        # Save stats for specific lap and seciton
        data_all_laps[scl][current_section]["max"] = section_max
        data_all_laps[scl][current_section]["min"] = section_min
        data_all_laps[scl][current_section]["avg"] = section_avg

        speeds_in_section = []
        
        # Calculate time, and update start_time_offset
        time_in_row = current_time(values_in_float)
        time_diff = round(time_in_row - start_time_section, 4)
        data_all_laps[scl][current_section]["time"] = time_diff
        start_time_section = time_in_row

        # If necessary, update stats for new fastest section
        if time_diff < best_time_section[current_section]["best_time"]:
            best_time_section[current_section]["best_time"] = time_diff
            best_time_section[current_section]["max"] = section_max
            best_time_section[current_section]["min"] = section_min
            best_time_section[current_section]["avg"] = section_avg
            best_time_section[current_section]["Lap"] = current_lap
        
        # Add section stats to appriopriate list
        std_of_variables[current_section]["std max"].append(section_max)
        std_of_variables[current_section]["std min"].append(section_min)
        std_of_variables[current_section]["std avg"].append(section_avg)
        std_of_variables[current_section]["std time"].append(time_diff)

    for row in range(1, len(file_object)):
        if values_in_float:
            dist_on_lap = float(file_object[row][DISTANCE_ON_LAP])
            speed = float(file_object[row][SPEED])
            lap_in_row = file_object[row][LAP_BEACON]
        else:
            dist_on_lap = float(
                file_object[row][DISTANCE_ON_LAP].replace(",","."))
            speed = float(file_object[row][SPEED].replace(",","."))
            lap_in_row = float(file_object[row][LAP_BEACON].replace(",","."))
        
        # For every new lap
        if int(lap_in_row) > current_lap:

            update_data_for_section()
            update_best_time_lap()

            cls = file_object[row][LAP_BEACON]
            if not values_in_float: 
                cls = float(cls.replace(",","."))
            current_lap = int(cls)

            current_section = "1"
            section_end = sections[current_section]["end"]

            data_all_laps[str(current_lap)] = {
                "1" : {}
            }

        # For every new section
        if dist_on_lap > section_end:

            update_data_for_section()

            current_section = str(int(current_section) + 1)
            section_end = sections[current_section]["end"]

            data_all_laps[str(current_lap)][current_section] = {}

        speeds_in_section.append(speed)
    else:
        update_data_for_section()
        update_best_time_lap()

    for sec in sections.keys():
        for std in std_of_variables[sec]:
            s = std_of_variables[sec][std]
            l = len(s)
            section_average = round(sum(s)/l, 2)
            sum_deviations = 0
            std_dev = 0
            if l > 1:
                for lap in s:
                    sum_deviations+=(lap - section_average)**2
                std_dev = (sum_deviations / (l-1))**0.5
            std_of_variables[sec][std]= round(std_dev, 2)
        
    fastest_lap = str(best_time_lap['lap'])
    data_for_best_lap = {fastest_lap : data_all_laps[fastest_lap]}

    return data_all_laps, data_for_best_lap, best_time_section, std_of_variables


def __save_laps_section_all_laps(path, data, title):
    
    f = open(f"{path}{sign}{title}.csv","w")
    file = csv.writer(f)
    file.writerow(["Lap","Section","Max Speed","Min Speed","Avg Speed","Time"])
    for lap in data:
        for section in data[lap]:
            file.writerow(
                [lap,
                section,
                str(data[lap][section]["max"]).replace(".",","),
                str(data[lap][section]["min"]).replace(".",","),
                str(data[lap][section]["avg"]).replace(".",","),
                str(data[lap][section]["time"]).replace(".",",")])
    f.close()


def __save_data_best_sections(path, data, title):
    
    f = open(f"{path}{sign}{title}.csv","w")
    file = csv.writer(f)
    file.writerow(["Lap","Section","Max Speed","Min Speed","Avg Speed", \
                   "Best Time"])
    for section in data:
        file.writerow(
            [str(data[section]["Lap"]).replace(".",","),
             section,
             str(data[section]["max"]).replace(".",","),
             str(data[section]["min"]).replace(".",","),
             str(data[section]["avg"]).replace(".",","),
             str(data[section]["best_time"]).replace(".",",")])
    f.close()


def __save_std_for_each_section(path, data, title):
    
    f = open(f"{path}{sign}{title}.csv","w")
    file = csv.writer(f)
    file.writerow(["Section","Std Max", "Std Min", "Std Avg", "Std Time"])
    for section in data:
        file.writerow(
            [section,
             str(data[section]["std max"]).replace(".",","),
             str(data[section]["std min"]).replace(".",","),
             str(data[section]["std avg"]).replace(".",","),
             str(data[section]["std time"]).replace(".",",")])
    f.close()


##############################  PUBLIC FUNCITONS  ##############################


def data_analysis(path_to_file, directory, date, time):
    """
    This funcion performs data analysis of provided file. 

    So far, analysis would result in creaton of 3 files:
    - '`all_laps`' - this file would contain max, min and average speed and time
    for every seciton
    - '`best_lap`' - this file would create subset of data of '`all_laps`', with
    data only for the fastest lap
    - '`best_section`' - this file would contain informaiton about best section
    from all laps in the data
    - '`std_each_section`' - this file would contain informaiton about standard
    defiation of max, min and average speed and time for every section based
    on the cleaned data - if data would contain only one lap, this file would 
    have only 0, as a value for each row in every column
    """

    file = open(path_to_file)
    file_object = list(csv.reader(file))

    val = __analyze_speed_time_per_seciton(file_object, True)
    data_all_laps, data_for_best_lap, best_time_section, std_of_variables = val

    __save_laps_section_all_laps(directory, data_all_laps, 
                                    f"{date}_{time}_all_laps")
    __save_laps_section_all_laps(directory, data_for_best_lap, 
                                    f"{date}_{time}_best_lap")
    __save_data_best_sections(directory, best_time_section, 
                                    f"{date}_{time}_best_section")
    __save_std_for_each_section(directory, std_of_variables,
                                    f"{date}_{time}_std_each_section")
    
    file.close()


if __name__ == "__main__":
    path = askdirectory()
    import os
    file_list = list(os.listdir(path))

    def cor_clean_data_file(file): return file.endswith("_cleaned_data.csv")
    files_csv_data = sorted(list(filter(cor_clean_data_file, file_list)))

    for file in files_csv_data:
        date, time = file.split("_")[0:2]
        data_analysis(f"{path}{sign}{file}", path, date, time)
