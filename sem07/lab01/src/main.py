import sys

from PyQt5 import QtWidgets

from matplotlib.backends.backend_qt5agg \
import NavigationToolbar2QT as NavigationToolbar

from gui.mainwindow import Ui_MainWindow

import distributions.tablefuncs as tf

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.autoUniform = True
        self.autoNormal = True

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.widgetUniformDensity.SetTitle('График функции плотности')
        self.ui.widgetUniformDistribution.SetTitle('График функции распределения')
        self.ui.widgetNormalDensity.SetTitle('График функции плотности')
        self.ui.widgetNormalDistribution.SetTitle('График функции распределения')

        self.ui.btnUniformGraph.clicked.connect(self.graphUniformFuncs)

        self.ui.cbUniformAuto.stateChanged.connect(self.cbUniformAutoChanged)
        self.ui.spUniformBtm.setDisabled(self.autoUniform)
        self.ui.spUniformTop.setDisabled(self.autoUniform)

        self.ui.btnNormalGraph.clicked.connect(self.graphNormalFuncs)

        self.ui.cbNormalAuto.stateChanged.connect(self.cbNormalAutoChanged)
        self.ui.spNormalBtm.setDisabled(self.autoNormal)
        self.ui.spNormalTop.setDisabled(self.autoNormal)



    def graphUniformFuncs(self):
        a = self.ui.spinBoxA.value()
        b = self.ui.spinBoxB.value()

        interval = ((self.ui.spUniformBtm.value(), self.ui.spUniformTop.value())
                    if not self.ui.cbUniformAuto.isChecked() else None)

        if a < b:
            if interval is None or interval[0] < interval[1]:
                xDen, yDen = tf.GetUniformDensityTableFunc(a, b, 1000, interval)
                xDist, yDist = tf.GetUniformDistributionTableFunc(a, b, 1000, interval)

                self.ui.widgetUniformDensity.Update(xDen, yDen)
                self.ui.widgetUniformDistribution.Update(xDist, yDist)
            else:
                QtWidgets.QMessageBox.critical(
                        self,
                        "Ошибка",
                        "Нижняя граница должна быть меньше верхней",
                        QtWidgets.QMessageBox.Ok)

        else:
            QtWidgets.QMessageBox.critical(
                    self,
                    "Ошибка",
                    "Коэффициент a должен быть меньше b",
                    QtWidgets.QMessageBox.Ok)


    def graphNormalFuncs(self):
        m = self.ui.spinBoxM.value()
        sigma = self.ui.spinBoxSigma.value()

        interval = ((self.ui.spNormalBtm.value(), self.ui.spNormalTop.value())
                    if not self.ui.cbNormalAuto.isChecked() else None)

        try:
            if interval is None or interval[0] < interval[1]:
                xDen, yDen = tf.GetNormalDensityTableFunc(m, sigma, 1000,
                                                          interval)
                xDist, yDist = tf.GetNormalDistributionTableFunc(m, sigma,
                                                                 1000, interval)

                self.ui.widgetNormalDensity.Update(xDen, yDen)
                self.ui.widgetNormalDistribution.Update(xDist, yDist)
            else:
                QtWidgets.QMessageBox.critical(
                        self,
                        "Ошибка",
                        "Нижняя граница должна быть меньше верхней",
                        QtWidgets.QMessageBox.Ok)

        except Exception as e:
            QtWidgets.QMessageBox.critical(
                    self, "Ошибка", "", QtWidgets.QMessageBox.Ok)


    def cbUniformAutoChanged(self):
        self.autoUniform = not self.autoUniform
        self.ui.spUniformBtm.setDisabled(self.autoUniform)
        self.ui.spUniformTop.setDisabled(self.autoUniform)


    def cbNormalAutoChanged(self):
        self.autoNormal = not self.autoNormal
        self.ui.spNormalBtm.setDisabled(self.autoNormal)
        self.ui.spNormalTop.setDisabled(self.autoNormal)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.showMaximized()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
