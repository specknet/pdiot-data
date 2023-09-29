import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog, QListWidgetItem, QHBoxLayout, QLabel, QPushButton, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os
import pandas as pd
import viewer_utils
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.selected_files = ["" for _ in range(3)]
        self.figures = []
        self.folders = ["" for _ in range(3)]
        self.view_cleaned_file = 1  # 0 for unprocessed
        self.filelists = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Matplotlib in PyQt5')
        self.setGeometry(0, 0, 1920, 1080)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局，用于容纳三个区域，并设置比例
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建第一个区域，大小比例为6，用于显示Matplotlib图形
        area1 = QWidget(self)
        area1.setStyleSheet("background-color: red;")  # 设置背景颜色以区分区域
        self.area1 = area1
        layout.addWidget(area1, 15)

        sub_layout = QVBoxLayout(area1)
        # 在第一个区域中添加Matplotlib图形，上下排列
        for i in range(3):
            figure = Figure()
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(121)
            ax = figure.add_subplot(122)
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x)
            ax.plot(x, y)
            sub_layout.addWidget(canvas)
            self.figures.append(figure)

        # 创建第二个区域，大小比例为2
        area2 = QWidget(self)
        area2.setStyleSheet("background-color: green;")
        self.area2 = area2
        layout.addWidget(area2, 3)

        # 创建一个水平布局
        filelist_layout = QHBoxLayout(area2)

        # 创建三个文件列表视图和路径选择按钮
        for i in range(3):
            # 创建一个垂直布局用于容纳文件列表、路径选择按钮和文件列表标题
            row_layout = QVBoxLayout()

            # 创建文件列表标题
            list_title = QLabel(f'List {i + 1}')
            row_layout.addWidget(list_title)

            # 创建文件列表视图
            file_list = QListWidget(self)
            file_list.itemClicked.connect(lambda item, idx=i: self.select_datafile(item, idx=idx))
            self.filelists.append(file_list)
            row_layout.addWidget(file_list)

            # 创建选择路径的按钮
            path_button = QPushButton(f'Select Path for List {i + 1}', self)
            path_button.clicked.connect(lambda state, idx=i, file_list=file_list: self.select_path(idx, file_list))
            row_layout.addWidget(path_button)

            filelist_layout.addLayout(row_layout)

        # 创建第三个区域，大小比例为1
        area3 = QWidget(self)
        area3.setStyleSheet("background-color: blue;")
        layout.addWidget(area3, 1)

        # 在area3中创建一个QPushButton
        toggle_button = QPushButton("Toggle Unprocessed / Clean Data")
        toggle_button.clicked.connect(self.toggle_mode)
        previous_file_button = QPushButton("Previous File", self)
        previous_file_button.clicked.connect(self.previous_file)
        next_file_button = QPushButton("Next File", self)
        next_file_button.clicked.connect(self.next_file)
        layout_in_area3 = QHBoxLayout(area3)
        layout_in_area3.addWidget(toggle_button)
        layout_in_area3.addWidget(previous_file_button)
        layout_in_area3.addWidget(next_file_button)
    
    def toggle_mode(self):
        if self.view_cleaned_file == 1:
            self.view_cleaned_file = 0
        else:
            self.view_cleaned_file = 1
        self.update_files()

    def previous_file(self):
        pass

    def next_file(self):
        pass

    def update_files(self):
        for i in range(3):
            if self.folders[i] == "":
                continue
            self.filelists[i].clear()
            files = os.listdir(self.folders[i])
            for file in files:
                if os.path.isfile(os.path.join(self.folders[i], file)):
                    if self.view_cleaned_file:
                        if "clean" in file:
                            item = QListWidgetItem(file)
                            self.filelists[i].addItem(item)
                    else:
                        if "clean" not in file:
                            item = QListWidgetItem(file)
                            self.filelists[i].addItem(item)
    
    def select_path(self, index, file_list):
        # 打开文件对话框以选择路径
        folder_path = QFileDialog.getExistingDirectory(self, f'Select Folder for List {index + 1}')
        if folder_path:
            # 清空文件列表
            file_list.clear()

            # 获取所选文件夹下的所有文件
            files = os.listdir(folder_path)
            for file in files:
                if os.path.isfile(os.path.join(folder_path, file)):
                    if self.view_cleaned_file:
                        if "clean" in file:
                            item = QListWidgetItem(file)
                            file_list.addItem(item)
                    else:
                        if "clean" not in file:
                            item = QListWidgetItem(file)
                            file_list.addItem(item)
        self.folders[index] = folder_path
    
    def select_datafile(self, item, idx=-1):
        # print(f"{idx} Selected: {item.text()}")
        self.selected_files[idx] = item.text()
        # print(self.selected_files)
        self.resize(1280, 720)
        self.update_plots(idx, item.text())
    
    def update_plots(self, idx, datafile):
        figure = self.figures[idx]
        full_path = os.path.join(
            self.folders[idx], datafile
        )
        cleaned = False
        if "clean" in datafile or "ui_trims" in full_path:
            cleaned = True
        header_size = 0 if cleaned else 5
        df = pd.read_csv(full_path, header=header_size)
        # TODO: check frequency and length as well here? display them
        self._plot_data(figure, df, datafile)
    
    def _plot_data(self, fig: Figure, dataframe: pd.DataFrame, datafile: str):
        axes = fig.get_axes()
        for ax in axes:
            ax.clear()
        num_data_points = len(dataframe)
        figure_width = num_data_points / 10  # Adjust the divisor to control the size
        aspect_ratio = 0.3  # You can adjust this value as needed
        figure_height = figure_width * aspect_ratio
        fig.set_size_inches(figure_width, figure_height)
        plot_title = datafile
        line_width = 1
        # Plot respeck with custom line width
        axes[0].plot(dataframe["accel_x"], label="accel_x", linewidth=line_width)
        axes[0].plot(dataframe["accel_y"], label="accel_y", linewidth=line_width)
        axes[0].plot(dataframe["accel_z"], label="accel_z", linewidth=line_width)
        axes[0].legend()
        # axes[0].set_title(
        #     f"Accelerometer data"
        # )
        # Plot gyroscope data
        axes[1].plot(dataframe["gyro_x"], label="gyro_x", linewidth=line_width)
        axes[1].plot(dataframe["gyro_y"], label="gyro_y", linewidth=line_width)
        axes[1].plot(dataframe["gyro_z"], label="gyro_z", linewidth=line_width)
        axes[1].legend()
        num_xticks = len(dataframe) // 10
        axes[0].xaxis.set_major_locator(ticker.MaxNLocator(num_xticks))
        axes[1].xaxis.set_major_locator(ticker.MaxNLocator(num_xticks))
        fnt_size = 9
        fnt_size2 = 6
        axes[1].set_xlabel(
            "Data point no", fontsize=fnt_size
        )  # Adjust fontsize for the x-axis label
        axes[0].set_ylabel(
            "Acceleration", fontsize=fnt_size
        )  # Adjust fontsize for the y-axis label
        axes[1].set_ylabel("Gyroscope", fontsize=fnt_size)
        # Adjust fontsize of individual ticks on the x-axis and y-axis for both subplots
        axes[0].tick_params(axis="both", labelsize=fnt_size2)
        axes[1].tick_params(axis="both", labelsize=fnt_size2)
        # Rotate x-axis tick labels by 45 degrees for both subplots
        axes[0].tick_params(axis="x", labelrotation=45)
        axes[1].tick_params(axis="x", labelrotation=45)
        # axes[0].set_title(plot_title, size=fnt_size)
        # axes[1].set_title(plot_title, size=fnt_size)
        # Add vertical grid lines (gridlines along the x-axis)
        axes[0].grid(axis="x", linestyle="--", linewidth=line_width)
        axes[1].grid(axis="x", linestyle="--", linewidth=line_width)
        fig.suptitle(plot_title)
        # fig.canvas.figure = fig
        fig.canvas.draw()
        # self.adjustSize()
        # self.showMaximized()
        self.resize(1920, 1080)
        # self.Refresh()
        # self.showMaximized()
        # self.resize(self.size())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
