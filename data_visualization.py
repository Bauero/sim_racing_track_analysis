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


def show_speed_distance_graphs(datasets : list[pd.DataFrame], lap : int = 1):
    plt.figure(figsize=(10,6))
    plt.title(f"Car comparison based on Distance - lap {lap}")

    plots = []
    highiest_distance = 0
    highiest_speed = 0

    for n, dts in enumerate(datasets):
        d_ft_d = dts[dts['LAP_BEACON'] == lap]
        driver_dist, = plt.plot(d_ft_d.Distance, 
                                d_ft_d['SPEED'],
                                label = f'Car #{n+1}')
        plots.append(driver_dist)
        cms = max(d_ft_d['SPEED'])
        cmd = max(d_ft_d['Distance'])
        highiest_speed = cms if cms > highiest_speed else highiest_speed
        highiest_distance = cmd if cmd > highiest_distance else highiest_distance

    plt.grid(True)
    plt.legend(handles=plots, loc='upper right')
    plt.xlabel("Distance [m]")
    plt.ylabel("Speed [km/h]")
    plt.yticks(np.arange(0,( highiest_speed // 10 + 1) * 10, 10))
    plt.xticks(np.arange(0, (highiest_distance // 250 + 1) * 250 + 1, 250))

    return plots


def show_speed_time_graphs(datasets : list[pd.DataFrame], lap : int = 1):
    plt.figure(figsize=(10,6))
    plt.title(f"Car comparison based on Time - lap {lap}")

    plots = []
    highiest_time = 0
    highiest_speed = 0

    for n, dts in enumerate(datasets):
        d_ft_t = dts[dts['LAP_BEACON'] == lap]
        driver_dist, = plt.plot(d_ft_t.index, 
                                d_ft_t['SPEED'],
                                label = f'Car #{n+1}')
        plots.append(driver_dist)
        cms = max(d_ft_t['SPEED'])
        cmt = max(d_ft_t.index)
        highiest_speed = cms if cms > highiest_speed else highiest_speed
        highiest_time = cmt if cmt > highiest_time else highiest_time

    plt.grid(True)
    plt.legend(handles=plots, loc='upper right')
    plt.xlabel("Time [s]")
    plt.ylabel("Speed [km/h]")
    plt.yticks(np.arange(0, (highiest_speed // 10 + 1) * 10 + 1, 10))
    plt.xticks(np.arange(0, (highiest_time // 10 + 1) * 10 + 1 , 10))

    return plots


if __name__ == "__main__":
    path = "/Users/piotrbauer/Documents/SGGW/Semsetr_6/HANZE/" +\
           "car_data_analysis/cleaned_data_2.3.2024_15-03-03.csv"
    path2 = "/Users/piotrbauer/Documents/SGGW/Semsetr_6/HANZE/" +\
           "car_data_analysis/cleaned_data_3.3.2024_17-45-14.csv"

    data = pd.read_csv(path, skip_blank_lines=True, header=0, index_col="Time",
                        delimiter=',',decimal=',')
    
    data2 = pd.read_csv(path2, skip_blank_lines=True, header=0, index_col="Time",
                        delimiter=',',decimal=',')

    exceptions = ['LAP_BEACON']
    not_exceptions = [x for x in data.columns.to_list() if x not in exceptions]

    data = data.astype(float)
    data[exceptions] = data[exceptions].astype(int)
    data2 = data2.astype(float)
    data2[exceptions] = data2[exceptions].astype(int)

    show_speed_distance_graphs([data, data2])
    show_speed_time_graphs([data, data2])

    plt.show()

    exit()
