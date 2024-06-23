"""
This file contains function which are necessary for extraction and display of
race data from csv file from MoTeC. Those funciton are stored in separate file
as they are use by data preparation files both using standard solution, and
pandas library
"""
from additional.additional_commands import c_blue, c_green, c_pink, c_cyan


def display_laps_summary(laps_start_end, color : bool = False):

    ts = ""

    # line separator for clear display of data
    if color:
        ts += c_cyan("\nLap times\n\n")
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
            
    return ts


def display_track_summary(race_data, color : bool = False):
    """
    This is helper function - it is used to prepare, and return track data
    in readable form (to be stored in file or displayed in console)
    """

    laps_start_end = race_data['laps_start_end']
    ts = ''

    # line separator for clear display of data
    if color:
        ts += "General informaiton about data\n\n"
    else:
        ts += "General informaiton about data\n\n"

    # display all stats except laps data (displayed separately below)
    for stats in race_data:
        if stats == 'beacon_makers' or stats == 'laps_start_end':
            continue
        if color:
            ts += c_pink(f"{stats.capitalize():20}") + \
                 " : "  +  f"{race_data[stats]}\n"
        else:
            ts += f"{stats.capitalize():20} : {race_data[stats]}\n"

    ts += display_laps_summary(laps_start_end, color)
    
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
    race_data = {
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
    race_data['beacon_makers'] = beacon_makers

    # Prepare dict of dicts which contains start end end of each lap
    # Lap 1 : 0.000 - 107.154
    # Lap 2 : 107.154 - 446.093
    # etc.
    laps_start_end = {}
    tmp_start = float(race_data['start_time'])
    for i in range(len(beacon_makers)):
        laps_start_end[str(i + 1)] = {"start" : tmp_start, 
                                      "end" : beacon_makers[i]}
        tmp_start = beacon_makers[i]
    else:
        if float(race_data['end_time']) > float(beacon_makers[-1]):
            laps_start_end[str(i + 2)] = {"start" : beacon_makers[i], 
                                    "end" : float(race_data['end_time'])}
    race_data['laps_start_end'] = laps_start_end

    # Display informaiton in the console if 'verbose' param set to 'True'

    if verbose:
        print(display_track_summary(race_data, True))
        
    return race_data
