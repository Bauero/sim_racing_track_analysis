"""
This file is responsible for processing prepared data & should store all func.
necessary to proprerly show properties of raw racing data.
"""

import os
from tkinter import filedialog
import pandas as pd
# from data_preparation import display_track_summary as __dts, \
#                              extract_general_data as __egd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import math

INF = math.inf

def show_speed_graph_whole(table):
    laps = table['LAP_BEACON'].unique()

    plt.figure(figsize=(10, 6))

    # Plot each lap
    for i, lap in enumerate(laps, start=1):
        lap_table = table[table['LAP_BEACON'] == lap]
        plt.plot(lap_table.index, lap_table['SPEED'], label=f'Lap {int(lap)}')

    plt.title('Speed on All Laps')
    plt.xlabel('Time')
    plt.ylabel('Speed (km/h)')
    plt.legend()
    plt.grid(True)
    plt.show()


def show_stats_one_lap_all_datasets(datasets : list[pd.DataFrame], 
                                    index_column : str = 'Time',
                                    data_column : str = 'SPEED',
                                    id_col_unit : str =  's',
                                    data_col_unit : str = 'm/s',
                                    xgrid_step = 0,
                                    ygrid_step = 0,
                                    lap : int = 1
                                    ):
    """
    This funciton should allow to create liniar plot between 2 values over time
    for all given datasets. By default, it would compare `Speed` over `Time` in
    lap one for all given datasets. By default the grid will be also adjusted
    because default matplotlib's grid behaviour produces only a few grid lines
    making graph hard to read. Hoverwer those settings might be changes using
    additional parameters:

    - `index_column` - specifies name of the column which will be used as X axis
    - `data_column` - specifies name of the column which will be used as Y axis
    - `id_col_unit` - what units will be displayed next to name of X axis
    - `data_col_unit` - what units will be displayed next to name of y axis
    - `xgrid_step` - specify custom x-axis step
    - `ygrid_step` - specify custom y-axis step
    - `lap` - data from which laps to display
    """

    is_index = index_column == 'Time'
    is_data_an_index = data_column == 'Time'

    index_column_to_disp = index_column[:].replace("_"," ")
    data_column_to_disp = data_column[:].replace("_"," ")
    id_col_unit.capitalize()
    data_col_unit.capitalize()
    
    whole_plot = plt.figure(figsize=(10,6))
    title = f"{data_column_to_disp.title()} comparison based on " + \
            f"{index_column_to_disp.lower()} - lap {lap}"
    plt.title(title)

    plots = []
    highiest_index = 0
    highiest_data = 0
    lowest_index = INF
    lowest_data = INF

    for n, dts in enumerate(datasets):
        d_ft_d = dts[dts['LAP_BEACON'] == lap]  # Filer data for our lap
        if d_ft_d.empty: continue   # Skip data without our lap

        X = d_ft_d.index if is_index else d_ft_d[index_column]
        Y = d_ft_d.index if is_data_an_index else d_ft_d[data_column]

        driver_dist, = plt.plot(X, Y, label = f'Driver #{n+1}')
        plots.append(driver_dist)
        
        cur_max_id = max(X)     ;  cur_min_id = min(X)
        cur_max_data = max(Y)   ;  cur_min_data = min(Y)
        
        if cur_max_id > highiest_index:     highiest_index  =   cur_max_id
        if cur_min_id < lowest_index:       lowest_index    =   cur_min_id
        if cur_max_data > highiest_data:    highiest_data   =   cur_max_data
        if cur_min_data < lowest_data:      lowest_data     =   cur_min_data

    # Adjust grid sizing
    if xgrid_step >= 0:
        id_step = (highiest_index - lowest_index)
        final_id_step = id_step//15 if id_step//15 > 0 else 1
        lowest_index = round(lowest_index)
    else:
        final_id_step = xgrid_step
        lowest_index = 0
        highiest_index = (highiest_index // xgrid_step) * xgrid_step
    
    if ygrid_step >= 0:
        data_step = (highiest_data - lowest_data)
        final_data_step = data_step//10 if data_step//10 > 0 else 1
        lowest_data = round(lowest_data)
    else:
        final_data_step = ygrid_step
        lowest_data = 0
        highiest_data = (highiest_data // ygrid_step) * ygrid_step

    # Create our plot
    plt.grid(True)
    plt.legend(handles=plots, loc='upper right')
    plt.xlabel(f"{index_column_to_disp.title()} [{id_col_unit}]")
    plt.ylabel(f"{data_column_to_disp.title()} [{data_col_unit}]")
    plt.xticks(np.arange(lowest_index, highiest_index * 1.01, final_id_step))
    plt.yticks(np.arange(lowest_data, highiest_data * 1.01, final_data_step))

    return whole_plot, plots, title


def main():

    directory = "/Users/piotrbauer/Documents/SGGW/Semsetr_6/HANZE/" + \
        "car_data_analysis/Clean_data/Clean_data/" + \
        "dot_separated_additional_collumns"

    path  = f"{directory}/cleaned_data_2.3.2024_15-03-03.csv"
    path2 = f"{directory}/cleaned_data_3.3.2024_17-45-14.csv"
    path3 = f"{directory}/cleaned_data_3.10.2024_14-32-04.csv"
    path4 = f"{directory}/cleaned_data_3.12.2024_20-11-03.csv"

    data = pd.read_csv(path, skip_blank_lines=True, header=0, index_col="Time",
                        delimiter=',',decimal=',')
    
    data2 = pd.read_csv(path2, skip_blank_lines=True, header=0, index_col="Time",
                        delimiter=',',decimal=',')
    
    data3 = pd.read_csv(path3, skip_blank_lines=True, header=0, index_col="Time",
                        delimiter=',',decimal=',')
    
    data4 = pd.read_csv(path4, skip_blank_lines=True, header=0, index_col="Time",
                        delimiter=',',decimal=',')

    exceptions = ['LAP_BEACON']
    not_exceptions = [x for x in data.columns.to_list() if x not in exceptions]

    data = data.astype(float)
    data[exceptions] = data[exceptions].astype(int)
    data2 = data2.astype(float)
    data2[exceptions] = data2[exceptions].astype(int)
    data3 = data3.astype(float)
    data3[exceptions] = data3[exceptions].astype(int)
    data4 = data4.astype(float)
    data4[exceptions] = data4[exceptions].astype(int)

    for i in range(1,6):
        whole_plot, plots, title = show_stats_one_lap_all_datasets(
                                        [data, data2, data3, data4], 
                                        "Distance_on_lap",
                                        "SPEED",
                                        data_col_unit = 'km/h',
                                        lap=i)
        whole_plot.savefig(f"{directory}/{title}.png", dpi=200)
    exit()


if __name__ == "__main__":
    main()
