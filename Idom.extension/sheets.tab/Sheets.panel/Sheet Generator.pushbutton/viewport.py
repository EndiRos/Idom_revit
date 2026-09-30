from System.Collections.Generic import List


from pyrevit import script
from pyrevit import forms
from pyrevit import DB
from Autodesk.Revit.DB import Viewport
from Autodesk.Revit.DB import ViewSheet, FilteredElementCollector, Document, FamilySymbol, Transaction, SheetCollection, Element, View
from titleblock import get_all_titleblock, get_tiitleblocks_names
from sheet_Collections import get_all_collection, get_collection_by_name, create_sheet_collection


def get_all_viewports(doc):
    views = FilteredElementCollector(doc)\
        .OfClass(Viewport)\
        .WhereElementIsNotElementType()\
        .ToElements()

    real_views = [v for v in views if not isinstance(v, ViewSheet) and not v.IsTemplate]

    if not real_views:
        forms.alert("No existen vistas en el documento", title="Info")
        return False

    return real_views

def get_viewport_by_name(viewports, name):
    for view in viewports:
        if view.Name == name:
            return view
    forms.alert ("No existe viewport con ese nombre",
                 title= "Name do not exist)")
    return False

def get_vieport_by_id(viewports, id):
    for view in viewports:
            if view.Name == id:
                return view
    forms.alert ("No existe viewport con ese nombre",
                     title= "Name do not exist)")
    return False
    
def get_views_names (doc):
    names = []
    views = get_all_viewports(doc)
    for vi in views:
           name = Element.Name.GetValue(vi)
           names.append(name)
    return names


def exist_viewport(doc, name):
    views = get_all_viewports(doc)
    view = get_viewport_by_name(views, name)
    if view:
        return view
    return False   





