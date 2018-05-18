from PyQt4 import QtGui, QtCore
from mainWindowUi import Ui_Dialog #same name as appears in mainWindowUi.py
import os
from BFRES_Vertex import *

class MainWindow (QtGui.QDialog): #Or wherever you are inheriting from

    valueChanged = QtCore.pyqtSignal()

    def __init__ (self, parent = None):
        super (MainWindow, self).__init__ ()
        self.ui = Ui_Dialog () #same name as appears in mainWindowUi.py
        self.ui.setupUi (self)
        self.ui.pushButton_2.clicked.connect(self.csv_open) #Open BFRES button
        self.ui.pushButton_3.clicked.connect(self.bfres_open) #Open BFRES button
        self.ui.textEdit.textChanged.connect(self.updatefile)
        self.ui.textEdit_2.textChanged.connect(self.updatefile)
        self.ui.pushButton.clicked.connect(self.bfres_inject) #Open BFRES button


			
    def updatefile(self):
        allValid = bool(self.ui.textEdit.text()
            and self.ui.textEdit_2.text())
        self.ui.pushButton.setEnabled(allValid)
        self.ui.comboBox.setEnabled(allValid)

    def csv_open(self):
        file = QtGui.QFileDialog.getOpenFileName(None, "Open File", "", "CSV (*.csv)");
        if file:
       #     cvsIn = open(file, "r") 
          #  self.ui.pushButton_2.setStyleSheet("background-color:  qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(17, 182, 54, 255), stop:1 rgba(171, 255, 173, 255));")
            self.ui.textEdit.setText(str(file))
        else:
            print('Cancelled')
			
    def bfres_open(self):
        file = QtGui.QFileDialog.getOpenFileName(None, "Open File", "", "BFRES (*.bfres)");
        if file:
            fil = open(file, "rb+") 
          #  self.ui.pushButton_3.setStyleSheet("background-color:  qlineargradient(spread:pad, x1:0, y1:1, x2:0, y2:0, stop:0 rgba(17, 182, 54, 255), stop:1 rgba(171, 255, 173, 255));")
            self.ui.textEdit_2.setText(str(file))
            self.ui.comboBox.clear()
            self.ui.comboBox.addItem("All FMDLs (Default)")
            bfres_data(self, fil)
			

			
        else:
            print('Cancelled')

    def bfres_inject(self):
        cvsIn = open(self.ui.textEdit.text(), "r")
        f = open(self.ui.textEdit_2.text(), "rb+")

        combindx = self.ui.comboBox.currentIndex()
		
        if combindx == 0:
            FMDLIndex = None
        else:
            FMDLIndex = combindx

        f.seek(0) #Seek back to start of bfres so we can start injecting
        readCSV(cvsIn)
        readBFRES(f, FMDLIndex)
    #    os.system("BFRES_Vertex.py " + f + " " + cvsIn)

     #   BFRES_Vertex(f(sys.argv[1]), cvsIn(sys.argv[2]))

def bfres_data(self, f):
    f.seek(4) #Magic
    SwitchCheck = readlongle(f)

    if (SwitchCheck == 0x20202020):
        f.seek(0x28)
        FMDLOffset = readlongle(f)

        f.seek(0xBC)
        FMDLTotal = readunshortle(f)

        f.seek(FMDLOffset,0)
        for mdl in range(1, FMDLTotal + 1):
            FMDLOffset = f.tell()
            f.seek(FMDLOffset)

            FMDLArr = []
                            
            #F_Model Header
            fmdl_info = fmdlh(f)
            FMDLArr.append(fmdl_info)
            NextFMDL = f.tell()

            f.seek(fmdl_info.fnameOff)
            f.seek(0x02,1)
            FMDLName = getString(f)
            self.ui.comboBox.addItem(FMDLName)

                            
            f.seek(NextFMDL)
    else:
        f.seek(5)
        verNum = readByte(f)
        f.seek(26,1)
        FileOffset = ReadOffset(f)
        f.seek(FileOffset)
        BlockSize = readu32be(f)
        FMDLTotal = readu32be(f)
        f.seek(0x10,1)

        for mdl in range(FMDLTotal):
            f.seek(12,1)
            FMDLOffset = ReadOffset(f)
            NextFMDL = f.tell()
            f.seek(FMDLOffset)

            FMDLArr = []

            #F_Model Header
            fmdl_info = WiiUfmdlh(f)
            FMDLArr.append(fmdl_info)

            f.seek(NextFMDL)
                    
            f.seek(fmdl_info.fnameOff)
            FMDLName = getString(f)
            self.ui.comboBox.addItem(FMDLName)
			
            f.seek(NextFMDL)	