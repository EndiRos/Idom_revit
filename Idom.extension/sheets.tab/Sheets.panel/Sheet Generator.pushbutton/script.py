# -*- coding: utf-8 -*-
__title__ = "Sheet Generator"

from pyrevit import script
output = script.get_output()
output.print_md("0. arranca")

import traceback
try:
    import clr
    clr.AddReference("System.ObjectModel")
    clr.AddReference("WindowsBase")
    output.print_md("1a. clr OK")

    from System.Collections.ObjectModel import ObservableCollection
    from System.ComponentModel import INotifyPropertyChanged, PropertyChangedEventArgs
    output.print_md("1b. System OK")

    from Autodesk.Revit.DB import (FilteredElementCollector, ViewSheet, Transaction,
        SheetCollection, ViewDuplicateOption, XYZ, Viewport, BuiltInParameter)
    from pyrevit import forms
    output.print_md("1c. Revit/pyrevit OK")

    from sheet_Collections import *
    from sheet import *
    from viewport import *
    from view import *
    output.print_md("1d. módulos propios OK")

    from ui import ViewItem, CollectionWindow
    output.print_md("1e. ui OK")
except Exception:
    output.print_md("**FALLO EN IMPORT:**\n```\n{}\n```".format(traceback.format_exc()))
    raise

doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument #type: UIDocument

import os
xaml = os.path.join(os.path.dirname(__file__), "form.xaml")   # form.xaml junto a script.py

window = None
try:
    window = CollectionWindow(doc, xaml)
    window.ShowDialog()
except Exception:
    import traceback
    output.print_md("**ERROR:**\n```\n{}\n```".format(traceback.format_exc()))

if window and window.accepted:
    collection = window.selected_collection
    views_list = list(window.selected_views_list)
    titleblock = window.selected_titleblock

    if titleblock is None:
        forms.alert("Selecciona un formato (cajetín).")
    else:
        t = Transaction(doc, "Crear nuevo sheet con el composer")
        t.Start()
        try:
            new_sheet = ViewSheet.Create(doc, titleblock.Id)
            new_sheet.Name = window.sheet_title_name
            new_sheet.SheetNumber = str(window.next_num)
            if collection is not None:
                new_sheet.SheetCollectionId = collection.Id

            for i, v in enumerate(views_list):
                view = v.View
                try:
                    new_id = view.Duplicate(ViewDuplicateOption.Duplicate)
                except Exception as ex:
                    output.print_md("No se pudo duplicar **{}**: {}".format(view.Name, ex))
                    continue

                new_view = doc.GetElement(new_id)

                # Título en plano
                p = new_view.get_Parameter(BuiltInParameter.VIEW_DESCRIPTION)
                if p and not p.IsReadOnly:
                    p.Set(v.Title)

                # Escala
                if v.Scale:
                    try:
                        new_view.Scale = int(v.Scale)
                    except Exception as ex:
                        output.print_md("Escala no aplicada en {}: {}".format(new_view.Name, ex))

                # Colocar en la hoja (desplazadas para que no se superpongan)
                if Viewport.CanAddViewToSheet(doc, new_sheet.Id, new_view.Id):
                    Viewport.Create(doc, new_sheet.Id, new_view.Id, XYZ(0.5 + i * 1.0, 0.5, 0))

            status = t.Commit()
            output.print_md("Resultado: {}".format(status))
        except Exception:
            t.RollBack()
            import traceback
            output.print_md("**ERROR:**\n```\n{}\n```".format(traceback.format_exc()))