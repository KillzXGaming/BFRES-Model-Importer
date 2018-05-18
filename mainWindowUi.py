# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BFRESInjector.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("BFRES Injector"))
        Dialog.setEnabled(True)
        Dialog.resize(404, 411)
        Dialog.setStyleSheet(_fromUtf8(""))
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.pushButton = QtGui.QPushButton(self.tab)
        self.pushButton.setEnabled(False)
        self.pushButton.setGeometry(QtCore.QRect(90, 290, 201, 81))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(self.tab)
        self.pushButton_2.setEnabled(True)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 60, 81, 23))
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setStyleSheet(_fromUtf8(""))
        self.pushButton_2.setCheckable(False)
        self.pushButton_2.setFlat(False)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.pushButton_3 = QtGui.QPushButton(self.tab)
        self.pushButton_3.setEnabled(True)
        self.pushButton_3.setGeometry(QtCore.QRect(0, 100, 81, 23))
        self.pushButton_3.setStyleSheet(_fromUtf8(""))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.comboBox = QtGui.QComboBox(self.tab)
        self.comboBox.setEnabled(False)
        self.comboBox.setGeometry(QtCore.QRect(0, 170, 131, 31))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.label = QtGui.QLabel(self.tab)
        self.label.setEnabled(False)
        self.label.setGeometry(QtCore.QRect(10, 140, 89, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.textEdit = QtGui.QLineEdit(self.tab)
        self.textEdit.setEnabled(False)
        self.textEdit.setGeometry(QtCore.QRect(90, 60, 281, 23))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.textEdit_2 = QtGui.QLineEdit(self.tab)
        self.textEdit_2.setEnabled(False)
        self.textEdit_2.setGeometry(QtCore.QRect(90, 100, 281, 23))
        self.textEdit_2.setObjectName(_fromUtf8("textEdit_2"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 371, 31))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "BFRES Injector", None))
        self.pushButton.setText(_translate("Dialog", "Inject BFRES", None))
        self.pushButton_2.setText(_translate("Dialog", "Open CSV", None))
        self.pushButton_3.setText(_translate("Dialog", "Open BFRES", None))
        self.label.setText(_translate("Dialog", "FMDL to inject into", None))
        self.label_2.setText(_translate("Dialog", "Select your CSV and your BFRES file and then press \"Inject BFRES\" below!", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Dialog", "Basics", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "BFRES Settings", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

