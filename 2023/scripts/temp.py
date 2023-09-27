import os
import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSplitter, QListWidget, QTextBrowser, QListWidgetItem, QPushButton, QTableWidget, QTableWidgetItem, QTableView
from PyQt5.QtGui import QPixmap, QIcon, QStandardItemModel, QStandardItem  # Corrected import here
from PyQt5.QtCore import Qt

class ImageViewer(QMainWindow):
    def __init__(self, folder_a, folder_b, csv_file_1, csv_file_2):
        super().__init__()
        self.folder_a = folder_a
        self.folder_b = folder_b
        self.csv_file_1 = csv_file_1
        self.csv_file_2 = csv_file_2
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 1200, 800)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Create a horizontal layout for the title labels
        title_layout = QHBoxLayout()

        # Add title label for image list from folder B
        label_b = QLabel("Original Images", self)
        title_layout.addWidget(label_b)

        # Add title label for image list from folder A
        label_a = QLabel("Rebuilt Images", self)
        title_layout.addWidget(label_a)

        # Add the title labels to the main layout
        layout.addLayout(title_layout)

        # Create a horizontal layout for the lists
        list_layout = QHBoxLayout()

        # Left side: List of images from folder B
        self.list_widget_b = QListWidget(self)
        self.populate_b_list()
        self.list_widget_b.currentItemChanged.connect(self.show_image_b)
        list_layout.addWidget(self.list_widget_b)

        # Right side: List of images from folder A
        self.list_widget_a = QListWidget(self)
        self.populate_a_list()
        self.list_widget_a.currentItemChanged.connect(self.show_image_a)
        list_layout.addWidget(self.list_widget_a)

        # Add the list layout to the main layout
        layout.addLayout(list_layout)

        splitter = QSplitter(Qt.Horizontal)
        layout.addWidget(splitter)

        # Bottom: Show two images side by side
        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        self.label_image_b = QLabel(self)
        bottom_layout.addWidget(self.label_image_b)

        self.label_image_a = QLabel(self)
        bottom_layout.addWidget(self.label_image_a)

        # Buttons to synchronize image selection
        self.sync_button_up = QPushButton("Up", self)
        self.sync_button_down = QPushButton("Down", self)
        self.sync_button_up.clicked.connect(self.sync_selection_up)
        self.sync_button_down.clicked.connect(self.sync_selection_down)

        bottom_layout.addWidget(self.sync_button_up)
        bottom_layout.addWidget(self.sync_button_down)

        # Functionality area: Table to show data from CSV files
        self.table_view = QTableView(self)
        layout.addWidget(self.table_view)

        # Load CSV files and display data
        self.load_csv_files()
        self.update_table_data()

        self.show()

    def populate_b_list(self):
        for filename in os.listdir(self.folder_b):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                # Check if the image also exists in folder A
                if os.path.exists(os.path.join(self.folder_a, filename)):
                    item = QListWidgetItem(filename)
                    item.setIcon(QIcon(os.path.join(self.folder_b, filename)))
                    self.list_widget_b.addItem(item)

    def populate_a_list(self):
        for filename in os.listdir(self.folder_a):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                item = QListWidgetItem(filename)
                item.setIcon(QIcon(os.path.join(self.folder_a, filename)))
                self.list_widget_a.addItem(item)

    def show_image_b(self, item):
        if item is not None:
            filename = item.text()
            image_path = os.path.join(self.folder_b, filename)
            pixmap = QPixmap(image_path)
            self.label_image_b.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

            # Update functionality area (table) when image selection changes
            self.update_table_data()

    def show_image_a(self, item):
        if item is not None:
            filename = item.text()
            image_path = os.path.join(self.folder_a, filename)
            pixmap = QPixmap(image_path)
            self.label_image_a.setPixmap(pixmap.scaled(400, 400, Qt.KeepAspectRatio))

            # Update functionality area (table) when image selection changes
            self.update_table_data()

    def sync_selection_up(self):
        a_current = self.list_widget_a.currentRow()
        b_current = self.list_widget_b.currentRow()
        if a_current - 1 >= 0:
            self.list_widget_a.setCurrentRow(a_current - 1)
        if b_current - 1 >= 0:
            self.list_widget_b.setCurrentRow(b_current - 1)

    def sync_selection_down(self):
        a_current = self.list_widget_a.currentRow()
        b_current = self.list_widget_b.currentRow()
        if a_current + 1 < self.list_widget_a.count():
            self.list_widget_a.setCurrentRow(a_current + 1)
        if b_current + 1 < self.list_widget_b.count():
            self.list_widget_b.setCurrentRow(b_current + 1)

    def load_csv_files(self):
        self.csv_data_1 = {}
        self.csv_data_2 = {}

        if os.path.exists(self.csv_file_1):
            with open(self.csv_file_1, 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if len(row) > 0:
                        self.csv_data_1[row[0]] = row[1:]

        if os.path.exists(self.csv_file_2):
            with open(self.csv_file_2, 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    if len(row) > 0:
                        self.csv_data_2[row[0]] = row[1:]

    def update_table_data(self):
        current_image_b = self.list_widget_b.currentItem()
        current_image_a = self.list_widget_a.currentItem()

        if current_image_b and current_image_a:
            filename_b = current_image_b.text()
            filename_a = current_image_a.text()

            data_b = self.csv_data_1.get(filename_b, [])
            data_a = self.csv_data_2.get(filename_a, [])

            num_rows = max(len(data_b), len(data_a))

            model = QStandardItemModel(2, num_rows)  # Transpose rows and columns
            model.setVerticalHeaderLabels(['Original Params', 'Regressed Params'])

            for i in range(num_rows):
                item_b = QStandardItem(f"{float(data_b[i]):.3f}" if i < len(data_b) else "")
                item_a = QStandardItem(f"{float(data_a[i]):.3f}" if i < len(data_a) else "")
                model.setItem(0, i, item_b)  # Use 0 and 1 as the row indices
                model.setItem(1, i, item_a)

            self.table_view.setModel(model)
            self.table_view.resizeColumnsToContents()  # Resize columns to fit content


if __name__ == "__main__":
    app = QApplication(sys.argv)
    dataset_name = "tr-bmcc-1000"
    folder_a = "./data/outputs/" + dataset_name + "_out/"  # output
    folder_b = "./data/massroof0801/" + dataset_name + "/images/"
    csv_file_1 = "./data/massroof0801/" + dataset_name + "/" + dataset_name + ".csv"
    csv_file_2 = "./data/outputs/" + dataset_name + "_out.csv"  # output
    image_viewer = ImageViewer(folder_a, folder_b, csv_file_1, csv_file_2)
    sys.exit(app.exec_())
