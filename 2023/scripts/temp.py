import sys
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

from viewer import DataViewer

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Create the matplotlib FigureCanvas object,
        # which defines a single set of axes as self.axes.
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])
        # student = "s2047783"
        # datafile = "Respeck_s2047783_Ascending stairs_Normal_21-09-2023_12-25-57.csv"
        # viewer = DataViewer(student)
        # viewer.view_data(datafile)

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

        # Create layout for input boxes and buttons
        input_layout = QtWidgets.QHBoxLayout()
        input_layout.addWidget(self.label1)
        input_layout.addWidget(self.input1)
        input_layout.addWidget(self.label2)
        input_layout.addWidget(self.input2)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.process_button)

        # Create a central widget and add layout
        central_widget = QtWidgets.QWidget(self)
        central_layout = QtWidgets.QVBoxLayout()
        central_layout.addWidget(self.sc)
        central_layout.addLayout(input_layout)
        central_layout.addLayout(button_layout)
        central_widget.setLayout(central_layout)

        self.setCentralWidget(central_widget)
        self.show()

    def record_values(self):
        # This method can be populated to record the input values
        value1 = self.input1.text()
        value2 = self.input2.text()
        print("Recorded Values:", value1, value2)

    def process_values(self):
        # This method can be populated to carry out some action with the recorded values
        print("Processing Recorded Values")

app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
