import sys
from UI.US_Cal_Test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import os
from send2trash import send2trash
import logging
from serial import Serial


class SerialWork(QObject):
    readStart = pyqtSignal()
    writeStart = pyqtSignal()

    def __init__(self, port=None, bounds=115200, timeout=10, parent=None):
        super(SerialWork, self).__init__(parent)
        self.port = port
        self.bounds = bounds
        self.timeout = timeout

    def run_serial(self):
        try:
            self.serial = Serial(self.port, self.bounds)
        except Exception as e:
            logging.error('串口打开失败，详见错误： \n' + str(e))
        self.read_msg()

    def read_msg(self):
        if os.path.exists(os.getcwd().join('/test.log')):
            send2trash(os.getcwd().join('/test.log'))
        log_file = open(os.getcwd() + '/test.log', 'w+')
        while True:
            log_str = str(self.serial.readline().decode('utf-8', errors='ignore'))
            print(log_str)
            # 记录读取的信息全部信息到文件
            try:
                log_file.write(log_str)
            except Exception as e:
                logging.error('文件写入错误： ' + str(e))

    def write_cmd(self):
        self.serial


class UsTestMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UsTestMain, self).__init__()
        self.setupUi(self)
        self.initUI()
        self.serial_op = SerialWork()
        self.serial_thread = QThread()
        self.serial_op.moveToThread(self.serial_thread)

    def initUI(self):
        self.lineEdit_savefile.setPlaceholderText(os.getcwd() + '/US_Cal_Test.txt')
        self.toolButton_choosepath.clicked.connect(self.click_choice_save_dir)
        self.lineEdit_savefile.clicked_focus.connect(self.click_choice_save_dir)
        self.action_run.triggered.connect(self.run)
        self.action_stop.triggered.connect(self.stop)
        self.action_rerun.triggered.connect(self.continue_start)

    def click_choice_save_dir(self):
        dir_path = QFileDialog.getSaveFileName(self, "保存为", ".", filter="TXT(*.txt) \n (*.log) \n EXCEL(*.xlsx)")
        # dir_path = QFileDialog.getOpenFileName(self, '打开文件', 'D:/', 'Image files(*.jpg *.gif *.png)')
        # 判断如果未选择目录，则取消
        if dir_path[0] == '':
            print("Not choice")
        else:
            self.lineEdit_savefile.setText(dir_path[0])
        return dir_path

    def run(self):
        print("The Test started")
        if self.lineEdit_savefile.text() == '':
            self.lineEdit_savefile.setText(self.lineEdit_savefile.placeholderText())
        # print(self.lineEdit_savefile.text())

        # TODO 打开CM串口和EB4404的GPIB口
        # TODO 读取串口数据并发送命令给串口
        # TODO 读取EB4404的数据，获取Freq和power值并写入本地文件
        # TODO
        self.serial_op.port = self.comboBox_Ports.currentText()
        self.serial_thread.started.connect(self.serial_op.run_serial)
        self.serial_thread.start()
        self.save_file()

    def stop(self):
        print("Stop Test")

    def continue_start(self):
        print("Continue Test")

    def save_file(self):
        if os.path.exists(self.lineEdit_savefile.text()):
            send2trash(self.lineEdit_savefile.text())
        try:
            with open(self.lineEdit_savefile.text(), 'w+') as file:
                file.write("Now are Testing The word!")
        except Exception as error:
            logging.error('文件写入失败！ \n 错误信息: ' + str(error))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UsTestMain()
    ui.show()
    sys.exit(app.exec_())

