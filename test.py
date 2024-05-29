import pandas as pd

file = pd.read_csv(r"/Users/piotrbauer/Documents/SGGW/Semsetr_6/HANZE/car_data_analysis/Data/Clean_data/05-29/Cleaned data/Chris/Barcelona-mclaren_720s_gt3-11-2024.05.29-13.37.41/13-37-41_29-05-2024_cleaned_data.csv")

print(file[file['Section'] == 1])

