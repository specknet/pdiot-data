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

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, dataframe, plot_title):
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        # super(MplCanvas, self).__init__(fig)

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

        line_width = 2

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
        
        # plt.tight_layout()
        # plt.show()

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        student = "s2047783"
        datafile = "Respeck_s2047783_Ascending stairs_Normal_21-09-2023_12-25-57.csv"
        viewer = DataViewer(student)
        data = viewer.load_data(datafile)

        # Create the matplotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        # self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        # self.sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        self.sc = MplCanvas(data, datafile)

        # Create labels and input boxes for integers
        self.label1 = QtWidgets.QLabel("Trim Start Index:")
        self.input1 = QtWidgets.QLineEdit(self)
        self.label2 = QtWidgets.QLabel("Trim End Index:")
        self.input2 = QtWidgets.QLineEdit(self)
        self.input2.setValidator(QtGui.QIntValidator())  # Only allow integer input

        # Create buttons
        self.record_button = QtWidgets.QPushButton("Record Trim Indexes")
        self.record_button.clicked.connect(self.record_values)
        self.process_button = QtWidgets.QPushButton("Trim All")
        self.process_button.clicked.connect(self.process_values)

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

        # Create a central widget and add layouts
        central_widget = QtWidgets.QWidget(self)
        central_layout = QtWidgets.QVBoxLayout()
        central_layout.addWidget(self.sc)
        central_layout.addLayout(input_layout)
        central_layout.addLayout(button_layout)
        central_layout.addWidget(self.recorded_values_text)  # Add the QTextEdit
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)
        self.show()

        self.recorded_values = []  # To store recorded values

    def record_values(self):
        value1 = self.input1.text()
        value2 = self.input2.text()
        self.recorded_values.append((value1, value2))
        self.update_recorded_values_text()

    def process_values(self):
        # This method can be populated to carry out some action with the recorded values
        print("Processing Recorded Values")
        print(self.recorded_values)

    def update_recorded_values_text(self):
        # Update the QTextEdit widget to display recorded values
        self.recorded_values_text.clear()
        for values in self.recorded_values:
            self.recorded_values_text.append(f"Value 1: {values[0]}, Value 2: {values[1]}")

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()