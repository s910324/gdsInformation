import pya
import chk
from ui_infoTable     import InfoTableWidget
from ui_headerSelCtrl import HeaderSelCtrl

class InfoWidget(pya.QWidget):
    def __init__(self, parent = None):
        super(InfoWidget, self).__init__(parent)
        self.headers = [
            "Cell XLB", 
            "Cell YLB", 
            "Cell XRT", 
            "Cell YRT", 
            "File name", 
            "Cell name", 
            "ckSum hash",
            "ckSum size", 
            "Unit", 
            "Cell width", 
            "Cell height",            
            "Origin", 
            "Warning", 
        ]
        self.infoT    = InfoTableWidget()
        self.browsePB = pya.QPushButton("Browse gds")
        self.layout   = pya.QVBoxLayout()

        self.layout.addWidget(self.infoT)
        self.layout.addWidget(self.browsePB)
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.browsePB.clicked(self.query)
        
        
    def setHeaders(self, headers):
        self.headers = headers
        self.infoT.setHeaders(headers)
        
    def query(self):
        fnames  = pya.QFileDialog.getOpenFileNames(self, "Select Layout", "", "GDSII (*.gds);;DXF (*.dxf)")      
        data    = chk.gdsFilesSummaryV2(fnames)
        self.infoT.setData(data, self.headers)
        
        
if __name__ == "__main__" :
    w = InfoWidget()
    w.show()