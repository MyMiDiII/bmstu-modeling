import sys

from PyQt5 import QtWidgets
from gui.mainwindow import Ui_MainWindow

from queuing_system.event_model   import EventModel
from queuing_system.generator     import Generator
from queuing_system.memory        import Memory
from queuing_system.processor     import Processor
from queuing_system.distributions import Uniform, Normal

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.sbMaxLenStep.setDisabled(True)
        self.ui.sbMaxLenEvent.setDisabled(True)

        self.ui.btnRun.clicked.connect(self.run)


    def run(self):
        a, b = self.ui.dsbA.value(), self.ui.dsbB.value()
        m, sigma = self.ui.dsbM.value(), self.ui.dsbSigma.value()
        num = self.ui.sbRequestNum.value()
        percent = int(self.ui.dsbProbability.value() * 100)
        delta_t = self.ui.dsbDeltaT.value()

        if m < 4 * sigma:
            QtWidgets.QMessageBox.critical(
                self,
                "Ошибка",
                "При таких m и sigma возможна генерация отрицательных значений",
                QtWidgets.QMessageBox.Ok)


        generator = Generator(Uniform(a, b))
        memory = Memory()
        processor = Processor(Normal(m, sigma))

        event_model = EventModel(generator, memory, processor, num, percent)
        event_model_result = event_model.run()

        self.ui.sbMaxLenEvent.setValue(event_model_result)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
