import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtCore import pyqtSignal
import logging


class QCustomComboBox(QComboBox):
    # popupAboutToBeShown = pyqtSignal()

    def __init__(self, parent=None):
        super(QCustomComboBox, self).__init__(parent)
        self.insertItem(0, "端口号")

    def showPopup(self):
        self.clear()
        self.insertItem(0, "端口号")
        index = 1
        port_list = self.scan_ports()
        # print(port_list)
        if port_list is not None:
            for port in port_list:
                self.insertItem(index, port)
                index += 1
        super(QCustomComboBox, self).showPopup()

    @staticmethod
    def scan_ports():
        try:
            for port in serial.tools.list_ports.comports():
                # 只找出包含USB的串口
                if 'USB-SERIAL' in port.description:
                    yield port.device
        except Exception as e:
            logging.error("获取所有接入的USB串口设备出错！\n错误信息：" + str(e))
