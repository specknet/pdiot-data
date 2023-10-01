import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from viewer import DataViewer
import viewer_utils
import os
from PyQt5.QtWidgets import QMessageBox

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, dataframe, plot_title):
        self.dataframe = dataframe
        self.plot_title = plot_title
        # taken from and modified based plot_data()
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
        # fig, ax = plt.subplots(2, 1, figsize=(figure_width, figure_height))

        fig = Figure(figsize=(figure_width, figure_height)) # dpi? 
        self.ax1 = fig.add_subplot(211)
        self.ax2 = fig.add_subplot(212)
        super(MplCanvas, self).__init__(fig)

        plot_title = plot_title

        line_width = 1

        # Plot respeck with custom line width
        self.ax1.plot(dataframe["accel_x"], label="accel_x", linewidth=line_width)
        self.ax1.plot(dataframe["accel_y"], label="accel_y", linewidth=line_width)
        self.ax1.plot(dataframe["accel_z"], label="accel_z", linewidth=line_width)
        self.ax1.legend()

        self.ax1.set_title(
            f"{dataframe['sensor_type'].values[0]} - {dataframe['activity_type'].values[0]} \n Accelerometer data"
        )

        # Plot gyroscope data
        self.ax2.plot(dataframe["gyro_x"], label="gyro_x", linewidth=line_width)
        self.ax2.plot(dataframe["gyro_y"], label="gyro_y", linewidth=line_width)
        self.ax2.plot(dataframe["gyro_z"], label="gyro_z", linewidth=line_width)
        self.ax2.legend()

        num_xticks = len(dataframe) // 10
        self.ax1.xaxis.set_major_locator(ticker.MaxNLocator(num_xticks))
        self.ax2.xaxis.set_major_locator(ticker.MaxNLocator(num_xticks))

        fnt_size = 9
        fnt_size2 = 6

        self.ax2.set_xlabel(
            "Data point no", fontsize=fnt_size
        )  # Adjust fontsize for the x-axis label
        self.ax1.set_ylabel(
            "Acceleration", fontsize=fnt_size
        )  # Adjust fontsize for the y-axis label
        self.ax2.set_ylabel("Gyroscope", fontsize=fnt_size)

        # Adjust fontsize of individual ticks on the x-axis and y-axis for both subplots
        self.ax1.tick_params(axis="both", labelsize=fnt_size2)
        self.ax2.tick_params(axis="both", labelsize=fnt_size2)

        # Rotate x-axis tick labels by 45 degrees for both subplots
        self.ax1.tick_params(axis="x", labelrotation=45)
        self.ax2.tick_params(axis="x", labelrotation=45)

        self.ax1.set_title(plot_title, size=fnt_size)

        # Add vertical grid lines (gridlines along the x-axis)
        self.ax1.grid(axis="x", linestyle="--", linewidth=line_width)
        self.ax2.grid(axis="x", linestyle="--", linewidth=line_width)
    
    def update_plot(self, new_data):
        self.dataframe = new_data
        # Clear existing plots
        self.ax1.clear()
        self.ax2.clear()

        # Update the plots with new data
        line_width = 1
        self.ax1.plot(new_data["accel_x"], label="accel_x", linewidth=line_width)
        self.ax1.plot(new_data["accel_y"], label="accel_y", linewidth=line_width)
        self.ax1.plot(new_data["accel_z"], label="accel_z", linewidth=line_width)
        self.ax1.legend()

        self.ax1.set_title(
            f"{new_data['sensor_type'].values[0]} - {new_data['activity_type'].values[0]} \n Accelerometer data"
        )

        self.ax2.plot(new_data["gyro_x"], label="gyro_x", linewidth=line_width)
        self.ax2.plot(new_data["gyro_y"], label="gyro_y", linewidth=line_width)
        self.ax2.plot(new_data["gyro_z"], label="gyro_z", linewidth=line_width)
        self.ax2.legend()

        num_xticks = len(new_data) // 10
        self.ax1.xaxis.set_major_locator(ticker.MaxNLocator(num_xticks))
        self.ax2.xaxis.set_major_locator(ticker.MaxNLocator(num_xticks))

        fnt_size = 9
        fnt_size2 = 6

        self.ax2.set_xlabel(
            "Data point no", fontsize=fnt_size
        )  # Adjust fontsize for the x-axis label
        self.ax1.set_ylabel(
            "Acceleration", fontsize=fnt_size
        )  # Adjust fontsize for the y-axis label
        self.ax2.set_ylabel("Gyroscope", fontsize=fnt_size)

        # Adjust fontsize of individual ticks on the x-axis and y-axis for both subplots
        self.ax1.tick_params(axis="both", labelsize=fnt_size2)
        self.ax2.tick_params(axis="both", labelsize=fnt_size2)

        # Rotate x-axis tick labels by 45 degrees for both subplots
        self.ax1.tick_params(axis="x", labelrotation=45)
        self.ax2.tick_params(axis="x", labelrotation=45)

        self.ax1.set_title(self.plot_title, size=fnt_size)

        # Add vertical grid lines (gridlines along the x-axis)
        self.ax1.grid(axis="x", linestyle="--", linewidth=line_width)
        self.ax2.grid(axis="x", linestyle="--", linewidth=line_width)

        # Redraw the canvas
        self.draw()


class MainWindow(QtWidgets.QMainWindow):
    # TODO: automatically trim final df to 750 (30s)
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.student = "s2047783"
        self.datafile = "Respeck_s2047783_Lying down on left_Hyperventilating_unprocessed_01-10-2023_13-45-20" + ".csv"
        self.viewer = DataViewer(self.student)
        self.data = self.viewer.load_data(self.datafile)
        self.index_min = self.data.index.start
        self.index_max = self.data.index.stop

        # Create the matplotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        # self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        # self.sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.sc = MplCanvas(self.data, self.datafile)

        # Create labels and input boxes for integers
        self.label1 = QtWidgets.QLabel("Trim Start:")
        self.input1 = QtWidgets.QLineEdit(self)
        self.label2 = QtWidgets.QLabel("Trim End:")
        self.input2 = QtWidgets.QLineEdit(self)
        self.input1.setValidator(QtGui.QIntValidator())
        self.input2.setValidator(QtGui.QIntValidator())  # Only allow integer input

        # Create buttons
        self.record_button = QtWidgets.QPushButton("Record Trim")
        self.record_button.clicked.connect(self.record_values)
        self.process_button = QtWidgets.QPushButton("Apply Recorded Trims")
        self.process_button.clicked.connect(self.process_values)
        
        self.save_button = QtWidgets.QPushButton("Save Trimmed Csv")
        self.save_button.clicked.connect(self.save_csv)

        self.undo_button = QtWidgets.QPushButton("Remove Last Record")
        self.undo_button.clicked.connect(self.remove_record)

        # Create a QTextEdit widget to display recorded values
        self.recorded_values_text = QtWidgets.QTextEdit(self)
        self.recorded_values_text.setReadOnly(True)

        # Create layout for input boxes and buttons
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.addWidget(self.label1)
        input_layout.addWidget(self.input1)
        input_layout.addWidget(self.label2)
        input_layout.addWidget(self.input2)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.undo_button)

        # Create a central widget and add layouts
        central_widget = QtWidgets.QWidget(self)
        central_layout = QtWidgets.QVBoxLayout()
        central_layout.addWidget(self.sc)
        central_layout.addLayout(input_layout)
        central_layout.addLayout(button_layout)
        central_layout.addWidget(self.recorded_values_text)  # Add the QTextEdit
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)
        # self.show()
        self.showMaximized()

        self.recorded_values = []  # To store recorded values

        # Bind Enter key to trigger "Record Values" button click
        self.input1.returnPressed.connect(self.record_button.click)
        self.input2.returnPressed.connect(self.record_button.click)
    
    def remove_record(self):
        if len(self.recorded_values) == 0:
            self.throw_warning("Nothing recorded so far, cannot remove records. ")
            return
        removed = self.recorded_values.pop()
        self.update_recorded_values_text()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Removed last record")
        msg.setInformativeText(f"Removed values: {removed}")
        msg.setWindowTitle("Undo")
        msg.exec_()

    def throw_warning(self, txt: str):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error")
        msg.setInformativeText(txt)
        msg.setWindowTitle("Error")
        msg.exec_()

    def record_values(self):
        value1 = self.input1.text()
        value2 = self.input2.text()
        if value1 == "" or value2 == "":
            self.throw_warning(f"Empty Value encountered: {value1}, {value2}")
            return
        # int checks done by pyqt QIntValidator
        try: 
            value1 = int(value1)
            value2 = int(value2)
        except:
            self.throw_warning(f"Unexpected Input: {value1}, {value2}")
            return
        if value1 < self.index_min or value1 > self.index_max + 50:
            self.throw_warning(f"{value1} is out of index bounds: {self.index_min} ~ {self.index_max} (+50)")
            return
        if value2 < self.index_min or value2 > self.index_max + 50:
            self.throw_warning(f"{value2} is out of index bounds: {self.index_min} ~ {self.index_max} (+50)")
            return
        self.recorded_values.append((value1, value2))
        self.update_recorded_values_text()

    def process_values(self):
        # This method can be populated to carry out some action with the recorded values
        print("Processing Recorded Values")
        print(self.recorded_values)

        # df_respeck['ind'] = df_respeck.index
        self.data['ind'] = self.data.index
        to_trim = len(self.recorded_values)
        for i in range(int(to_trim)):
            range_trim_start = self.recorded_values[i][0]
            range_trim_end = self.recorded_values[i][1]
            # df_respeck = df_respeck[~((df_respeck['ind'] >= range_trim_start) & (df_respeck['ind'] <= range_trim_end))]
            self.data = self.data[~((self.data['ind'] >= range_trim_start) & (self.data['ind'] <= range_trim_end))]
        self.data.reset_index(inplace=True, drop=True)
        self.index_min = self.data.index.start
        self.index_max = self.data.index.stop

        # Define the starting timestamp in milliseconds
        start_timestamp_ms = self.data.timestamp[0]

        # Define the number of timestamps you want to generate
        num_timestamps = len(self.data)

        # Calculate the time interval between timestamps in microseconds
        microseconds_per_timestamp = int(1e6 / 25)

        # Initialize a list to store the generated timestamps
        timestamps = []

        # Generate the timestamps
        for i in range(num_timestamps):
            timestamp = start_timestamp_ms + i * microseconds_per_timestamp // 1000  # Convert microseconds to milliseconds
            timestamps.append(timestamp)

        # Print the generated timestamps
        # for timestamp in timestamps:
        #    formatted_time = datetime.datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S.%f')
        #    print(timestamp, formatted_time[:-3])  # Print the timestamp with milliseconds

        self.data['timestamp'] = timestamps

        # Update the plot in self.sc with the modified data
        self.sc.update_plot(self.data)
        self.recorded_values.clear()
        self.recorded_values_text.clear()
    
    def save_csv(self):
        save_folder = os.path.join(self.viewer.full_path, "./ui_trims")
        if not os.path.exists(save_folder):
            os.mkdir(save_folder)
        if not "ui_trims" in self.datafile:
            filepath = os.path.join(self.viewer.full_path, "./ui_trims", self.datafile)
        else:
            filepath = os.path.join(self.viewer.full_path, self.datafile)
        self.data.to_csv(filepath, index=False)

    def update_recorded_values_text(self):
        # Update the QTextEdit widget to display recorded values
        self.recorded_values_text.clear()
        for values in self.recorded_values:
            self.recorded_values_text.append(f"Trim Start: {values[0]}, Trim End: {values[1]}")

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()