from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import pyqtSignal


class QCustomLineEdit(QLineEdit):
    clicked_focus = pyqtSignal()

    def __init__(self, parent=None):
        super(QCustomLineEdit, self).__init__(parent)

    def focusInEvent(self, QFocusEvent):
        self.clicked_focus.emit()
        super(QCustomLineEdit, self).focusInEvent(QFocusEvent)




