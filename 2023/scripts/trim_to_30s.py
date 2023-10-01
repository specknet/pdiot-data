import os
from typing import Dict, List
import pandas as pd


# CONSTANTS #
PREFIX_2023 = os.getcwd()
if PREFIX_2023[-4:] == "data":
    PREFIX_2023 = os.path.join(
        PREFIX_2023, "2023"
    )


student = "s2047783"
folder_path = os.path.join(PREFIX_2023, student)
# file_names = [filename for filename in os.listdir(folder_path) if "clean" in filename]
file_names = ["Respeck_s2047783_Lying down on left_Hyperventilating_clean_01-10-2023_13-45-20.csv"]

for filename in file_names:
    full_path = os.path.join(folder_path, filename)
    df = pd.read_csv(full_path, header=0)
    df = df[:760]
    df.to_csv(full_path, index=False)