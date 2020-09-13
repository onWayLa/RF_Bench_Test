import sys
from UI.US_Cal_Test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
import os
from send2trash import send2trash
import logging


class UsTestMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UsTestMain, self).__init__()
        self.setupUi(self)
        self.initUI()

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

