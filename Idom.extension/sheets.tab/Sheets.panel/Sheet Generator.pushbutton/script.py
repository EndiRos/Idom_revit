# -*- coding: utf-8 -*-

__title__ = "Sheet Generator"

from Autodesk.Revit.DB import FilteredElementCollector, ViewSheet, Document, Transaction, SheetCollection

from pyrevit import forms, script


doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument
output = script.get_output()


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


sheets = get_all_sheets(doc)

for sheet in sheets: # type : ViewSheet
    print(sheet.Name)
    print (get_collection_by_id(get_all_collection(doc), sheet.SheetCollectionId).Name)
   # print (get_collection_by_name(get_all_collection(doc), "asjsaj").Id)
    colec = create_sheet_collection(doc, "B4468-DD-IDIC-1060")