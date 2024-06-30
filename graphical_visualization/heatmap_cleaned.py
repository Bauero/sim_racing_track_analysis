import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import pathlib


##########################  CONSTANTS FOR COLORING   ##########################


acceptable_time_std = {
    1:  0.5,
    2:  0.2,
    3:  0.3,
    4:  0.1,
    5:  0.3,
    6:  0.2,
    7:  0.3,
    8:  0.15,
    9:  0.3,
    10: 0.3,
    11: 0.3,
    12: 0.3,
    13: 0.3,
    14: 0.3,
    15: 0.3,
    16: 0.03,
    17: 0.15,
    18: 0.3,
    19: 0.05,
    20: 0.3,
    21: 0.3,
    22: 0.3,
    23: 0.3,
    24: 0.3,
}

bad_color = [255,0,0]
avg_color = [255,255,0]
good_color = [0,255,0]


#########################  FUNCITONS USED IN PROGRAM   #########################


def __return_color(section, value, std_table) -> str:
    """
    This function will return a string in form of `#120A11`. Function checkes
    what value is the `average` for a speciphic `section` based on the section 
    and `std_table` provided. Then, function calculates the color. Color would 
    be pure `good_color` if the value is <= 50% of value, and pure `bad_color` 
    if value is >= 200% of the expected value. (Expected, average value is the
    value in the table for a speciphic seciton)

    :section: - section in the table for which we do calculation
    
    :value: - value which we want to compare against

    :std_table: - table with values which are considered to be average
    """
    
    global bad_color
    global avg_color
    global good_color

    proper_std = std_table[section]
    end_color = []

    if value < proper_std:
        if value <= proper_std*0.5:
            end_color = good_color
        else:
            normalizer = 1 - abs(0.5*proper_std - value)/(0.5*proper_std)
            end_color = [int((good_color[i] -  avg_color[i]) * normalizer + 
                         avg_color[i]) for i in range(3)]
    elif value > proper_std:
        if value >= proper_std*2:
            end_color = bad_color
        else:
            normalizer = 1 - abs(2*proper_std - value)/(2*proper_std)
            end_color = [int((bad_color[i] -  avg_color[i]) * normalizer + avg_color[i]) 
                          for i in range(3)]
    else:
        end_color = avg_color

    return f"#{end_color[0]:02x}{end_color[1]:02x}{end_color[2]:02x}"


def __return_colors_for_seciton(file : str, 
                                value_to_compare : str, 
                                std_table : dict):
    """This funciton allows to genrate colors to all secitons
    
    - `file` - path to file which should contain column specifiend in 
    `value_to_compare` param
    - `value_to_compare` - name of the colum with value which we are using for
    comparison - propably 'Std Time'
    - `std_table` - table with values which are used as expected for seciphic
    sections
    """

    global acceptable_time_std
    return_dictionary = {}

    df = pd.read_csv(file)

    for row in acceptable_time_std:
        std_time = float(df.iloc[row-1][value_to_compare].replace(",","."))
        return_dictionary[row] = __return_color(row, std_time, std_table)

    return return_dictionary


#############################  PUBLIC FUNCTIONS   #############################


def draw_heatmap_for_file(file, main = False):

    if not main:
        catalunya_cleaned = pd.read_csv(str(pathlib.Path().resolve()) + 
                        "/graphical_visualization/Catalunya_cleaned.csv")
    else:
        catalunya_cleaned = pd.read_csv(str(pathlib.Path().resolve()) + 
                            "/Catalunya_cleaned.csv")

    # Extract the coordinates and sections
    x_coords = catalunya_cleaned['Starting_x']
    y_coords = catalunya_cleaned['Starting_y']
    sections = catalunya_cleaned['Section']

    # Determine the rotation angle (90 degrees in radians)
    theta = -0.3185 * np.pi

    # Create the rotation matrix
    rotation_matrix = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])

    # Apply the rotation to each coordinate
    rotated_coords = np.dot(rotation_matrix, np.vstack((x_coords, y_coords)))

    # Get unique sections
    unique_sections = sections.unique()


    color_map = __return_colors_for_seciton(file, 'Std Time', 
                                            acceptable_time_std)

    # Plot each section separately with the specified colors
    plt.figure(figsize=(16, 8))

    for section in unique_sections:
        section_coords = rotated_coords[:, sections == section]
        plt.scatter(section_coords[0], 
                    section_coords[1], 
                    label=section, 
                    c = color_map.get(section),
                    )
        # Add section labels
        section_mean_x = np.mean(section_coords[0])
        section_mean_y = np.mean(section_coords[1])
        plt.text(section_mean_x, section_mean_y, str(section), 
                 fontsize=12, ha='center', va='center', color='black')
        

    x_min, x_max = np.min(rotated_coords[0]), np.max(rotated_coords[0])
    y_min, y_max = np.min(rotated_coords[1]), np.max(rotated_coords[1])
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), 
                         np.linspace(y_min, y_max, 100))

    # Calculate contours
    levels = np.linspace(np.min(rotated_coords), np.max(rotated_coords), 10)

    # Add contours
    plt.contour(xx, yy, np.zeros_like(xx), levels = levels, colors = 'black', 
                alpha=0.3)

    plt.title('Consistency heatmap (base on time)')
    plt.grid(False)  # Hide grid lines
    plt.axis('equal')
    plt.legend(title='Sections', loc='center left', bbox_to_anchor=(1, 0.5))  
    plt.tick_params(axis='both', which='both', bottom=False, top=False, 
                    left=False, right=False, labelbottom=False, labelleft=False)
    x_buffer = (x_max - x_min) * 0.1  # Adjust the buffer as needed
    y_buffer = (y_max - y_min) * 0.1  # Adjust the buffer as needed
    plt.xlim(x_min - x_buffer, x_max + x_buffer)
    plt.ylim(y_min - y_buffer, y_max + y_buffer)
    plt.show()


if __name__ == "__main__":

    import tkinter as TK
    from tkinter.filedialog import askopenfilename

    TK.Tk().withdraw()
    # Load the data from the CSV file
    csv_file_path = askopenfilename(
            title="Select location of std file",
            filetypes=[("CSV files", "*.csv")]
        )
    TK.Tk().destroy()

    if csv_file_path.endswith("_std_each_section.csv"):
        draw_heatmap_for_file(csv_file_path, main = True)
