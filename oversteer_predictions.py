"""
This is a program which would try to learn model, and then validate results and
show the overall error. 
"""

from sklearn.tree import DecisionTreeRegressor
import tkinter as tk
from tkinter.filedialog import askopenfilename
import pandas as pd


root = tk.Tk()
root.withdraw()
file = askopenfilename()
if not file:
    print("No file was selected - ending program")

data = pd.read_csv(file)
# print(data.columns)

ovst = data.Oversteer
col = ['STEERANGLE','steered angle','G_LON','G_LAT',
       'SPEED','Section','THROTTLE','BRAKE','Distance_on_lap',
       'WHEEL_SPEED_LF','WHEEL_SPEED_RF','WHEEL_SPEED_LR','WHEEL_SPEED_RR']
X = data[col]


from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

train_X, val_X, train_y, val_y = train_test_split(X, ovst, random_state = 0)

our_model = DecisionTreeRegressor()

our_model.fit(train_X, train_y)

val_predictions = our_model.predict(val_X)
mae = mean_absolute_error(val_y, val_predictions, multioutput='raw_values')


print(mae)


