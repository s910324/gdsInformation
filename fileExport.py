import os
import pya
import chk
from   datetime import date

class CellExport(object):
    def __init__(self, cell):
        super().__init__()  
        self.cell = cell
        
    def flip(self):
        layout     = self.cell.layout()
        topCell    = layout.create_cell(f"{self.cell.name}_flip")
        mirrirInst = pya.CellInstArray (self.cell, pya.Trans(2, True, 0, 0))
        topCell.insert(mirrirInst)
        self.cell  = topCell
        
    def flatten(self):
        if not(self.cell.is_leaf()):
            self.cell.flatten(True)
            
    def filterLayers(self, layers = {}):
        layout = self.cell.layout()
        expLid = [layout.layer(l[0], l[1]) for l in layers]
        
        if expLid:
            for lid in layout.layer_indexes():
                if not(lid in expLid) : layout.clear_layer(lid)
                
    def flatCellMergeLayer(self, layers = []):
        self.filterLayers(layers)
        self.flatten()
        for lydt in layers:
            layerIndex = self.cell.layout().layer(lydt[0], lydt[1])
            mergedReg  = pya.Region()
            for shape in self.cell.each_shape(layerIndex):
                if shape.polygon:
                    mergedReg.insert(shape.polygon)
                else:
                    self.cell.shapes(layerIndex).insert(shape)
                shape.delete()
            self.cell.shapes(layerIndex).insert(mergedReg.merged())
        return self.cell
    
    def childCellList(self, cell, result = []):
        for cellIndex in cell.each_child_cell():
            child = cell.layout().cell(cellIndex)
            result.append(child)
            self.childCellList(child, result)
            
        return result
        
    def cellReplace(self, tgtCellName, rpcCellName):
        layout = self.cell.layout()
        if not(layout.cell(tgtCellName)):
            print(f"Target cell {tgtCellName} not exist")
            return
            
        if not (layout.cell(rpcCellName)):
            print(f"Replace cell {rpcCellName} not exist")
            return     
            
        tgtCell  = layout.cell(tgtCellName)
        rpcCell  = layout.cell(rpcCellName)
        tw       = tgtCell.bbox().width()
        th       = tgtCell.bbox().height()
        count    = 0
        
        for c in self.childCellList(cell, []):
            cw = c.bbox().width()
            ch = c.bbox().height()
            if (cw >= tw and ch >= th):
                for i in c.each_inst():
                    if i.cell == tgtCell:
                        i.cell = rpcCell
                        count += 1
        return count
    
    def cellListReplace(self, replace = []):
        outstring  = "" 
        for tgtCellName in replace:
            rpcCellName  = replace[tgtCellName]
            replaceCount = self.cellReplace(self.cell, tgtCellName, rpcCellName)
            outstring   += f"\n\treplace #{replaceCount} | {tgtCellName} ==> {rpcCellName}"
        print(outstring)
    
    
    def processCell(self, layers = {}, flip = False, flat = False, merge = False, replace = False):
        if replace : self.cellListReplace(replace)
        if flip    : self.flip() 
        if flat    : self.flatten() 
        if merge   : self.flatCellMergeLayer(layers)
            

    def saveCell(self, folderPath, fileName, layers = {}, fmt = "GDS2", mapping = False):
        option                    = pya.SaveLayoutOptions()
        option.write_context_info = False    
        option.no_empty_cells     = True
        option.keep_instances     = False
        option.format             = {"GDS2" : "GDS2", "GDS" : "GDS2", "DXF" : "DXF"}[fmt.upper()]
        option.dxf_polygon_mode   = 0
        layout                    = self.cell.layout()
        
        if layers:
            option.deselect_all_layers()
            for lydt in layers:
                mlydt = layers[lydt] if mapping else lydt 
                option.add_layer(layout.layer(lydt[0], lydt[1]), pya.LayerInfo(mlydt[0], mlydt[1]))  
        else:
            option.select_all_layers()

        if not os.path.exists(folderPath) : os.makedirs(folderPath)
        fileFullPath = f"{folderPath}{fileName}"
        self.cell.write(fileFullPath, option)
        print (chk.gdsInfo(fileFullPath))
        return f"{fileFullPath}" 

        
    def outputCell(self, layers = [], prefix = "", suffix = "", fmt = "GDS2",
        mapping = False, flip = False, flat = False, merge = False, replace = False, **kwargs):
        
        mainWindow = pya.Application.instance().main_window()
        layoutView = mainWindow.current_view()                
        cellView   = layoutView.active_cellview() 
        
        nowDate    = date.today().strftime("%Y%m%d")
        prefix     = f"{prefix}_" if prefix else prefix
        suffix     = f"_{suffix}" if suffix else suffix
        filefmt    =  {"GDS2" : "gds", "GDS" : "gds", "DXF" : "dxf"}[fmt.upper()]
        
        path       = "/".join(cellView.active().filename().replace("/", "\\").split("\\")[0:-1])
        folderPath = f"{path}/output/{prefix}output/"
        attri     = "".join([
            "_LMP" * mapping, "_FLP"    * flip, "_FLT" * flat, 
            "MRG"   * merge,   "_RPC" * replace
        ])
        
        cellName   = self.cell.name
        fileName   = f"{prefix}{cellName}{suffix}_{nowDate}{attri}.{filefmt}"
        self.processCell(layers, flip = flip, flat = flat, merge = merge, replace = replace)
        self.saveCell(folderPath, fileName, layers = layers, fmt = fmt, mapping = mapping)
   
def exp(*args, **kwargs):
    cellName     = kwargs["cell"]
    layout       = pya.Application.instance().main_window().current_view().active_cellview().layout().dup()  
    cell         = layout.cell(cellName)
    if cell:
        CellExport(cell).outputCell(**kwargs)
    else:
        print (f"cell '{cellName}' not exist")
    