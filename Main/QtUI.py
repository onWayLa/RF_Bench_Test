import sys
from UI.US_Cal_Test import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class UsTestMain(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(UsTestMain, self).__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.toolButton_choosepath.clicked.connect(self.click_choice_save_dir)

    def click_choice_save_dir(self):
        dir_path = QFileDialog.getSaveFileName(self, "保存为", ".", filter="TXT(*.txt) \n (*.log) \n EXCEL(*.xlsx)")
        # dir_path = QFileDialog.getOpenFileName(self, '打开文件', 'D:/', 'Image files(*.jpg *.gif *.png)')
        # 判断如果未选择目录，则取消
        if dir_path[0] == '':
            print("Not choice")
        else:
            self.lineEdit_savefile.setText(dir_path[0])
        return dir_path


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = UsTestMain()
    ui.show()
    sys.exit(app.exec_())

