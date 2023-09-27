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


# FUNCTIONS
class DataExaminer():
    '''
    Checks for: 
     - file integrity: all files belongs to same specified student; 
     - counts: having the right counts of total/respeck/thingy recordings before/after cleaning. 
    '''
    def __init__(self, uun: str, path_prefix: str=PREFIX_2023, 
                 gt_counts: dict=GT_COUNTS) -> None:
        
        self.uun = uun
        self.full_path = os.path.join(PREFIX_2023, uun)
        self.files = os.listdir(self.full_path)
        self.gt_counts = gt_counts
        self.gt_raw_counts = {k: int(v / 2) for k, v in self.gt_counts.items()}
    
    def all_checks(self, cleaned: bool=False, verbose: bool=True) -> bool:
        integrity = self.integrity_check()
        if verbose:
            print(f"Integrity: {integrity} for {self.uun}")
        counts = self.count_files()
        target_counts = self.gt_counts if cleaned else self.gt_raw_counts
        if verbose:
            print(f"Counts: {counts}")
            cleaned_str = "cleaned" if cleaned else "uncleaned"
            print(f"Target Counts when {cleaned_str}: {target_counts}")

        
        checks = [integrity, counts == target_counts]
        if all(checks):
            print("All checks passed.")
            return True
        print("Some checks failed, enable 'verbose' to see all checks")
        return False

    def integrity_check(self) -> bool:
        '''
        Checks if all files under this dir belongs to the right student.
        '''
        for file in self.files:
            if self.uun not in file:
                return False
        return True

    def count_files(self) -> Dict[str,int]:
        results = {}
        results["total"] = len(self.files) - 1  # ui_trims
        respecks = 0
        thingys = 0
        for file in self.files:
            if "Respeck" in file:
                respecks += 1
            elif "Thingy" in file:
                thingys += 1
            elif "ui_trims" in file:
                pass
            else:
                raise AssertionError(f"{file} is neither respeck nor thingy recording.")
        results["respecks"] = respecks
        results["thingys"] = thingys
        return results


if __name__ == "__main__":
    student = "s2047783"
    examiner = DataExaminer(student)
    examiner.all_checks(cleaned=False)
    # integrity = examiner.integrity_check()
    # counts = examiner.count_files()
