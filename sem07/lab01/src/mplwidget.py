from PyQt5.QtWidgets import QVBoxLayout, QWidget

from matplotlib.backends.backend_qt5agg \
import FigureCanvas
#, NavigationToolbar2QT as NavigationToolbar

from matplotlib.figure import Figure


class MplWidget(QWidget):
    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)

        self.canvas.axes = self.canvas.figure.add_subplot(111)
        self.canvas.figure.tight_layout()
        #self.canvas.axes.plot([1, 2, 3, 4], [1, 2, 3, 4])
        self.setLayout(layout)


    def SetTitle(self, title):
        self.canvas.axes.set_title(title)

