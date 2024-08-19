import pya
from ui_headerSelList import HeaderSelList

class HeaderSelCtrl(pya.QListWidget):
    def __init__(self, parent = None):
        super(HeaderSelCtrl, self).__init__()
        self.initUI()
        self.initSignal()

    def initUI(self):
        self.listW     = HeaderSelList()
        self.addPB     = pya.QPushButton("add")
        self.delPB     = pya.QPushButton("del")
        self.mvTopPB   = pya.QPushButton("top")
        self.mvUpPB    = pya.QPushButton("up")
        self.mvDownPB  = pya.QPushButton("down")
        self.mvEndPB   = pya.QPushButton("end")
        self.setPB     = pya.QPushButton("set")
        self.layout    = pya.QGridLayout()
        
        self.layout.addWidget(self.listW,    0, 1,10, 1)
        
        self.layout.addWidget(self.addPB,    0, 0, 1, 1)
        self.layout.addWidget(self.delPB,    1, 0, 1, 1)
        self.layout.addWidget(self.mvTopPB,  3, 0, 1, 1)
        self.layout.addWidget(self.mvUpPB,   4, 0, 1, 1)
        self.layout.addWidget(self.mvDownPB, 5, 0, 1, 1)
        self.layout.addWidget(self.mvEndPB,  6, 0, 1, 1)
        self.layout.addWidget(self.setPB,    8, 0, 1, 1)
        
        self.layout.setRowMinimumHeight(2, 15)
        self.layout.setRowStretch      (7,  1)
        
        self.setLayout(self.layout)
        
    def initSignal(self):
        self.addPB.clicked.connect(self.addItem)
        self.delPB.clicked.connect(self.delItem)
        
        self.mvTopPB.clicked.connect(self.mvTopItem)
        self.mvUpPB.clicked.connect(self.mvUpItem)
        self.mvDownPB.clicked.connect(self.mvDnItem)
        self.mvEndPB.clicked.connect(self.mvEndItem)     
        
    
    def headers(self):
        return self.listW.updateValue()

    def addItem(self):
        self.listW.addColumnItem("")
        
    def delItem(self):
        index = self.listW.currentRow
        self.listW.delItem(index)
    
    def mvUpItem(self):
        index = self.listW.currentRow
        self.listW.mvItem(index, -1)

    def mvDnItem(self):
        index = self.listW.currentRow
        self.listW.mvItem(index,  1)
        
    def mvTopItem(self):
        index = self.listW.currentRow
        self.listW.mvItem(index,  -index)
        
    def mvEndItem(self):
        index = self.listW.currentRow
        self.listW.mvItem(index,  self.listW.count)
    
    def saveSettings(self):
        self.listW.saveSettings()
        
    def closeEvent(self, event):
        self.saveSettings()
        event.accept()
        
if __name__ == "__main__" :
    w = HeaderSelCtrl()
    w.show()