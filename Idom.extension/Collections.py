
from Autodesk.Revit.DB import FilteredElementCollector, Transaction, SheetCollection
from pyrevit import forms

def get_all_collection(doc):
    collections =  FilteredElementCollector(doc).OfClass(SheetCollection).ToElements()
    if collections.Count == 0:
        forms.alert ("No existen coleciones de hojas en el documento",
                             title= "info not sheetcollections"
                    )
    return collections


def get_collection_by_name(collects , name):
    for coll in collects: # type SheetCollection
        if coll.Name == name:
            return coll
    forms.alert ("No existe sheetcollection con ese nombre",
                     title= "Name do not exist)")
    return False

def get_collection_by_id(collects, id):

    for coll in collects:  # type: SheetCollection

        if coll.Id == id:
            return coll

    forms.alert(
        "No existe sheetcollection con ese nombre",
        title="Name do not exist"
    )

    return False

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

