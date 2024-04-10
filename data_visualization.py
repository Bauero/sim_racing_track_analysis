"""
This file is responsible for processing prepared data & should store all func.
necessary to proprerly show properties of raw racing data.
"""

from pandas import read_csv, DataFrame
from tkinter import Tk
from tkinter.filedialog import askopenfilenames, askdirectory
import matplotlib.pyplot as plt
from numpy import arange
import math
INF = math.inf


##########################  FUNCTIONS TO MAKE GRAPHS  ##########################


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


def show_stats_one_lap_all_datasets(datasets : list[DataFrame], 
                                    index_column : str = 'Time_on_lap',
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
    plt.xticks(arange(lowest_index, highiest_index * 1.01, final_id_step))
    plt.yticks(arange(lowest_data, highiest_data * 1.01, final_data_step))

    return whole_plot, plots, title


######################  EXAMPLES OF USE OF THE FUNCTIONS  ######################


def example1():
    """
    This funciton is responsible for:

    1. Asking for source files which would be analyzed
    2. Assuring thery are formatted well (all values are floats)
    3. Asking where to store grapsh when they will be done
    4. Generating plots and storing them inside 
    """

    # Ask for files to get data from
    Tk().withdraw()
    fl_paths = askopenfilenames(initialdir="~", 
                                title="Choose files with racing data",
                                filetypes=[("CSV","*.csv")])

    # Quit if no files selected
    if not fl_paths: return

    # Otherwise ...
    files = []
    exceptions = ['LAP_BEACON']

    # Read each file, and assure, that all columns contains float (excep columns
    # which are stored in list 'excptions' - those will be converted to int)
    for file in fl_paths:
        data = read_csv(file, 
                           skip_blank_lines=True, 
                           header=0, 
                           index_col="Time", 
                           delimiter=',', 
                           decimal=',')
        data = data.astype(float)
        data[exceptions] = data[exceptions].astype(int)
        files.append(data)

    # Now, generate 5 grahs - one for each lap, to compare how specific value, 
    # changes during every lap for each driver
    laps = 5

    # Here, I want to display speed, for specific distance value on every lap,
    # for each driver (for each source file I selected) - I have to specify
    # names of columns which will be used as X and Y axis
    X_axis = "Distance_on_lap"
    Y_axis = "SPEED"

    # Before proceeding, ask where grapsh should be stored
    Tk().withdraw()
    directory = askdirectory(title="Choose directory to save graphs")
    if not directory: return

    # Generate graphs, according to the settings
    for i in range(laps):
        whole_plot, plots, title = show_stats_one_lap_all_datasets(
                                        files, 
                                        X_axis,
                                        Y_axis,
                                        lap = i+1)
        whole_plot.savefig(f"{directory}/{title}.png", dpi=200)


if __name__ == "__example__":
    example1()
