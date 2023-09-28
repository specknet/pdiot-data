import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 设置主窗口标题
        self.setWindowTitle('PyQt5 Template')

        # 设置窗口尺寸
        self.setGeometry(0, 0, 500, 500)

        # 创建一个标签
        self.label = QLabel('Hello, PyQt5!', self)
        self.label.setGeometry(150, 150, 200, 50)

        # 创建一个按钮
        self.button = QPushButton('Click Me', self)
        self.button.setGeometry(150, 200, 100, 30)

        # 按钮点击事件处理
        self.button.clicked.connect(self.on_button_click)

    def on_button_click(self):
        # 处理按钮点击事件
        self.label.setText('Button Clicked!')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.showMaximized()
    sys.exit(app.exec_())
