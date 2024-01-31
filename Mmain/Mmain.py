
import traceback

from PyQt5.QtWidgets import QFileDialog
from functools import partial
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMessageBox
from PyQt5 import QtGui
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from Mthread import Thread_1
import sys, os, json, urllib3
urllib3.disable_warnings()
e = True

class Ui_Form(QMainWindow):

    def __init__(self):
        try:
            super(Ui_Form, self).__init__()
            self.ui = loadUi('ui\\main.ui', self)
            self.thread = None
            palette1 = QtGui.QPalette()
            self.ui.setPalette(palette1)
            self.ui.setWindowTitle('百度检索 1.1')
            self.ui.Bpath.clicked.connect(self.MtextFile)
            self.ui.Bclear.clicked.connect(self.clearLog)
            self.ui.Bexport.clicked.connect(self.exportLog)
            self.ui.Brun.clicked.connect(self.Mlogin)
        except:
            print(traceback.print_exc())

    def MtextFile(self):
        try:
            file_, filetype = QFileDialog.getOpenFileName(self, '选取文件', '.', 'Excel文件(*.xlsx , *.xls , *.xlsm)')
            print('文本类型选择', file_)
            if file_:
                self.Lshow.setText(file_)
        except:
            print(traceback.print_exc())

    def MSelect(self):
        file_, filetype = QFileDialog.getOpenFileName(self, '选取文件', '.', 'Excel文件(*.xlsx , *.xls , *.xlsm)')
        print('标题选择', file_)
        if file_:
            self.titleFile.setText(file_)

    def Mlogin(self, submitType='login'):
        try:
            if self.thread:
                self.thread.terminate()
                self.thread.wait()
                if self.thread.isFinished():
                    del self.thread
                    self.thread = None
                    self.articleIssue.setText('暂停')
            else:
                data = {'type':submitType, 
                 'path':self.Lshow.text(), 
                 'cookie':self.lineEdit.text()}
                print(data)
            try:
                if data.get('path'):
                    self.thread1 = Thread_1(data)
                    self.thread1._signal.connect(self.info)
                    self.thread1.start()
            except:
                print(traceback.print_exc())

        except:
            print(traceback.print_exc())

    def info(self, data):
        if data.get('type') == 'str':
            self.Tpanel.append(f"{data.get('data')}{chr(10)}")
        else:
            if data.get('type') == 'return':
                pass
            elif data.get('type') == 'status':
                self.exeStatus = data.get('data')
            else:
                if data.get('type') == 'data':
                    _dict = {}
                    for item in data.get('data'):
                        _dict[item.get('shipNameCh')] = item.get('mmsi')

                    self.items = _dict
                    self.initCombox()

    def clearLog(self):
        self.Tpanel.clear()

    def exportLog(self):
        try:
            filename = QFileDialog.getSaveFileName(self.ui, '保存日志', './', 'Text Files (*.txt)')
            with open(filename[0], 'w') as (f):
                my_text = self.Tpanel.toPlainText()
                f.write(my_text)
        except:
            print(traceback.print_exc()) if e else None


def main():
    try:
        QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
        app = QtWidgets.QApplication(sys.argv)
        w = Ui_Form()
        w.show()
        sys.exit(app.exec_())
    except:
        print(traceback.print_exc()) if e else None


if __name__ == '__main__':
    main()
