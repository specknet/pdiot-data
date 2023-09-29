import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 初始化Matplotlib图表列表
        self.matplotlib_figures = []

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Matplotlib in PyQt5')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建一个垂直布局，用于容纳Matplotlib图表
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # 创建三个Matplotlib图表，并将它们添加到布局中
        for i in range(3):
            figure = Figure()
            canvas = FigureCanvas(figure)
            ax = figure.add_subplot(111)
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x)
            ax.plot(x, y)
            layout.addWidget(canvas)

            # 将Matplotlib图表添加到列表中
            self.matplotlib_figures.append(figure)

        # 创建一个按钮，用于触发更新图表的操作
        update_button = QPushButton('Update Charts', self)
        update_button.clicked.connect(self.update_charts)
        layout.addWidget(update_button)

    def update_charts(self):
        # 在这个方法中，你可以通过self.matplotlib_figures访问之前创建的Matplotlib图表
        for i, figure in enumerate(self.matplotlib_figures):
            ax = figure.get_axes()[0]  # 获取图表的第一个子图
            x = np.linspace(0, 2 * np.pi, 100)
            y = np.sin(x + i)  # 根据需要更新y值
            ax.clear()  # 清空图表内容
            ax.plot(x, y)  # 绘制新数据
            ax.set_title(f'Chart {i + 1}')  # 更新图表标题
            figure.canvas.draw()  # 重新绘制图表

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
