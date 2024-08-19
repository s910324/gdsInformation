import os
import pya
import pickle
from ui_headerSelItem import HeaderSelItem

class HeaderSelList(pya.QListWidget):
    def __init__(self, parent = None):
        super().__init__()
        self.data = []
        self.loadSettings()
        

    def addColumnItem(self, columnName = ""):
        lwidget = HeaderSelItem(self.count + 1, columnName, self)
        lItem   = pya.QListWidgetItem(self)
        lItem.setSizeHint(lwidget.sizeHint())
        self.addItem(lItem)
        self.setItemWidget(lItem, lwidget)
        self.data.append(columnName)
    
    def updateValue(self):
        self.data = [self.itemWidget(self.item(r)).currentText() for r in range(self.count)]
        return self.data
        
    def loadItems(self, itemList):
        self.clear()
        self.data = []
        for i in itemList:
            self.addColumnItem(i)
            
    def mvItem(self, index, shift):
        self.updateValue()
        new_index = sorted([0, (index + shift), len(self.data)-1])[1]
        if not(new_index == index):
            mv_item = self.data.pop(index)
            self.data.insert(new_index, mv_item)
            
        self.loadItems(self.data)
        self.setCurrentRow(new_index)
        
    def delItem(self, index):
        self.updateValue()
        self.data.pop(index)
        self.loadItems(self.data)
        
    def saveSettings(self):      
        self.updateValue()
        dirPath  = os.path.dirname(__file__) 
        filepath = os.path.realpath(os.path.join(dirPath, "setting.pkl"))
        with open(filepath, 'wb') as f:
            pickle.dump(self.data, f)

    def loadSettings(self):
        dirPath  = os.path.dirname(__file__) 
        filepath = os.path.realpath(os.path.join(dirPath, "setting.pkl"))

        if not(os.path.isfile(filepath)) : return False
        
        with open(filepath, 'rb') as f:  
            try:
                s = pickle.load(f)
                if s:
                    self.loadItems(s)
            except Exception:
                pass
        return True
        
    def closeEvent(self, event):
        self.saveSettings()
        event.accept()
        
if __name__ == "__main__" :
    headers  = [
            "",
            "File name", 
            "Unit", 
            "ckSum",
            "ckSum hash",
            "ckSum size",
        ]
    w = HeaderSelList()
    w.show()