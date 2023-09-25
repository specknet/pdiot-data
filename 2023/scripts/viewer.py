from viewer_utils import *


# CONSTANTS #
PREFIX_2023 = os.getcwd()
if PREFIX_2023[-4:] == "data":
    PREFIX_2023 = os.path.join(
        PREFIX_2023, "2023"
    )


# FUNCTIONS
class DataViewer():
    '''
    Not to be confused with the actual data cleaning process. 
    It only removes redundant thingy recordings. 
    '''
    def __init__(self, uun: str) -> None:
        self.uun = uun
        self.full_path = os.path.join(PREFIX_2023, uun)
        self.files = os.listdir(self.full_path)
    
    def view_data(self, filename: str) -> None:
        full_filepath = os.path.join(self.full_path, filename)
        plot_data(
            read_data_to_df(full_filepath), plot_title=filename
        )


if __name__ == "__main__":
    student = "s2047783"
    datafile = "Respeck_s2047783_Ascending stairs_Normal_21-09-2023_12-25-57.csv"
    viewer = DataViewer(student)
    viewer.view_data(datafile)
