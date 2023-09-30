from viewer_utils import *
from pprint import pprint


# CONSTANTS #
PREFIX_2023 = os.getcwd()
if PREFIX_2023[-4:] == "data":
    PREFIX_2023 = os.path.join(
        PREFIX_2023, "2023"
    )

redo_needed = {  # item: note
    # "standing_hyperventilating": "confused w/sittt",
    # "sitting_hyperventilating": "confused w/stand"
}

need_less = {}

student = "s2047783"
# full_path = os.path.join(PREFIX_2023, student, "ui_trims")
full_path = os.path.join(PREFIX_2023, student)
# print(len(os.listdir(full_path)))
cleaned = [filename for filename in os.listdir(full_path)
              if "clean" in filename]
# print(len(ui_trimmed))

time_limit_min = 25*28
time_limit_min_save_margin = int(25*28.5)
time_limit_max = 25*32
time_limit_max_save_margin = int(25*31.5)

# check length: 
for trimmed_file in cleaned:
    filepath = os.path.join(full_path, trimmed_file)
    df = read_data_to_df(filepath, 0)
    length = df.index.stop - df.index.start
    if length < time_limit_min_save_margin:
        redo_needed[trimmed_file] = length
    elif length > time_limit_max_save_margin:
        need_less[trimmed_file] = length

print("Need Redo:")
pprint(redo_needed)
print("Less needed")
pprint(need_less)