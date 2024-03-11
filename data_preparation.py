"""
This file contains funcitons which would allow to help clean csv files exported
from Motec software. This way one can easily clean data just by using prepared
funtions
"""

def __extract_general_data(file_object, make_file : bool = False,
                           verbose : bool = False) -> dict:
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
    
    def __display_track_summary():

        ts = ''

        # display all stats except laps data (displayed separately below)
        for stats in track_summary:
            if stats == 'beacon_makers' or stats == 'laps_start_end':
                continue
            ts += (f"{stats.capitalize():20} : {track_summary[stats]}") + '\n'

        print("\nLap times\n") # line separator for clear display of data

        # display each lap times
        for i in range(len(laps_start_end)):
            start, end = laps_start_end[str(i + 1)].values()
            ts += f'Lap {(i + 1)} : {start:08.3f} - {end:08.3f}   =   {(end - start):.3f}s' + '\n'
        
        ts.strip()

        return ts
    
    if verbose:
        print(__display_track_summary())

    if make_file:
        new_file = f"data_information_{track_summary['log_date'].replace('-','_')}_{track_summary['log_time'].replace(':','_')}.csv"
        
        if verbose:
            print(f"Creting file '{new_file}'")

        new_file = open(new_file, "w")

        if verbose:
            print("Printing all information from the file:\n")
            ts = __display_track_summary()
            new_file.write(ts)
            print(ts,'\n')
        else:
            new_file.write(ts)
        


    return track_summary


def __remove_unnecessary_rows(file_object, hard_coded : bool = False,
                               verbose : bool = False) -> None:
    """
    This function is calles to remove data which are not important in our program
    aka. empty rows,
    or rows which contains not important information [like units]
    """

    if hard_coded:
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
        file_object = file_object[0] + file_object[3:]


def __remove_unnecessary_colums(file_object, verbose : bool = False):
    """
    This function allows to remove unnecessary columns which are not
    necessary for our data analysis
    """    

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


def __convert_values_to_float(file_object):
    """
    The purpose of this function is to convert all values to float
    """

    for row in range(len(file_object)):
        if row:
            file_object[row] = list(map(float, file_object[row]))


def __fill_missing_lap_data(file_object):
    import math
    column = file_object[0].index('LAP_BEACON')

    lap = 1

    last_time = track_summary['laps_start_end'][str(lap)]['end']

    for row in range(1,len(file_object)):
        if file_object[row][0] <= last_time:
            file_object[row][column] = lap
        else:
            lap += 1
            try:
                last_time = track_summary['laps_start_end'][str(lap)]['end']
            except:
                last_time = math.inf
            file_object[row][column] = lap


def prepare_data(file_object, verbose : bool = False):
    """
    This is general function which is responsible 
    """
    __extract_general_data(file_object, verbose)
    if verbose: print()
    __remove_unnecessary_rows(file_object, verbose)
    if verbose: print()
    __remove_unnecessary_colums(file_object, verbose)
    __convert_values_to_float(file_object)
    __fill_missing_lap_data(file_object)


def save_data_csv_coma_format(file_object):
    """
    This function is responsible for storage of modified file into a new file
    """
    import csv

    new_file = open(f"cleaned_data_{track_summary['log_date'].replace('-','_')}_{track_summary['log_time'].replace(':','_')}.csv",'w')

    csvwriter = csv.writer(new_file)

    # csvwriter.writerows(csvreader)
    for row in csvreader:
        csvwriter.writerow([str(a).replace('.',',') for a in row])

    new_file.close()


if __name__ == "__main__":
    # print("This file is should only contain function which can later be used to" +
    #        "work on data. Therefore if you open this file this message is visible." +
    #        "To use function of from this file open proper file")
    # print()
    # input("Press Enter to close the widndow ... ")
    import csv
    file = open('all_laps_motec.csv')
    csvreader = list(csv.reader(file))

    # prepare_data(csvreader)
    # save_data_csv_coma_format(csvreader)

    __remove_unnecessary_rows(csvreader, True)

    for i in range(20):
        print(str(csvreader[i])[:80])

    file.close()