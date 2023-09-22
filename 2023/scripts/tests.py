import os
from typing import Dict, List


# CONSTANTS #
PREFIX_2023 = os.getcwd()
if PREFIX_2023[-4:] == "data":
    PREFIX_2023 = os.path.join(
        PREFIX_2023, "2023"
    )


# FUNCTIONS
def integrity_check(uun: str) -> bool:
    '''
    Checks if all files under this dir belongs to the right student.
    '''
    full_path = os.path.join(PREFIX_2023, uun)
    files = os.listdir(full_path)
    for file in files:
        if uun not in file:
            return False
    return True

def count_files(uun: str) -> Dict[str,int]:
    results = {}
    full_path = os.path.join(PREFIX_2023, uun)
    files = os.listdir(full_path)
    results["total"] = len(files)
    respecks = 0
    thingys = 0
    for file in files:
        if "Respeck" in file:
            respecks += 1
        elif "Thingy" in file:
            thingys += 1
        else:
            raise AssertionError(f"{file} is neither respeck nor thingy recording.")
    results["respeck"] = respecks
    results["thingy"] = thingys
    return results


if __name__ == "__main__":
    student = "s0247783"
    print(integrity_check(student))
    res = count_files(student)
    print(res)
