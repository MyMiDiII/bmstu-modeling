import sys

from PyQt5 import QtWidgets
from gui.mainwindow import Ui_MainWindow

from mss.event_model   import EventModel
from mss.generator     import Generator
from mss.memory        import Memory
from mss.processor     import Processor
from mss.distributions import Uniform

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.dsbProbability.setEnabled(False)

        self.ui.btnRun.clicked.connect(self.run)


    def run(self):
        clientM = self.ui.sbClientsM.value()
        clientD = self.ui.sbClientsD.value()

        op1M, op1D = self.ui.sbOperator1M.value(), self.ui.sbOperator1D.value()
        op2M, op2D = self.ui.sbOperator2M.value(), self.ui.sbOperator2D.value()
        op3M, op3D = self.ui.sbOperator3M.value(), self.ui.sbOperator3D.value()

        computer1M = self.ui.sbComputer1.value()
        computer2M = self.ui.sbComputer2.value()

        requestsNum = self.ui.sbNum.value()

        print("run")
        print(clientM, clientD)
        print(op1M, op1D)
        print(op2M, op2D)
        print(op3M, op3D)
        print(computer1M)
        print(computer2M)
        print(requestsNum)

        self.ui.dsbProbability.setValue(0.5)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
