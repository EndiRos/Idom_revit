# -*- coding: utf-8 -*-

__title__ = "Sheet Generator"

from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.DB import FilteredElementCollector, ViewSheet, Document, Transaction, SheetCollection
from Autodesk.Revit.DB import ElementId
from pyrevit import forms, script
from Collections import *
from sheet import *
from System.Collections.Generic import List




doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument #type: UIDocument

collections = list(get_all_collection(doc)) #type: SheetCollection

Sele_collections = forms.SelectFromList.show(
    collections,
    title="Selecciona coleciones",
    name_attr="Name",
    multiselect=True,
    buton_name="Acrptar"
    )
if not Sele_collections:
    forms.alert("no se ha selecionado ninguna coleccion")

collec_ids = List[ElementId]([collection.Id for collection in Sele_collections])

sel = uidoc.Selection.SetElementIds(collec_ids) 
                                              
output = script.get_output()



sheets = get_all_sheets(doc)

for col_id in collec_ids:
    
    for sheet in sheets: # type : ViewSheet
        if sheet.
        print (get_collection_by_id(get_all_collection(doc), sheet.SheetCollectionId).Name)
    # print (get_collection_by_name(get_all_collection(doc), "asjsaj").Id)
        colec = create_sheet_collection(doc, "B4468-DD-IDIC-1060")