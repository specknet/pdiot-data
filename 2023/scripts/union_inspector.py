import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 设置主窗口标题
        self.setWindowTitle('Three Vertical Areas')

        # 设置窗口尺寸
        self.setGeometry(100, 100, 400, 300)

        # 创建一个主窗口中的中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局
        layout = QVBoxLayout(central_widget)

        # 创建第一个区域，大小比例为3
        label1 = QLabel('Area 1 (3x)', self)
        layout.addWidget(label1, 6)  # 3表示分配更多的空间

        # 创建第二个区域，大小比例为1
        label2 = QLabel('Area 2 (1x)', self)
        layout.addWidget(label2, 2)

        # 创建第三个区域，大小比例为0.5
        label3 = QLabel('Area 3 (0.5x)', self)
        layout.addWidget(label3, 1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
