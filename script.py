# -*- coding: utf-8 -*-

__title__ = "Sheet Generator"

from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.DB import FilteredElementCollector, ViewSheet, Document, Transaction, SheetCollection
from Autodesk.Revit.DB import ElementId, Viewport
from pyrevit import forms, script
from Collections import *
from sheet import *
from viewport import *
from System.Collections.Generic import List




doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument #type: UIDocument

collections = list(get_all_collection(doc)) #type: SheetCollection

Sele_collections = forms.SelectFromList.show(
    collections,
    title="Selecciona coleciones",
    name_attr="Name",
    multiselect=True,
    button_name="Aceptar"
    )
if not Sele_collections:
    forms.alert("No se ha seleccionado ninguna colección")
    script.exit()

collec_ids = List[ElementId]([collection.Id for collection in Sele_collections])

uidoc.Selection.SetElementIds(collec_ids)

output = script.get_output()


sheets = get_all_sheets(doc)
transaction = Transaction(doc, "Renombrar vistas de las colecciones seleccionadas")
renamed_views = 0

try:
    transaction.Start()

    for collection in Sele_collections:
        for sheet in sheets:
            if sheet.SheetCollectionId != collection.Id:
                continue

            prefix = "{} - {} - ".format(collection.Name, sheet.Name)

            for viewport_id in sheet.GetAllViewports():
                viewport = doc.GetElement(viewport_id)
                view = doc.GetElement(viewport.ViewId)
                new_name = prefix + view.Name

                if not view.Name.startswith(prefix):
                    view.Name = new_name
                    renamed_views += 1

    transaction.Commit()
    forms.alert("Se han renombrado {} vistas".format(renamed_views), title="Sheet Generator")
except Exception as error:
    if transaction.HasStarted():
        transaction.RollBack()
    forms.alert(
        "No se pudieron renombrar las vistas:\n\n{}".format(error),
        title="Error"
    )