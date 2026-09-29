from pyrevit import forms
from Autodesk.Revit.DB import (
    FilteredElementCollector, View, ViewSheet, Element,
    ViewPlacementOnSheetStatus
)


def get_all_views(doc):
    views = FilteredElementCollector(doc)\
        .OfClass(View)\
        .WhereElementIsNotElementType()\
        .ToElements()
    return [v for v in views
            if not isinstance(v, ViewSheet) and not v.IsTemplate]


def get_view_name(view):
    return Element.Name.GetValue(view)


def get_view_by_name(views, name):
    for v in views:
        if get_view_name(v) == name:
            return v
    return None


def get_view_by_id(views, view_id):
    for v in views:
        if v.Id == view_id:
            return v
    return None


def get_views_names(doc):
    return [get_view_name(v) for v in get_all_views(doc)]


def get_views_by_name(views, views_names):
    names = set(views_names)
    return [v for v in views if get_view_name(v) in names]


def exist_view(doc, name):
    return get_view_by_name(get_all_views(doc), name) is not None


def is_view_placed(view):
    return view.GetPlacementOnSheetStatus() != ViewPlacementOnSheetStatus.NotPlaced