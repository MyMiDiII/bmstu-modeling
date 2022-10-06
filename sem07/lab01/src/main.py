import sys

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg \
import NavigationToolbar2QT as NavigationToolbar

from mainwindow import Ui_MainWindow

import graphics as gr

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.widgetUniformDensity.SetTitle('График функции плотности')
        self.ui.widgetUniformDistribution.SetTitle('График функции распределения')
        self.ui.widgetNormalDensity.SetTitle('График функции плотности')
        self.ui.widgetNormalDistribution.SetTitle('График функции распределения')

        self.ui.btnUniformGraph.clicked.connect(self.graphUniformFuncs)
        self.ui.btnNormalGraph.clicked.connect(self.graphNormalFuncs)
        #self.addToolBar(NavigationToolbar(self.ui.widgetUniformDensity.canvas, self))
        #self.addToolBar(NavigationToolbar(self.ui.widgetUniformDistribution.canvas, self))


    def graphUniformFuncs(self):
        x, y = gr.GetUniformTableFunc()


    def graphNormalFuncs(self):


def main():
    app = QtWidgets.QApplication(sys.argv)
    #app.setStyle('Breeze')
    main = MainWindow()
    main.showMaximized()
    #main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
