import os
from typing import Dict, List


# CONSTANTS #
PREFIX_2023 = os.getcwd()
if PREFIX_2023[-4:] == "data":
    PREFIX_2023 = os.path.join(
        PREFIX_2023, "2023"
    )
GT_COUNTS = {
    "total": 48 + 24 + 40,
    "respecks": 24 + 24 + 40,
    "thingys": 24
}


# rename unprocessed
student = "s2047783"
folder_path = os.path.join(PREFIX_2023, student)



