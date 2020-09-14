from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal, Qt


class QCustomLineEdit(QLineEdit):
    clicked_focus = pyqtSignal()

    def __init__(self, parent=None):
        super(QCustomLineEdit, self).__init__(parent)

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked_focus.emit()
        super(QCustomLineEdit, self).mousePressEvent(QMouseEvent)




