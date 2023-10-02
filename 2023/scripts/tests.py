import os
from typing import Dict, List, Tuple
import pandas as pd
import numpy as np


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
TIME_LIMITS = {
    "min": 25 * 28,
    "max": 25 * 32
}
FREQUENCY = 25.0
FREQUENCY_TOLERANCE = 0.01


# FUNCTIONS
class DataExaminer():
    '''
    Checks for: 
     - file integrity: all files belongs to same specified student; 
     - counts: having the right counts of total/respeck/thingy recordings before/after cleaning. 
    '''
    def __init__(self, uun: str, path_prefix: str=PREFIX_2023, 
                 gt_counts: dict=GT_COUNTS, 
                 time_limits: dict=TIME_LIMITS, 
                 frequency: float=FREQUENCY, 
                 freq_tol: float=FREQUENCY_TOLERANCE) -> None:
        
        self.uun = uun
        self.full_path = os.path.join(PREFIX_2023, uun)
        self.files = os.listdir(self.full_path)
        self.gt_counts = gt_counts
        self.gt_raw_counts = {k: int(v / 2) for k, v in self.gt_counts.items()}
        self.time_limits = time_limits
        self.frequency = frequency
        self.freq_tol = freq_tol
    
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
        results["total"] = len(self.files)
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
    
    def _read_data(self, filename: str, header_size=0) -> pd.DataFrame:
        full_path = os.path.join(self.full_path, filename)
        df = pd.read_csv(full_path, header=header_size)
        return df

    def length_checks(self) -> Tuple[Dict[str,int], Dict[str,int]]:
        shorts = {}
        longs = {}
        for file in self.files:
            if "clean" in file:
                header = 0
            elif "unprocessed" in file:
                continue
            else:
                print(f"{file} is labeled neither unprocessed nor clean. Skipping reading it.")
                continue
            df = self._read_data(file, header)
            length = df.index.stop - df.index.start
            if length < self.time_limits["min"]:
                shorts[file] = length
            elif length > self.time_limits["max"]:
                longs[file] = length
        return shorts, longs
    
    def _get_frequency(self, dataframe: pd.DataFrame, ts_column: str = 'timestamp') -> float:
        """
        :param dataframe: Dataframe containing sensor data. It needs to have a 'timestamp' column.
        :param ts_column: The name of the column containing the timestamps. Default is 'timestamp'.
        :returns: Frequency in Hz (samples per second)
        """

        return len(dataframe) / ((dataframe[ts_column].iloc[-1] - dataframe[ts_column].iloc[0]) / 1000)
    
    def frequency_checks(self) -> Dict[str, float]:
        invalid_freqs = {}
        for file in self.files:
            if "clean" in file:
                header = 0
            elif "unprocessed" in file:
                continue
            else:
                print(f"{file} is labeled neither unprocessed nor clean. Skipping reading it.")
                continue
            df = self._read_data(file, header)
            freq = self._get_frequency(df)
            if not np.isclose(freq, self.frequency, self.freq_tol):
                invalid_freqs[file] = freq
        return invalid_freqs



if __name__ == "__main__":
    student = "s2047783"
    examiner = DataExaminer(student)
    # examiner.all_checks(cleaned=True)
    # integrity = examiner.integrity_check()
    # counts = examiner.count_files()
    # lengths = examiner.length_checks()
    freqs = examiner.frequency_checks()
    print(freqs)
