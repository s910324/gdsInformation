import pya
import chk
from ui_infoWidget    import InfoWidget
from ui_headerSelCtrl import HeaderSelCtrl


class LayoutChkWidget(pya.QWidget):
    def __init__(self, parent = None):
        super(LayoutChkWidget, self).__init__(parent)
        self.infoW    = InfoWidget()
        self.ctrlW    = HeaderSelCtrl()
        self.layout   = pya.QHBoxLayout()
        
        self.infoW.setHeaders(self.ctrlW.headers())
        
        self.layout.addWidget(self.ctrlW)
        self.layout.addWidget(self.infoW)
        self.setLayout(self.layout)
        self.resize(1280, 600)
        self.ctrlW.setFixedWidth(290)
        self.setWindowTitle("Layout Info")
        self.ctrlW.setPB.clicked.connect(lambda : self.infoW.setHeaders(self.ctrlW.headers()))  
        
    def saveSettings(self):
        self.ctrlW.saveSettings()
        
    def closeEvent(self, event):
        self.saveSettings()
        event.accept()
        

if __name__ == "__main__" :
    w = LayoutChkWidget()
    w.show()