import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Selection Example')
        self.setGeometry(100, 100, 400, 200)

        # 创建按钮，用于触发文件选择对话框
        select_button = QPushButton('Select File', self)
        select_button.setGeometry(150, 50, 100, 30)
        select_button.clicked.connect(self.select_file)

    def select_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # 可以添加其他选项

        # 打开文件选择对话框以选择文件
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select File', '', 'All Files (*)', options=options)

        if file_path:
            # 用户选择了文件
            print('Selected file:', file_path)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
