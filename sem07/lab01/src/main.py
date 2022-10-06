import sys

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg \
import NavigationToolbar2QT as NavigationToolbar

from mainwindow import Ui_MainWindow

import tablefuncs as tf

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
        a = self.ui.spinBoxA.value()
        b = self.ui.spinBoxB.value()

        if a < b:
            xDen, yDen = tf.GetUniformDensityTableFunc(a, b, 1000)
            xDist, yDist = tf.GetUniformDistributionTableFunc(a, b, 1000)

            self.ui.widgetUniformDensity.Update(xDen, yDen)
            self.ui.widgetUniformDistribution.Update(xDist, yDist)
        else:
            QtWidgets.QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Коэффициент a должен быть меньше b",
                    QtWidgets.QMessageBox.Ok)



    def graphNormalFuncs(self):
        m = self.ui.spinBoxM.value()
        sigma = self.ui.spinBoxSigma.value()

        try:
            xDen, yDen = tf.GetNormalDensityTableFunc(m, sigma, 1000)
            xDist, yDist = tf.GetNormalDistributionTableFunc(m, sigma, 1000)

            self.ui.widgetNormalDensity.Update(xDen, yDen)
            self.ui.widgetNormalDistribution.Update(xDist, yDist)
        except Exception as e:
            print(e.args)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
