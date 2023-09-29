import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Three Areas with Ratios 6:2:1')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局，用于容纳三个区域，并设置比例
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建第一个区域，大小比例为6
        area1 = QWidget(self)
        area1.setStyleSheet("background-color: red;")  # 设置背景颜色以区分区域
        layout.addWidget(area1, 6)

        # 创建第二个区域，大小比例为2
        area2 = QWidget(self)
        area2.setStyleSheet("background-color: green;")
        layout.addWidget(area2, 2)

        # 创建第三个区域，大小比例为1
        area3 = QWidget(self)
        area3.setStyleSheet("background-color: blue;")
        layout.addWidget(area3, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
