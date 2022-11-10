import sys

from PyQt5 import QtWidgets
from gui.mainwindow import Ui_MainWindow

from randseq.algorithmic import QuadraticGenerator
from randseq.criterion import RandomnessCriterion


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.btnGenAlg.clicked.connect(self.generateAlg)

        self.inputNum = 10
        self.initInputTable()
        self.ui.btnCaclInput.clicked.connect(self.calculateInput)


    def generateAlg(self):
        number = self.ui.sbAlg.value()

        sequences = [
            QuadraticGenerator(0, 9).GenerateSequence(number),
            QuadraticGenerator(10, 99).GenerateSequence(number),
            QuadraticGenerator(100, 999).GenerateSequence(number)
        ]

        self.ui.twAlg.setRowCount(number)
        self.ui.twAlg.setColumnCount(3)
        self.ui.twAlg.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)

        coefficients = []

        for j, sequence in enumerate(sequences):
            for i in range(number):
                item = QtWidgets.QTableWidgetItem(str(sequence[i]))
                self.ui.twAlg.setItem(i, j, item)
                #sbCell = QtWidgets.QSpinBox()
                #sbCell.setMinimum(0)
                #sbCell.setMaximum(999)
                #sbCell.setValue(sequence[i])
                #sbCell.setDisabled(True)

                #self.ui.twAlg.setCellWidget(j, i, sbCell)

            coefficients.append(RandomnessCriterion().GetCoefficient(sequence))

        print(coefficients)

        self.ui.twCoefAlg.setRowCount(1)
        self.ui.twCoefAlg.setVerticalHeaderLabels(["K"])
        self.ui.twCoefAlg.setColumnCount(3)
        self.ui.twCoefAlg.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)

        for j, coefficient in enumerate(coefficients):
            item = QtWidgets.QTableWidgetItem(str(coefficient))
            self.ui.twCoefAlg.setItem(0, j, item)


    def initInputTable(self):

        self.ui.twInput.setRowCount(self.inputNum)
        self.ui.twInput.setColumnCount(1)
        self.ui.twInput.horizontalHeader().setSectionResizeMode(
                QtWidgets.QHeaderView.Stretch)

        for i in range(self.inputNum):
            sbCell = QtWidgets.QSpinBox()
            sbCell.setMinimum(0)
            sbCell.setMaximum(9)
            sbCell.setSingleStep(1)

            self.ui.twInput.setCellWidget(i, 0, sbCell)

    def calculateInput(self):
        sequence = [self.ui.twInput.cellWidget(i, 0).value()
                        for i in range(self.inputNum)]

        coefficient = RandomnessCriterion().GetCoefficient(sequence)

        self.ui.dsbCoefInput.setValue(coefficient)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
