import pya

class HeaderSelItem(pya.QWidget):
    def __init__(self, index = 0, columnTitle = "", parent = None):
        super(HeaderSelItem, self).__init__(parent)
        self.opt = [
            "",
            "File name", 
            "Unit", 
            "ckSum",
            "ckSum hash",
            "ckSum size",
            "Top cell count", 
            "File size(byte)", 
            "File size(KB)", 
            "File size(MB)", 

            "Layer count", 
            "Layer info", 

            "Cell name", 
            "Cell width", 
            "Cell height",            
            
            "Cell XLB", 
            "Cell YLB", 
            "Cell XRT", 
            "Cell YRT", 
            "Cell LB", 
            "Cell RT", 
            "Cell window", 
            "Origin", 
            "Warning", 
        ]
        self.initUI(index, columnTitle)
        
    def initUI(self, index = 0, columnTitle = ""):
        self.idLB      = pya.QLabel()
        self.optionCMB = pya.QComboBox()
        self.layout    = pya.QHBoxLayout()

        self.optionCMB.addItems(self.opt) 
        self.layout.addWidget(self.idLB)
        self.layout.addWidget(self.optionCMB)
        self.idLB.setFixedWidth(35)
        self.setLayout(self.layout)
        self.setValue(columnTitle)
        self.setLabelIndex(index)
        self.layout.setContentsMargins(5, 5, 5, 5)
        self.layout.setSpacing(0)

    def setLabelIndex(self, index):
        self.idLB.setText(f"#{str(index).zfill(2)}")

    def setIndex(self, index):
        index = 0 if index< len(self.opt) else index
        self.optionCMB.setCurrentIndex (index)

    def setValue(self, value):
        index  = 0
        if (value in self.opt): 
            index = self.opt.index(value)
        self.optionCMB.setCurrentIndex(index)

    def currentText(self):
        return self.optionCMB.currentText

if __name__ == "__main__":
    hsi = HeaderSelItem(0, "Cell XLB")
    hsi.show()
    
