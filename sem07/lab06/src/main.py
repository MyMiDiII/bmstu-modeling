import sys
import math

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

        self.ui.btnRun.clicked.connect(self.run)

    def run(self):
        theatergoersM = self.ui.sbThGoersM.value()
        theatergoersD = self.ui.sbThGoersD.value()

        numM = self.ui.sbNumM.value()
        numD = self.ui.sbNumD.value()

        checkersM = self.ui.sbCheckM.value()
        checkersD = self.ui.sbCheckD.value()

        attendantM = self.ui.sbAttendantM.value()
        attendantD = self.ui.sbAttendantD.value()

        probabilityVIP = self.ui.sbVIP.value() / 100

        number = self.ui.sbNum.value()

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
        time = math.ceil(model.run() / 60)

        self.ui.lcdResult.display(time)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
