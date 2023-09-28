from viewer_utils import *


# CONSTANTS #
PREFIX_2023 = os.getcwd()
if PREFIX_2023[-4:] == "data":
    PREFIX_2023 = os.path.join(
        PREFIX_2023, "2023"
    )

redo_needed = [
    "standing_hyperventilating",
    "sitting_hyperventilating"
]

student = "s2047783"
full_path = os.path.join(PREFIX_2023, student, "ui_trims")
print(len(os.listdir(full_path)))
ui_trimmed = [filename for filename in os.listdir(full_path)
              if "doubt" not in filename]
print(len(ui_trimmed))

# check length: 
# for 
