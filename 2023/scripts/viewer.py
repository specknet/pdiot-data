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
    
    def load_data(self, filename: str) -> pd.DataFrame:
        full_filepath = os.path.join(self.full_path, filename)
        header = 0 if "ui_trims" in filename else 5
        return read_data_to_df(full_filepath, header)

    def view_data(self, filename: str) -> None:
        full_filepath = os.path.join(self.full_path, filename)
        header = 0 if "ui_trims" in filename else 5  # cleaned data does not have header
        df = read_data_to_df(full_filepath, header_size=header)
        print(df.index.start)
        print(df.index.stop)
        plot_data(
            df, plot_title=filename
        )


if __name__ == "__main__":
    student = "s2047783"
    datafile = "./ui_trims/Thingy_s2047783_Sitting_Normal_22-09-2023_15-10-06.csv"
    # datafile = "Respeck_s2047783_Lying down back_Hyperventilating_21-09-2023_16-01-10.csv"
    viewer = DataViewer(student)
    viewer.view_data(datafile)
