# -*- coding: utf-8 -*-

from System.Collections.Generic import List


from typing import cast

from pyrevit import script
from pyrevit import forms
from pyrevit import DB
from Autodesk.Revit.DB import ViewSheet, FilteredElementCollector, Document, FamilySymbol, Transaction, SheetCollection

def get_all_titleblock(doc:Document):
    blocks = cast(List [FamilySymbol], FilteredElementCollector(doc).OfClass(FamilySymbol).OfCategory(DB.BuiltInCategory.OST_TitleBlocks).ToElements())
    if not blocks:
        forms.alert ("No existe formatos en el documennto",
                     title = "info not titleblock")
    return blocks

def get_titleblock_by_name (blocks :List [FamilySymbol], name):
    for block in blocks:
        block : FamilySymbol
        if block.Name == name:
            return block
    forms.alert ("el formato no existe", title= "Titleblock nort exist")
    return False



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

def get_sheet_by_name(sheets: List[ViewSheet], name):
    for sheet in sheets:
        sheet : ViewSheet
        if (sheet.Name == name)
            return sheet
    forms.alert ("No existe sheet con ese nombre",
                 title= "Name do not exist)")
    return False



def get_all_sheet_coll(doc : Document):
    collections = cast (List [SheetCollection], FilteredElementCollector(doc).OfClass(SheetCollection).ToElements())
    if not collections:
        forms.alert ("No existen coleciones de hojas en el documento",
                             title= "info not sheetcollections"
                    )
    return sheets

def get_collection_by_name(collects , name):
    for coll in collects: # type SheetCollection
        coll : SheetCollection
        if coll.Name == name:
            return coll
    forms.alert ("No existe sheetcollection con ese nombre",
                     title= "Name do not exist)")
    return False

def exist_sheet(doc, name):
    sheets = get_all_sheets(doc)
    sheet = get_sheet_by_name(sheets, name)
    if sheet:
        return sheet
    return False   



def cratenot_sheet (doc: Document, name, Titleblock_name, sheetcol_name):
    number = 1
    sheet = exist_sheet(doc, name) # type : ViewSheet
    if sheet:
        number =int (sheet.SheetNumber)
    titles = get_all_titleblock(doc)
    block = get_titleblock_by_name(titles, Titleblock_name)
    if not block:
        return False
    t = Transaction(doc, "Create Sheet Collection")
    try:
        t.Start()
        new_sheet  = ViewSheet.Create(doc, block.Id) # type : ViewSheet
        cole  = get_collection_by_name(get_all_sheet_coll(doc), sheetcol_name)
        new_sheet.SheetCollectionId = cole.Id
        new_sheet.
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


def create_sheet_collection(doc, name):
    t = Transaction(doc, "Create Sheet Collection")
    try:
        t.Start()
        collection = SheetCollection.Create(doc, name)
        t.Commit()
        return collection
    except Exception as e:
        if t.HasStarted():
            t.RollBack()
        forms.alert(
            "No se pudo crear la Sheet Collection:\n\n{}".format(e),
            title="Error"
        )
        return None