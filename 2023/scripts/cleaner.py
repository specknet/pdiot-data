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
    '''
    Not to be confused with the actual data cleaning process. 
    It only removes redundant thingy recordings. 
    '''
    def __init__(self, uun: str) -> None:
        self.uun = uun
        self.full_path = os.path.join(PREFIX_2023, uun)
        self.files = os.listdir(self.full_path)
    
    def filter_thingys(self):
        '''
        Remove any thingy recording that is not labeled as normal. 
        Resulting in 12 thingy files. 
        Warning: Back up original raw files before running. 
        '''
        thingys = []
        for file in self.files:
            if "Thingy" in file:
                thingys.append(file)
        for thingy in thingys:
            if "Normal" not in thingy:
                os.remove(os.path.join(self.full_path, thingy))


if __name__ == "__main__":
    student = "s2047783"
    cleaner = DataCleaner(student)
    cleaner.filter_thingys()