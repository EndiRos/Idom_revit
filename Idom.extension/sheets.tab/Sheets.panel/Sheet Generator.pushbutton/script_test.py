__title__ = "Sheet Generator"

from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.DB import FilteredElementCollector, ViewSheet, Document, Transaction, SheetCollection, FamilySymbol
from Autodesk.Revit.DB import ElementId, Viewport,Element
from pyrevit import forms, script
from Collections import *
from sheet import *
from viewport import *
from System.Collections.Generic import List
import os

output = script.get_output()
doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument #type: UIDocument

titleblock = get_all_titleblock(doc)
output.print_md("el numero de titleblocks es = {}".format(titleblock.Count))
for ti in titleblock:
    name = Element.Name.GetValue(ti)
    output.print_md("Nombre: {}".format(name))