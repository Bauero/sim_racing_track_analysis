import openpyxl
from helper_functions import *

path = r"/Users/piotrbauer/Documents/SGGW/Semsetr_6/HANZE/car_data_analysis/Data/Clean_data/06-05/Register_laps_2.xlsx"
file = openpyxl.open(path)
sheet_list = file.sheetnames

all_data = {}

for sheet in sheet_list:

    last_cell = list(file[sheet].dimensions.split(":")[-1])
    tmp = 0

    # Find, where separation between column, and row number is
    # in "AB10598" it is on index 2 -> digit '1'
    for c in last_cell:
        if c.isdecimal(): break
        tmp += 1

    end = 'C' + "".join(last_cell[tmp:])

    performance = {}
    values = file[sheet]["A2":end]

    for row in values:
        lap, section, value = (v.value for v in row)

        # If we finished iterating over data
        if lap == None or section == None or value == None:
            break

        lap, seciton, value = int(lap), int(section), int(value)
        
        if lap not in performance.keys():
            performance[lap] = {}
        if section not in performance[lap].keys():
            performance[lap][section] = value

    for key in performance:
        print(key, performance[key])

    all_data[sheet] = performance

print(all_data.keys())
file.close()
