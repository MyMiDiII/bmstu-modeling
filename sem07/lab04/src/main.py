import sys

from PyQt5 import QtWidgets
from gui.mainwindow import Ui_MainWindow

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.cbPrinciple.addItems(['Пошаговый', "Событийный"])
        self.ui.cbPrinciple.currentIndexChanged.connect(
                lambda : self.ui.dsbDeltaT.setDisabled(True if
                self.ui.dsbDeltaT.isEnabled() else False)
                )


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
