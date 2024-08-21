import os
import pya
from ui_headerSelList import HeaderSelList

class HeaderSelCtrl(pya.QListWidget):
    def __init__(self, parent = None):
        super(HeaderSelCtrl, self).__init__()
        self.initUI()
        self.initSignal()

    def initUI(self):
        self.listW     = HeaderSelList()
        self.addPB     = pya.QPushButton(icon = self.svgIcon("square-plus-solid"),  text = "")
        self.delPB     = pya.QPushButton(icon = self.svgIcon("square-minus-solid"), text = "")
        self.mvTopPB   = pya.QPushButton(icon = self.svgIcon("angles-up-solid"),    text = "")
        self.mvUpPB    = pya.QPushButton(icon = self.svgIcon("angle-up-solid"),     text = "")
        self.mvDownPB  = pya.QPushButton(icon = self.svgIcon("angle-down-solid"),   text = "")
        self.mvEndPB   = pya.QPushButton(icon = self.svgIcon("angles-down-solid"),  text = "")
        
        self.importPB  = pya.QPushButton(icon = self.svgIcon("upload-solid"),       text = "")
        self.exportPB  = pya.QPushButton(icon = self.svgIcon("download-solid"),     text = "")
        
        self.setPB     = pya.QPushButton(icon = self.svgIcon("circle-check-solid"), text = "")
        self.layout    = pya.QGridLayout()
        
        self.layout.addWidget(self.listW,    0, 1,12, 1)
        
        self.layout.addWidget(self.addPB,    0, 0, 1, 1)
        self.layout.addWidget(self.delPB,    1, 0, 1, 1)
        self.layout.addWidget(self.mvTopPB,  3, 0, 1, 1)
        self.layout.addWidget(self.mvUpPB,   4, 0, 1, 1)
        self.layout.addWidget(self.mvDownPB, 5, 0, 1, 1)
        self.layout.addWidget(self.mvEndPB,  6, 0, 1, 1)
        
        self.layout.addWidget(self.importPB, 8, 0, 1, 1)
        self.layout.addWidget(self.exportPB, 9, 0, 1, 1)
        
        self.layout.addWidget(self.setPB,   11, 0, 1, 1)
        
        self.layout.setRowMinimumHeight( 2, 15)
        self.layout.setRowStretch      ( 7,  1)
        self.layout.setRowStretch      (10,  1)
        self.setLayout(self.layout)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.setLineWidth(0)
        self.setFrameShape(pya.QFrame.Panel)
        self.setFrameShadow(pya.QFrame.Plain)

        theme = """
        QListWidget{
            background-color : #f0f0f0;
        }
        """
        self.setStyleSheet(theme)
        
    def initSignal(self):
        self.addPB.clicked.connect(self.addItem)
        self.delPB.clicked.connect(self.delItem)
        
        self.mvTopPB.clicked.connect(self.mvTopItem)
        self.mvUpPB.clicked.connect(self.mvUpItem)
        self.mvDownPB.clicked.connect(self.mvDnItem)
        self.mvEndPB.clicked.connect(self.mvEndItem)     
        
        self.importPB.clicked.connect(self.importSettings)   
        self.exportPB.clicked.connect(self.exportSettings)   
    
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
    
    def exportSettings(self):
        self.listW.saveSettings(showOptions = True)
        
    def importSettings(self):
        self.listW.loadSettings(showOptions = True)
         
    def saveSettings(self):
        self.listW.saveSettings()
        
    def closeEvent(self, event):
        self.saveSettings()
        event.accept()

    def svgIcon(self, name, size = (12, 12), color = pya.QColor(0,0,0,150)):
        dirPath   = os.path.dirname(__file__) 
        genPath   = lambda rPath : os.path.realpath(os.path.join(dirPath, *rPath.split("/")))
        iconPath  = genPath("../icon")
        renderer  = pya.QSvgRenderer(f"{iconPath}/{name}.svg")
        pixmap    = pya.QPixmap(size[0], size[1])
        pixmap.fill(pya.QColor(0,0,0,0))
        painter   = pya.QPainter(pixmap)
        renderer.render(painter)
        painter.setCompositionMode(painter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(pixmap.rect(), color)
        painter.end()
        return pya.QIcon(pixmap)

if __name__ == "__main__" :
    w = HeaderSelCtrl()
    w.show()