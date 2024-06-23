import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tkinter as TK
from tkinter.filedialog import askopenfilename

acceptable_time_std = {
    1:  0.5,
    2:  0.2,
    3:  0.3,
    4:  0.1,
    5:  0.3,
    6:  0.2,
    7:  0.3,
    8:  0.3,
    9:  0.3,
    10: 0.3,
    11: 0.3,
    12: 0.3,
    13: 0.3,
    14: 0.3,
    15: 0.3,
    16: 0.3,
    17: 0.3,
    18: 0.3,
    19: 0.3,
    20: 0.3,
    21: 0.3,
    22: 0.3,
    23: 0.3,
    24: 0.3,
}

acceptable_max_speed_std = {
    1:  5,
    2:  2,
    3:  3,
    4:  1,
    5:  3,
    6:  2,
    7:  3,
    8:  3,
    9:  3,
    10: 3,
    11: 3,
    12: 3,
    13: 3,
    14: 3,
    15: 3,
    16: 3,
    17: 3,
    18: 3,
    19: 3,
    20: 3,
    21: 3,
    22: 3,
    23: 3,
    24: 3,
}

bad_color = [255,0,0]
avg_color = [255,255,0]
good_color = [0,255,0]

def return_color(section, value, std_table):
    
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



def return_colors_for_seciton(file : str, 
                              value_to_compare : str, 
                              std_table : dict):
    """This funciton allows to genrate colors to all secitons
    
    - `file` - path to file which should contain column specifiend in 
    `value_to_compare` param
    - `value_to_compare` - 
    """

    global acceptable_time_std
    return_dictionary = {}

    df = pd.read_csv(file)

    for row in acceptable_time_std:
        std_time = float(df.iloc[row-1][value_to_compare].replace(",","."))
        return_dictionary[row] = return_color(row, std_time, std_table)

    return return_dictionary




TK.Tk().withdraw()
# Load the data from the CSV file
file_path = askopenfilename(
        title="Select location of Catalunya_cleaned file",
        filetypes=[("CSV files", "*.csv")]
    )
TK.Tk().destroy()

catalunya_data = pd.read_csv(file_path)

# Extract the coordinates and sections
x_coords = catalunya_data['Starting_x']
y_coords = catalunya_data['Starting_y']
sections = catalunya_data['Section']

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

TK.Tk().withdraw()
file_path2 = askopenfilename(
        title="Select file with std to analyze",
        filetypes=[("CSV files", "*.csv")]
    )
TK.Tk().destroy()

color_map = return_colors_for_seciton(file_path2, 'Std Time', acceptable_time_std)



# EFFICIENCY !!! - parse file for each seciton ?!?!

def choose_color(file_path3, section_number):
    # Load the CSV file
    df = pd.read_csv(file_path3)
    
    # Clean up column names
    df.columns = df.columns.str.replace(' ', '_')
    
    # Find the row with the specified section number
    row = df[df['Section'] == section_number]
    
    if not row.empty:
        # Extract the Std_Avg value
        std_avg = float(row['Std_Avg'].values[0].replace(',','.'))
        if std_avg >=10:
            return 'red'
        else:
            return 'blue'
  
    else:
        return None

# Define a color map for the sections
# color_map = {k : choose_color(file_path2, k) for k in range(1,25)}





# Plot each section separately with the specified colors
plt.figure(figsize=(16, 8))
# plt.axis('off')
# plt.grid(b=None)

for section in unique_sections:
    section_coords = rotated_coords[:, sections == section]
    plt.scatter(section_coords[0], 
                section_coords[1], 
                label=section, 
                c = color_map.get(section),
                )
    

x_min, x_max = np.min(rotated_coords[0]), np.max(rotated_coords[0])
y_min, y_max = np.min(rotated_coords[1]), np.max(rotated_coords[1])
xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))

# Calculate contours
levels = np.linspace(np.min(rotated_coords), np.max(rotated_coords), 10)

# Add contours
plt.contour(xx, yy, np.zeros_like(xx), levels=levels, colors='black', alpha=0.3)

plt.title('Circuit de Barcelona-Catalunya Heatmap')
plt.grid(False)  # Hide grid lines
plt.axis('equal')
plt.legend(title='Sections', loc='center left', bbox_to_anchor=(1, 0.5))  # Move legend outside and to the left
plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, 
                right=False, labelbottom=False, labelleft=False)
x_buffer = (x_max - x_min) * 0.1  # Adjust the buffer as needed
y_buffer = (y_max - y_min) * 0.1  # Adjust the buffer as needed
plt.xlim(x_min - x_buffer, x_max + x_buffer)
plt.ylim(y_min - y_buffer, y_max + y_buffer)
plt.show()