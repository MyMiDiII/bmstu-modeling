from PyQt5.QtWidgets import QVBoxLayout, QWidget

from matplotlib.backends.backend_qt5agg \
import FigureCanvas, NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure


class MplWidget(QWidget):
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.figure.tight_layout()
        self.canvas.figure.subplots_adjust(left=0.133, right=0.995)

        layout.addWidget(NavigationToolbar(self.canvas, parent))

        self.setLayout(layout)

        self.title = ""



    def SetTitle(self, title):
        self.title = title
        self.canvas.axes.set_title(title)


    def Update(self, x, y):
        self.canvas.axes.clear()
        self.SetTitle(self.title)
        self.canvas.axes.plot(x, y)
        self.canvas.axes.grid()
        self.canvas.draw()

