import pya
import chk

class InfoTableWidget(pya.QTableWidget):
    def __init__(self, data = [], headers = [], parent = None):
        super(InfoTableWidget, self).__init__(parent)
        self.setEditTriggers(pya.QAbstractItemView.NoEditTriggers)
        self.setSelectionBehavior(pya.QAbstractItemView.SelectRows)
        self.data    = data
        self.headers = headers
        self.setData(data, headers)
        
    def keyPressEvent(self, event):
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
        colWidth     = [ len(h) for h in headers]
        self.setRowCount(len(data))
        self.setColumnCount(len(headers))
        self.setHorizontalHeaderLabels(headers)
        
        for row, instData in enumerate(data):
            for column, header in enumerate(headers):
                dataStr          = str(instData.get(header) or "")
                item             = pya.QTableWidgetItem(dataStr)
                colWidth[column] = max(colWidth[column], len(dataStr))
                self.setItem (row, column, item )

        
        for column in range(len(headers)):
            self.setColumnWidth(column, colWidth[column] * 6 + 35)

    
    def setHeaders(self, headers = []):
        if headers:
            self.setData(self.data, headers)
        
    def clearContents(self):
        self.data    = []
        self.headers = []        
        super(InfoTableWidget, self).clearContents()
        
if __name__ == "__main__" :
    w = InfoTableWidget()
    headers  = [
            "",
            "File name", 
            "Unit", 
            "ckSum",
            "ckSum hash",
            "ckSum size",
    ]
    data = []
    w.setData(data, headers)
    w.show()