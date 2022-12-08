import sys

from PyQt5 import QtWidgets
from gui.mainwindow import Ui_MainWindow

from mss.eventmodeller import EventModel
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

        #print("run")
        #print(clientM, clientD)
        #print(op1M, op1D)
        #print(op2M, op2D)
        #print(op3M, op3D)
        #print(computer1M)
        #print(computer2M)
        #print(requestsNum)

        generatorDistribution = Uniform(clientM-clientD, clientM+clientD)

        operator1Distribution = Uniform(op1M-op1D, op1M+op1D)
        operator2Distribution = Uniform(op2M-op2D, op2M+op2D)
        operator3Distribution = Uniform(op3M-op3D, op3M+op3D)

        computer1Distribution = Uniform(computer1M, computer1M)
        computer2Distribution = Uniform(computer2M, computer2M)

        computer1Generator = Generator(computer1Distribution, [])
        computer2Generator = Generator(computer2Distribution, [])

        computer1 = Processor(computer1Generator, Memory())
        computer2 = Processor(computer2Generator, Memory())
        computers = [computer1, computer2]

        operator1Generator = Generator(operator1Distribution, [computer1])
        operator2Generator = Generator(operator2Distribution, [computer1])
        operator3Generator = Generator(operator3Distribution, [computer2])

        operator1 = Processor(operator1Generator, Memory(0))
        operator2 = Processor(operator2Generator, Memory(0))
        operator3 = Processor(operator3Generator, Memory(0))

        operators = [operator1, operator2, operator3]

        orderedOperators = sorted([(operator1, op1M, op1D)
                                  ,(operator2, op1M, op2D)
                                  ,(operator3, op3M, op3D)],
                                  key=lambda x: (x[1], -x[2]))
        orderedOperators = [operator[0] for operator in orderedOperators]

        generator = Generator(generatorDistribution, orderedOperators)

        model = EventModel(generator, operators, computers, requestsNum)
        probability = model.run()

        self.ui.dsbProbability.setValue(probability)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
