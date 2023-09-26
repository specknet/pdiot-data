import pandas as pd
import matplotlib.pyplot as plt
from typing import Tuple, Dict
import matplotlib.ticker as ticker
import os


"""
Copied from and modified based on lab 2, pdiot 2023. (PDIoT_Lab2_data_loading_visualization.ipynb)
"""


def _extract_header_info(filename: str, header_size: int = 5) -> Dict[str, str | int]:
    """
    :param filename: Path to recording file.
    :param header_size: The size of the header, defaults to 5.
    :returns: A dict containing the sensor type, activity type, activity code, subject id and any notes.
    """
    sensor_type = ""
    activity_type = ""
    activity_code = -1
    subject_id = ""
    notes = ""
    with open(filename) as f:
        head = [next(f).rstrip().split("# ")[1] for x in range(header_size)]
        for l in head:
            title, value = l.split(":")
            if title == "Sensor type":
                sensor_type = value.strip()
            elif title == "Activity type":
                activity_type = value.strip()
            elif title == "Activity code":
                activity_code = int(value.strip())
            elif title == "Subject id":
                subject_id = value.strip()
            elif title == "Notes":
                notes = value.strip()
    header_info_dict = {
        "sensor_type": sensor_type,
        "activity_type": activity_type,
        "activity_code": activity_code,
        "subject_id": subject_id,
        "notes": notes,
    }
    return header_info_dict


def read_data_to_df(filename: str, header_size: int = 5) -> pd.DataFrame:
    df = pd.read_csv(filename, header=header_size)
    header_info = _extract_header_info(filename, header_size)
    df = df.assign(**header_info)  # append header info to last cols
    df["recording_id"] = filename.split("/")[-1].split(".")[
        0
    ]  # append filename as recording id
    return df


def get_frequency(dataframe: pd.DataFrame, ts_column: str = "timestamp") -> float:
    """
    :param dataframe: Dataframe containing sensor data. It needs to have a 'timestamp' column.
    :param ts_column: The name of the column containing the timestamps. Default is 'timestamp'.
    :returns: Frequency in Hz (samples per second)
    """

    return len(dataframe) / (
        (dataframe[ts_column].iloc[-1] - dataframe[ts_column].iloc[0]) / 1000
    )


def get_recording_length(dataframe: pd.DataFrame):
    """
    :param dataframe: Dataframe containing sensor data.
    """
    return len(dataframe) / get_frequency(dataframe)


def plot_data(dataframe: pd.DataFrame, plot_title):
    # Calculate the number of data points in your dataset
    num_data_points = len(dataframe)

    # Calculate a suitable figure width based on the number of data points
    # You can adjust the multiplier as needed to control the figure size
    figure_width = num_data_points / 10  # Adjust the divisor to control the size

    # Set a fixed aspect ratio for the figure (optional)
    aspect_ratio = 0.3  # You can adjust this value as needed

    # Calculate the figure height based on the aspect ratio and width
    figure_height = figure_width * aspect_ratio

    # Create the figure with the calculated size
    fig, ax = plt.subplots(2, 1, figsize=(figure_width, figure_height))

    plot_title = plot_title

    line_width = 2

    # Plot respeck with custom line width
    ax[0].plot(dataframe["accel_x"], label="accel_x", linewidth=line_width)
    ax[0].plot(dataframe["accel_y"], label="accel_y", linewidth=line_width)
    ax[0].plot(dataframe["accel_z"], label="accel_z", linewidth=line_width)
    ax[0].legend()

    ax[0].set_title(
        f"{dataframe['sensor_type'].values[0]} - {dataframe['activity_type'].values[0]} \n Accelerometer data"
    )

    # Plot gyroscope data
    ax[1].plot(dataframe["gyro_x"], label="gyro_x", linewidth=line_width)
    ax[1].plot(dataframe["gyro_y"], label="gyro_y", linewidth=line_width)
    ax[1].plot(dataframe["gyro_z"], label="gyro_z", linewidth=line_width)
    ax[1].legend()

    num_xticks = len(dataframe) // 10
    ax[0].xaxis.set_major_locator(ticker.MaxNLocator(num_xticks))
    ax[1].xaxis.set_major_locator(ticker.MaxNLocator(num_xticks))

    fnt_size = 9
    fnt_size2 = 6

    ax[1].set_xlabel(
        "Data point no", fontsize=fnt_size
    )  # Adjust fontsize for the x-axis label
    ax[0].set_ylabel(
        "Acceleration", fontsize=fnt_size
    )  # Adjust fontsize for the y-axis label
    ax[1].set_ylabel("Gyroscope", fontsize=fnt_size)

    # Adjust fontsize of individual ticks on the x-axis and y-axis for both subplots
    ax[0].tick_params(axis="both", labelsize=fnt_size2)
    ax[1].tick_params(axis="both", labelsize=fnt_size2)

    # Rotate x-axis tick labels by 45 degrees for both subplots
    ax[0].tick_params(axis="x", labelrotation=45)
    ax[1].tick_params(axis="x", labelrotation=45)

    ax[0].set_title(plot_title, size=fnt_size)

    # Add vertical grid lines (gridlines along the x-axis)
    ax[0].grid(axis="x", linestyle="--", linewidth=line_width)
    ax[1].grid(axis="x", linestyle="--", linewidth=line_width)

    # plt.tight_layout()
    plt.show()
