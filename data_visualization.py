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


if __name__ == "__main__":
    path = "/Users/piotrbauer/Documents/SGGW/Semsetr_6/HANZE/" +\
           "car_data_analysis/cleaned_data_2_3_2024_15_03_03.csv"

    data = pd.read_csv(path, skip_blank_lines=True, header=0, index_col="Time",
                        delimiter=',',decimal=',')

    exceptions = ['LAP_BEACON']
    not_exceptions = [x for x in data.columns.to_list() if x not in exceptions]

    data[exceptions] = data[exceptions].astype(int)
    data[not_exceptions] = data[not_exceptions].astype(float)

    # plt.figure(figsize=(10,6))
    # wynik = sns.lineplot(data['SPEED'])
    # plt.show()

    show_speed_graph_whole(data)

    exit()
