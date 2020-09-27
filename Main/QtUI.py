import sys
from UI.US_Cal_Test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import os
import time
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
        self.freq_nums = None
        self.power_nums = None
        self.module = None

    def init_config(self, freq_num, power_num, module):
        if freq_num == 2:
            self.freq_nums = [5.1, 35]
        elif freq_num == 3:
            self.freq_nums = [5.1, 35, 64.9]
        elif freq_num == 4:
            self.freq_nums = [5.1, 35, 64.9, 84.9]
        else:
            logging.error('Freq number error')

        if power_num == 8:
            self.power_nums = [58, 52, 46, 40, 34, 28, 22, 16]
        elif power_num == 10:
            self.power_nums = [58, 52, 46, 40, 34, 28, 22, 16, 10, 8]
        else:
            logging.error('power number error')

        if module == 'QPSK':
            self.module = module
        elif module == '64QAM':
            self.module = module
        elif module == '256QAM':
            self.module = module

    def run_serial(self):
        print('run the serial', self.module)
        print('current threading id: ', int(QThread.currentThreadId()))
        try:
            self.serial = Serial(self.port, self.bounds)
        except Exception as e:
            logging.error('串口打开失败，详见错误： \n' + str(e))
        # time.sleep(3)
        self.write_stop_scan()

        if os.path.exists(os.getcwd().join('/test.log')):
            send2trash(os.getcwd().join('/test.log'))
        log_file = open(os.getcwd() + '/test.log', 'w+')

        # 记录读取到的信息
        for freq in self.freq_nums:
            for power in self.power_nums:
                self.write_us_trans(self.module, freq, power)
                self.read_msg(log_file)
                time.sleep(2)

    def read_msg(self, log_file):
        log_str = str(self.serial.readline().decode('utf-8', errors='ignore'))
        # 记录读取的信息全部信息到文件
        try:
            log_file.write(log_str)
            print(log_str)
        except Exception as e:
            logging.error('文件写入错误： ' + str(e))

    def write_stop_scan(self):
        # 暂停扫频并进入cmHal路径
        self.serial.write('/doc/scan_stop\r\n'.encode())
        self.serial.write('cd /cm\r\n'.encode())

    def write_us_trans(self, modu, freq, pwr):
        transmit = 'us_transmit {} 0.16 {} {} tdma 0\r\n'.format(modu, freq, pwr)
        self.serial.write('us_reset\r'.encode())
        self.serial.write(transmit.encode())
        print(transmit)
        time.sleep(2)


class UsTestMain(QMainWindow, Ui_MainWindow):
    paramChanged = pyqtSignal(int, int, str)

    def __init__(self):
        super(UsTestMain, self).__init__()
        self.setupUi(self)
        self.serial_op = SerialWork()
        self.serial_thread = QThread()
        self.serial_op.moveToThread(self.serial_thread)
        self.initUI()

    def initUI(self):
        self.lineEdit_savefile.setPlaceholderText(os.getcwd() + '\\US_Cal_Test.txt')
        self.toolButton_choosepath.clicked.connect(self.click_choice_save_dir)
        self.lineEdit_savefile.clicked_focus.connect(self.click_choice_save_dir)
        self.action_run.triggered.connect(self.run)
        self.action_stop.triggered.connect(self.stop)
        self.action_rerun.triggered.connect(self.continue_start)
        self.serial_thread.started.connect(self.serial_op.run_serial)

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
        # print('current threading id: ', int(QThread.currentThreadId()))
        if self.serial_thread.isRunning():
            print('current threading id: ', int(QThread.currentThreadId()))
        print("The Test started")
        if self.lineEdit_savefile.text() == '':
            self.lineEdit_savefile.setText(self.lineEdit_savefile.placeholderText())

        # TODO 打开CM串口和EB4404的GPIB口
        # TODO 读取串口数据并发送命令给串口
        # TODO 读取EB4404的数据，获取Freq和power值并写入本地文件
        # TODO
        self.serial_op.init_config(self.spinBox_numfreq.value(),
                                   self.spinBox_numpower.value(),
                                   self.comboBox_constellation.currentText())
        self.serial_op.port = self.comboBox_Ports.currentText()
        self.serial_thread.start()
        self.save_file()

    def stop(self):
        #  关闭串口
        self.serial_op.serial.close()
        # 结束子进程
        self.serial_thread.exit()
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

