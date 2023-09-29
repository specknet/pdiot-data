import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QFileDialog, QListWidgetItem, QHBoxLayout, QLabel, QPushButton, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import os

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Matplotlib in PyQt5')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局，用于容纳三个区域，并设置比例
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建第一个区域，大小比例为6，用于显示Matplotlib图形
        area1 = QWidget(self)
        area1.setStyleSheet("background-color: red;")  # 设置背景颜色以区分区域
        layout.addWidget(area1, 6)

        sub_layout = QVBoxLayout(area1)
        # 在第一个区域中添加Matplotlib图形，上下排列
        for i in range(3):
            figure = Figure()
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x)
            ax.plot(x, y)

            # 创建一个垂直布局，用于放置Matplotlib图形
            
            sub_layout.addWidget(canvas)

        # 创建第二个区域，大小比例为2
        area2 = QWidget(self)
        area2.setStyleSheet("background-color: green;")
        layout.addWidget(area2, 2)

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
                    item = QListWidgetItem(file)
                    file_list.addItem(item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
