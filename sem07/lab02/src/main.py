import sys
import random

import numpy as np
import networkx as nx
import scipy as sp
import matplotlib.pyplot as plt

from PyQt5 import QtWidgets

from gui.mainwindow import Ui_MainWindow

import markov.probabilities as prob
import markov.stabilization as stab

LAMBDA_MIN  = 0
LAMBDA_MAX  = 5
LAMBDA_STEP = 0.01


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.statesNumber = 0

        self.ui.btnSetMatrix.clicked.connect(self.SetMatrix)
        self.ui.btnCacl.clicked.connect(self.Calculate)

        self.ui.twMatrix.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)

        self.ui.twResult.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)

        self.graphicsData = None


    def SetMatrix(self):
        self.statesNumber = self.ui.sbNum.value()

        self.ui.twMatrix.setRowCount(self.statesNumber)
        self.ui.twMatrix.setColumnCount(self.statesNumber)

        self.ui.twMatrix.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)

        for i in range(self.statesNumber):
            for j in range(self.statesNumber):
                dsbCell = self.ui.twMatrix.cellWidget(i, j)

                value = 0 if dsbCell is None else dsbCell.value()

                dsbCell = QtWidgets.QDoubleSpinBox()
                dsbCell.setMinimum(LAMBDA_MIN)
                dsbCell.setMaximum(LAMBDA_MAX)
                dsbCell.setSingleStep(LAMBDA_STEP)
                dsbCell.setValue(value)

                if self.ui.cbGeneration.isChecked():
                    dsbCell.setValue(random.uniform(LAMBDA_MIN, LAMBDA_MAX))

                self.ui.twMatrix.setCellWidget(i, j, dsbCell)

        self.graphicsData = None


    def GetMatrix(self):
        tmp = []
        for i in range(self.statesNumber):
            for j in range(self.statesNumber):
                dsbCell = self.ui.twMatrix.cellWidget(i, j)
                tmp.append(dsbCell.value())

        matrix = np.array(tmp).reshape((self.statesNumber, self.statesNumber))

        return matrix


    def AddRow(self, table, row):
        rowNumber = table.rowCount()
        table.insertRow(rowNumber)

        for i, value in enumerate(row):
            dsbCell = QtWidgets.QDoubleSpinBox()
            dsbCell.setDisabled(True)
            dsbCell.setValue(value)

            table.setCellWidget(rowNumber, i, dsbCell)


    def Calculate(self):
        matrix = self.GetMatrix()

        try:
            p = prob.CalculateMarginalProbabilities(matrix)
            t, self.graphicsData = stab.CalculateStabilizationTime(matrix, p)

            self.ui.twResult.setRowCount(0)
            self.ui.twResult.setColumnCount(len(p))
            self.AddRow(self.ui.twResult, p)
            self.AddRow(self.ui.twResult, t)
            self.ui.twResult.setVerticalHeaderLabels(["P", "t"])

            if sum([np.isnan(x) for x in t]) > 0:
                QtWidgets.QMessageBox.warning(self, "Предупреждение",
                                              "Одно или несколько значений"
                                              + " времени не были найдены")

        except sp.linalg.LinAlgError:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Вырожденная матрица!")

        except Exception as ex:
            QtWidgets.QMessageBox.critical(self, "Ошибка", "Неизвестная ошибка!")
            raise ex


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
