
import os
import sys
import pya
from   importlib import reload  
from   datetime  import datetime

importPath  = os.path.dirname(__file__)
if not importPath in sys.path:
    sys.path.insert(0, importPath)
    
import chk    
import fileExport
reload(chk)
reload(fileExport)


class LayoutCheckWidget(pya.QWidget):
    def __init__(self, parent = None):
        super(LayoutCheckWidget, self).__init__(parent)

        self.headers  = ["File Name", "check Sum", "file Size", "Unit", "cell Name", "cad Window", "cell Width", "cell Heigth", "origin"]
        self.data     = []
        
        self.browsePB = pya.QPushButton("Browse")
        self.layoutTB = LayoutTableWidget(self.data, self.headers)
        self.mainLY   = pya.QVBoxLayout()
        
        self.mainLY.addWidget(self.layoutTB)
        self.mainLY.addWidget(self.browsePB)
        self.setLayout(self.mainLY)

        self.browsePB.clicked(self.query)
        self.resize(1280, 600)
        self.setWindowTitle("Layout Info")
        
        
    def query(self):

        fnames    = pya.QFileDialog.getOpenFileNames(self, "Select Layout", "", "GDSII (*.gds);;DXF (*.dxf)")
        self.data = []
        for d in chk.gdsFilesSummary(fnames).split("\n")[1:]:
            colData = d.split("|")
            self.data.append(colData)
        
        self.layoutTB.setData(self.data, self.headers)

class AlignDelegate(pya.QItemDelegate):
    def paint(self, painter, option, index):
        option.displayAlignment = pya.Qt.AlignCenter
        pya.QItemDelegate.paint(self, painter, option, index)
        
class LayoutTableWidget(pya.QTableWidget):
    def __init__(self, data = [], headers = [], parent = None):
        super(LayoutTableWidget, self).__init__()  
        self.setEditTriggers(pya.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(pya.QAbstractItemView.SelectRows)
        self.data    = data
        self.headers = headers
        self.setData(data, headers)
        #self.setItemDelegate(AlignDelegate())
        
    def keyPressEvent(self, event):
        #super().keyPressEvent(event)
        self.copyTable()
    
    def copyTable(self):
        copyText    = ''
        copiedCells = sorted(self.selectedIndexes())
        maxColumn   = copiedCells[-1].column()
        maxRow      = copiedCells[-1].row()
               
        for c in copiedCells:
            cellText = self.item(c.row(), c.column()).text
            copyText += cellText
            if c.column() == maxColumn:
                if c.row() != maxRow:
                    copyText += '\n'
            else:
                copyText += '\t'
        pya.QApplication.clipboard().setText(copyText)
        pya.QToolTip.showText(pya.QCursor.pos, "Information Copied to Clipboard")
 
    def setData(self, data = [], headers = []):
        self.clearContents()
        self.data    = data
        self.headers = headers
        
        self.setRowCount(len(data))
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        
        colWidth = [300, 150, 85, 85, 100, 200, 85, 85, 85]
        for column in range(len(headers)):
            self.setColumnWidth(column, colWidth[column])

                
        for row, instData in enumerate(data):
            for column, header in enumerate(headers):
                dataStr = str(instData[column])
                item    = pya.QTableWidgetItem(dataStr)
                self.setItem (row, column, item )

    def clearContents(self):
        self.data    = []
        self.headers = []        
        super(LayoutTableWidget, self).clearContents() 

if __name__ == "__main__" :

    lcw = LayoutCheckWidget()
    lcw.show()
