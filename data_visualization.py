"""
This file is responsible for processing prepared data & should store all func.
necessary to proprerly show properties of raw racing data.
"""

import os
from tkinter import filedialog
import pandas as pd


def __read_data_term():
    ans = input("\033[93mInput file path\033[0m: \033[94m").strip()
    print("\033[0m", end = "")
    if os.path.exists(ans):
        return __read_data(ans)
    else:
        return None


def __read_data_choose_file():
    ans = filedialog.askopenfile(filetypes=[("Coma Separated Value","*.csv")])
    if ans:
        return __read_data(ans)
    else:
        return None


def __read_data(path : str):
    return pd.read_csv(path)


if __name__ == "__main__":
    print(__read_data_term())
    exit()
