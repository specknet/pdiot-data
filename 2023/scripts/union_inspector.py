import sys
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # 设置主窗口标题
        self.setWindowTitle('Matplotlib Figures in PyQt5')

        # 设置窗口尺寸
        self.setGeometry(100, 100, 800, 600)

        # 创建一个主窗口中的中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局
        layout = QVBoxLayout(central_widget)

        # 创建三个Matplotlib图表
        for i in range(3):
            figure = Figure()
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x)
            ax.plot(x, y)
            layout.addWidget(canvas)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
