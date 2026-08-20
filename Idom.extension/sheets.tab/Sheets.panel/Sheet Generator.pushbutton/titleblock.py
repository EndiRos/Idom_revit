from Autodesk.Revit.DB import FilteredElementCollector, Document, FamilySymbol
from pyrevit import DB, forms
 

def get_all_titleblock(doc):
    blocks = FilteredElementCollector(doc)\
        .OfClass(FamilySymbol)\
        .OfCategory(DB.BuiltInCategory.OST_TitleBlocks)\
        .ToElements() # type : FamilySymbol
    if blocks.Count == 0:
        forms.alert ("No existe formatos en el documennto",
                     title = "info not titleblock")
        return False
    return blocks

def get_titleblock_by_name (blocks, name):
    for block in blocks: # type : FamilySymbol
        if block.Name == name:
            return block
    forms.alert ("el formato no existe", title= "Titleblock not exist")
    return False

def get_tiitleblocks_names(doc):
    names = []
    blocks = get_all_titleblock(doc)
    for bl in blocks:
        names.append(bl.Name)
    return names