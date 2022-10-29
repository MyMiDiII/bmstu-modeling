import sys
import random

import numpy as np
import networkx as nx
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


    def SetMatrix(self):
        self.statesNumber = self.ui.sbNum.value()

        self.ui.twMatrix.setRowCount(self.statesNumber)
        self.ui.twMatrix.setColumnCount(self.statesNumber)

        for i in range(self.statesNumber):
            for j in range(self.statesNumber):
                dsbCell = QtWidgets.QDoubleSpinBox()
                dsbCell.setMinimum(LAMBDA_MIN)
                dsbCell.setMaximum(LAMBDA_MAX)
                dsbCell.setSingleStep(LAMBDA_STEP)

                if self.ui.cbGeneration.isChecked():
                    dsbCell.setValue(random.uniform(LAMBDA_MIN, LAMBDA_MAX))

                self.ui.twMatrix.setCellWidget(i, j, dsbCell)


    def GetMatrix(self):
        tmp = []
        for i in range(self.statesNumber):
            for j in range(self.statesNumber):
                dsbCell = self.ui.twMatrix.cellWidget(i, j)
                tmp.append(dsbCell.value())

        matrix = np.array(tmp).reshape((self.statesNumber, self.statesNumber))

        print(matrix)

        #G = nx.from_numpy_matrix(matrix, create_using=nx.DiGraph)
        #print(G)

        #layout = nx.spring_layout(G)
        #edge_labels = nx.get_edge_attributes(G, "weight")
        #node_labels = dict((x, x+1) for x in range(self.statesNumber))

        #nx.draw(G, layout, connectionstyle='arc3, rad = 0.1')
        #nx.draw_networkx_edge_labels(G, pos=layout, edge_labels=edge_labels)
        #nx.draw_networkx_labels(G, layout, labels=node_labels)

        #plt.show()

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

        p = prob.CalculateMarginalProbabilities(matrix)
        t = stab.CalculateStabilizationTime(matrix)

        self.ui.twResult.setRowCount(0)
        self.ui.twResult.setColumnCount(len(p))
        self.AddRow(self.ui.twResult, p)
        self.AddRow(self.ui.twResult, t)
        self.ui.twResult.setVerticalHeaderLabels(["p", "t"])


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
