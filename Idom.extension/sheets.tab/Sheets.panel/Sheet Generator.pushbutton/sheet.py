# -*- coding: utf-8 -*-

from System.Collections.Generic import List


from pyrevit import script
from pyrevit import forms
from pyrevit import DB
from pyrevit.DB import ViewSheet 
from Autodesk.Revit.DB import ViewSheet, FilteredElementCollector, Document, FamilySymbol, Transaction, SheetCollection

def get_all_sheets(doc):
    sheets = FilteredElementCollector(doc) \
        .OfClass(ViewSheet) \
        .ToElements()

    if sheets.Count == 0:
        forms.alert(
            "No existen sheets en el documento",
            title="Info"
        ) 

    return sheets

def get_sheet_by_name(sheets, name):
    for sheet in sheets:
        sheet : ViewSheet
        if sheet.Name == name:
            return sheet
    forms.alert ("No existe sheet con ese nombre",
                 title= "Name do not exist)")
    return False

def get_sheets_names (doc):
    names = []
    shts = get_all_sheets(doc)
    for sh in shts:
        names.append(sh.Name)
    return names


def exist_sheet(doc, name):
    sheets = get_all_sheets(doc)
    sheet = get_sheet_by_name(sheets, name)
    if sheet:
        return sheet
    return False   

from titleblock import get_all_titleblock, get_titleblock_by_name
from Collections import get_all_collection, get_collection_by_name, create_sheet_collection

def create_sheet (doc: Document, name, Titleblock_name, sheetcol_name):
    number = 1
    sheet = exist_sheet(doc, name) # type : ViewSheet
    if sheet:
        number =int (sheet.SheetNumber) + 1
    titles = get_all_titleblock(doc)
    block = get_titleblock_by_name(titles, Titleblock_name)
    if not block:
        return False
    cole  = get_collection_by_name(get_all_collection(doc), sheetcol_name)
    if cole == False:
        cole = create_sheet_collection(doc, sheetcol_name)
    t = Transaction(doc, "Create Sheet")
    try:
        t.Start()
        new_sheet  = ViewSheet.Create(doc, block.Id) # type : ViewSheet
        new_sheet.SheetNumber = "{:02d}".format(number)
        new_sheet.SheetCollectionId = cole.Id
        t.Commit()
        return new_sheet
    except Exception as e:
        if t.HasStarted():
            t.RollBack()
        forms.alert(
                "No se pudo crear la hoja :\n\n{}".format(e),
                title="Error"
            )
        return None
    
    

    return
