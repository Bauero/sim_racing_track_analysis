"""
This file would contain funcitons which are necessary to perform data analysis
of preprocessed file. If this file is run as an stanalone file, it expects you
to select directory in which there are located files with data. Files are 
expected to have names in form of '`data_time_cleaned_data.csv`'
"""

import pandas as pd
from constants import sign
from tkinter.filedialog import askdirectory


#############################  INTERNAL FUNCITONS  #############################


def __calculate_speed_per_section(df):
    tabela = pd.DataFrame()
    tabela['Lap'], tabela['Section'] = \
        df['LAP_BEACON'].astype(str), df['Section'].astype(str)
    tabela = tabela.drop_duplicates(subset=['Lap','Section'])
    tabela.reset_index(drop=True)
    tabela = tabela.astype(float)

    def calculate_speed_stats(row):
        lap = row['Lap']
        section = row['Section']
        
        # Filter the original DataFrame for the given lap and section
        subset = df[(df['LAP_BEACON'] == lap) & (df['Section'] == section)]
        
        # Calculate max, min, and average speed for the subset
        max_speed = subset['SPEED'].max()
        min_speed = subset['SPEED'].min()
        avg_speed = round(subset['SPEED'].mean(), 3)
        time_diff = round(subset['Time'].max() - subset['Time'].min(), 3)
        
        return pd.Series({'Lap': lap, 
                          'Section': section, 
                          'Max Speed': max_speed, 
                          'Min Speed': min_speed, 
                          'Avg Speed': avg_speed, 
                          'Time duration' : time_diff})

    speed_stats = tabela.apply(calculate_speed_stats, axis=1)
    col_to_f = ["Max Speed", "Min Speed", "Avg Speed", "Time duration"]
    speed_stats[col_to_f] = speed_stats[col_to_f].astype(float)
    col_to_int = ["Lap", "Section"]
    speed_stats[col_to_int] = speed_stats[col_to_int].astype(int)
    speed_stats = speed_stats.reset_index(drop=True)

    return speed_stats


def __find_best_lap(speed_stats):
    result = pd.pivot_table(
        speed_stats[["Lap","Time duration"]], columns=["Lap"], aggfunc=sum)
    result = result.transpose()
    shortest_lap = int(result.sort_values(by='Time duration').iloc[0].name)
    return speed_stats[speed_stats['Lap'] == shortest_lap]


def __calculate_best_sections(speed_stats):
    sh_time_rows = speed_stats.groupby('Section')['Time duration'].idxmin()
    shortest_time_table = speed_stats.loc[sh_time_rows]
    return shortest_time_table


def __calculate_std(speed_stats):
    std_dev_df = pd.DataFrame(columns=['Section', 
                                       'Std max speed', 
                                       'Std min speed', 
                                       'Std avg speed', 
                                       'Std sec time'])

    # Loop through each section and calculate standard deviation
    for i in range(1, 25):
        std_max = speed_stats[speed_stats.Section == i]['Max Speed'].std()
        std_min = speed_stats[speed_stats.Section == i]['Min Speed'].std()
        std_avg = speed_stats[speed_stats.Section == i]['Avg Speed'].std()
        std_time = speed_stats[speed_stats.Section == i]['Time duration'].std()
        
        std_max = round(std_max, 3)
        std_min = round(std_min, 3)
        std_avg = round(std_avg, 3)
        std_time = round(std_time, 3)

        # Append standard deviation values to the DataFrame
        std_dev_df = std_dev_df.append(
            {
            'Section': int(i),
            'Std max speed': std_max,
            'Std min speed': std_min,
            'Std avg speed': std_avg,
            'Std sec time': std_time
            }, ignore_index=True)
        
    std_dev_df.set_index('Section')
    std_dev_df = std_dev_df.astype(float)

    return std_dev_df


def __save_file_as_csv(path, data, title):
    data.to_csv(f"{path}{sign}{title}.csv", index=False)


##############################  PUBLIC FUNCITONS  ##############################


def data_analysis(path_to_file, directory, date, time):

    df = pd.read_csv(path_to_file)
    df = df.astype(float)

    speed_stats = __calculate_speed_per_section(df)
    best_lap = __find_best_lap(speed_stats)
    best_sections = __calculate_best_sections(speed_stats)
    std_values = __calculate_std(speed_stats)

    __save_file_as_csv(directory, speed_stats, f"{date}_{time}_all_laps")
    __save_file_as_csv(directory, best_lap, f"{date}_{time}_best_lap")
    __save_file_as_csv(directory, best_sections, f"{date}_{time}_best_section")
    __save_file_as_csv(directory, std_values, f"{date}_{time}_std_each_section")


if __name__ == "__main__":
    path = askdirectory()
    import os
    file_list = list(os.listdir(path))

    def cor_clean_data_file(file): return file.endswith("_cleaned_data.csv")
    files_csv_data = sorted(list(filter(cor_clean_data_file, file_list)))

    for file in files_csv_data:
        date, time = file.split("_")[0:2]
        data_analysis(f"{path}{sign}{file}", path, date, time)

