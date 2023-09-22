import os
from typing import Dict, List
from pprint import pprint


# CONSTANTS #
PREFIX_2023 = os.getcwd()
if PREFIX_2023[-4:] == "data":
    PREFIX_2023 = os.path.join(
        PREFIX_2023, "2023"
    )


# FUNCTIONS
class DataCleaner():
    def __init__(self, uun: str) -> None:
        self.uun = uun
        self.full_path = os.path.join(PREFIX_2023, uun)
        self.files = os.listdir(self.full_path)
    
    def filter_thingys(self):
        '''
        Remove any thingy recording that is not labeled as normal.
        '''
        thingys = []
        for file in self.files:
            if "Thingy" in file:
                thingys.append(file)
        needed_thingys = []
        for thingy in thingys:
            if "Normal" in thingy:
                needed_thingys.append(thingy)
        pprint(needed_thingys)
        print(len(needed_thingys))


if __name__ == "__main__":
    student = "s2047783"
    cleaner = DataCleaner(student)
    cleaner.filter_thingys()