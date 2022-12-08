import sys

from PyQt5 import QtWidgets
from gui.mainwindow import Ui_MainWindow

from mss.eventmodeller import EventModel
from mss.generator     import Generator, TheatergoersGenerator
from mss.memory        import Memory
from mss.processor     import Processor, ProcessorVIP
from mss.distributions import Uniform, UniformInt

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.dsbProbability.setEnabled(False)

        self.ui.btnRun.clicked.connect(self.run)


    def run(self):
        theatergoersM = 5
        theatergoersD = 4

        numM = 3
        numD = 2

        checkersM = 10
        checkersD = 5

        attendantM = 7
        attendantD = 3

        probabilityVIP = 0.05

        number = 600

        #print("run")
        #print(clientM, clientD)
        #print(op1M, op1D)
        #print(op2M, op2D)
        #print(op3M, op3D)
        #print(computer1M)
        #print(computer2M)
        #print(requestsNum)

        generatorDistribution = Uniform(theatergoersM-theatergoersD
                                        , theatergoersM+theatergoersD)
        numDistribution = UniformInt(numM-numD, numM+numD)
        checkerDistribution = Uniform(checkersM-checkersD, checkersM+checkersD)
        attendantDistribution = Uniform(attendantM-attendantD
                                        , attendantM+attendantD)

        attendant1Generator = Generator(attendantDistribution, [])
        attendant2Generator = Generator(attendantDistribution, [])
        attendant3Generator = Generator(attendantDistribution, [])
        attendant4Generator = Generator(attendantDistribution, [])

        attendant1 = Processor(attendant1Generator, Memory())
        attendant2 = Processor(attendant2Generator, Memory())
        attendant3 = Processor(attendant3Generator, Memory())
        attendant4 = Processor(attendant4Generator, Memory())

        attendants = [attendant1, attendant2, attendant3, attendant4]

        checker1Generator = Generator(checkerDistribution, attendants)
        checker2Generator = Generator(checkerDistribution, attendants)
        checker3Generator = Generator(checkerDistribution, attendants)

        checker1 = ProcessorVIP(checker1Generator, Memory(), False)
        checker2 = ProcessorVIP(checker2Generator, Memory(), False)
        checker3 = ProcessorVIP(checker3Generator, Memory(), True)

        checkers = [checker1, checker2, checker3]

        generator = TheatergoersGenerator(generatorDistribution
                                          , numDistribution
                                          , checkers
                                          , probabilityVIP)

        model = EventModel(generator, checkers, attendants, number)
        time = model.run()

        print(time)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
