import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListView, QPushButton, QFileDialog, QHBoxLayout, QListWidget, QListWidgetItem, QLabel
from PyQt5.QtCore import Qt, QModelIndex

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 设置主窗口标题
        self.setWindowTitle('File Selection')

        # 设置窗口尺寸
        self.setGeometry(100, 100, 800, 600)

        # 创建一个主窗口中的中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局
        layout = QVBoxLayout(central_widget)

        # 创建三个文件列表视图和路径选择按钮
        for i in range(3):
            # 创建一个水平布局用于容纳文件列表、路径选择按钮和文件列表标题
            row_layout = QHBoxLayout()

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

            layout.addLayout(row_layout)

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
