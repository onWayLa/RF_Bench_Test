import sys
from Instrument.US_Cal_Test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow


class UsTestMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UsTestMain, self).__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UsTestMain()
    ui.show()
    sys.exit(app.exec_())

