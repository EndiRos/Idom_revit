# -*- coding: utf-8 -*-

from System.ComponentModel import INotifyPropertyChanged, PropertyChangedEventArgs
from System.Collections.ObjectModel import ObservableCollection
import os
import clr

from Autodesk.Revit.UI import UIDocument
from pyrevit import forms, script
from Autodesk.Revit.DB import ElementId, Viewport,ViewType, View, ViewDuplicateOption, XYZ
from Autodesk.Revit.DB import Transaction, SheetCollection

from sheet_Collections import *
from sheet import get_all_sheets, get_all_titleblock
from viewport import *
from view import *

FILTER_MAP = {
    "rb_Todas": None,
    "rb_Plantas": ViewType.FloorPlan,
    "rb_Alzados": ViewType.Elevation,
    "rb_Secciones": ViewType.Section,
    "rb_3D": ViewType.ThreeD,
    "rb_Detalles": ViewType.Detail,
    "rb_tablas": ViewType.Schedule,
}

class ViewItem(INotifyPropertyChanged):
    def __init__(self, view):
        self.View = view                       # el objeto real de Revit, solo para usarlo al crear hojas
        self._name = view.Name
        try:
            self._scale = str(view.Scale)
        except Exception:
            self._scale = ""                   # tablas, leyendas... no tienen escala
        self._title = view.Name
        self._handlers = []

    def add_PropertyChanged(self, handler):
        self._handlers.append(handler)

    def remove_PropertyChanged(self, handler):
        self._handlers.remove(handler)

    def _notify(self, prop):
        for h in self._handlers:
            h(self, PropertyChangedEventArgs(prop))

    @property
    def Name(self):
        return self._name

    @property
    def Scale(self):
        return self._scale

    @Scale.setter
    def Scale(self, value):
        self._scale = value
        self._notify("Scale")

    @property
    def Title(self):
        return self._title

    @Title.setter
    def Title(self, value):
        self._title = value
        self._notify("Title")
    
class CollectionWindow(forms.WPFWindow):
    def __init__(self, doc, xaml_path):
        # --- Estado propio de la ventana (se define ANTES de cargar el XAML) ---
        # Así, si algún evento salta durante la carga, estos atributos ya existen.
        self.output = script.get_output()              # ventana de salida de pyRevit (para logs)
        self.doc = doc                                 # documento activo de Revit
        self.collections = get_all_collection(self.doc)      # colecciones de hojas existentes
        self.all_views = get_all_views(self.doc)             # todas las vistas "reales" (sin plantillas ni hojas)
        self.all_titleblock = get_all_titleblock(self.doc)   # tipos de cajetín disponibles
        self.selected_collection = None                # None por defecto: si cierran con la X, no hay selección
        self.selected_views_list = ObservableCollection[object]()
        self.selected_titleblock = None
        self.sheet_title_name = ""               
        self.accepted = False
        self.new_sheet = None
        self.next_num = 0

        
        forms.WPFWindow.__init__(self, xaml_path)      # a partir de aquí existen los controles (self.ViewsList, etc.)

        # --- Rellenar los controles con datos iniciales ---
        self.S_Collection.ItemsSource = self.collections
        self.S_Titleblock.ItemsSource = self.all_titleblock
        self.SelectedViews.ItemsSource = self.selected_views_list   # empieza vacía
        self.ViewsList.ItemsSource = sorted(self.all_views, key=lambda v: v.Name)  # disponibles, ordenadas por nombre
        if self.collections:
            self.S_Collection.SelectedIndex = 0        # preselecciona la primera colección

    def accept_click(self, sender, args):
        # Guarda la colección elegida y cierra; el script principal la lee después de ShowDialog()
        self.accepted = True
        self.Close()

    def cancel_click(self, sender, args):
        # Cancelar: se descarta cualquier selección
        self.selected_collection = None
        self.Close()
    def titleblock_selected(self, sende , arg):
        self.selected_titleblock = self.S_Titleblock.SelectedItem

    def sheet_title (self, sender, arg):
        self.sheet_title_name = self.S_sheet_title.Text
        
    def collection_selected(self, sender, arg):
        self.selected_collection = self.S_Collection.SelectedItem
        if self.selected_collection is None:
            return

        cole_id = self.selected_collection.Id
        hojas = get_all_sheets(self.doc)
        grupo_hojas = [s for s in hojas if s.SheetCollectionId == cole_id]

        if grupo_hojas:
            self.next_num = len(grupo_hojas) + 1
            self.S_sheet_name.Text = grupo_hojas[0].Name
            self.S_sheet_title.Text = grupo_hojas[0].Name
            self.sheet_title_name = self.S_sheet_title.Text
            self.S_sheet_name.IsReadOnly = True
            self.S_sheet_title.IsReadOnly = True
        else:
            self.next_num = 1
            self.S_sheet_name.Text = ""
            self.S_sheet_name.IsReadOnly = False
            self.S_sheet_title.IsReadOnly = False


    def new_collection_click(self, sender, arg):
        name = forms.ask_for_string(
            default="Nueva colección",
            prompt="Introduce el nombre de la colección:",
            title="Crear colección"
        )

        # Cancelar devuelve None; también validamos vacío
        if not name or not name.strip():
            return
        name = name.strip()

        # Evitar nombres duplicados
        existentes = get_all_collection(self.doc)
        if any(c.Name.lower() == name.lower() for c in existentes):
            forms.alert("Ya existe una colección con ese nombre.", title="Nombre duplicado")
            return

        with Transaction(self.doc, "Crear nueva collection") as t:
            t.Start()
            new_cole = SheetCollection.Create(self.doc, name)  # revisa la firma real
            status = t.Commit()
            print(status)

        collections = get_all_collection(self.doc)
        self.S_Collection.ItemsSource = collections

        # Buscar en la nueva lista por Id (más fiable que por referencia)
        self.S_Collection.SelectedItem = next(
            (c for c in collections if c.Id == new_cole.Id), None
        )

    def new_sheet_click(self, sender, arg):
        pass  # pendiente de implementar

    def apply_filters(self, views):
        # Aplica los filtros de la UI sobre la lista de vistas que recibe
        view_type = FILTER_MAP.get(self._get_checked_radio_name())   # tipo de vista según el radio button marcado
        if view_type is not None:                      # None = "Todas", no se filtra por tipo
            views = [v for v in views if v.ViewType == view_type]
        if self.chk_OcultarUsadas.IsChecked:           # checkbox: ocultar vistas ya colocadas en una hoja
            views = [v for v in views if not is_view_placed(v)]
        return views

    def print_items(self, cabecera, elem):
        # Utilidad de depuración: imprime el nombre de cada elemento con una cabecera
        for i in elem:
            self.output.print_md(cabecera + " " + i.Name)

    def add_view_click(self, sender, args):
        try:
            selected = list(self.ViewsList.SelectedItems)
            if not selected:
                return
            for v in selected:
                self.selected_views_list.Add(ViewItem(v))
            self.refresh_available()
        except Exception:
            import traceback
            forms.alert(traceback.format_exc(), title="Error en add_view_click")

    def remove_view_click(self, sender, args):
        try:
            selected = list(self.SelectedViews.SelectedItems)
            for item in selected:
                self.selected_views_list.Remove(item)
            self.refresh_available()
        except Exception:
            import traceback
            forms.alert(traceback.format_exc(), title="Error en remove_view_click")

    def refresh_available(self):
        chosen_ids = set(i.View.Id.Value for i in self.selected_views_list)   # .Value en Revit 2026
        filtered = self.apply_filters(self.all_views)
        filtered = [v for v in filtered if v.Id.Value not in chosen_ids]
        self.ViewsList.ItemsSource = sorted(filtered, key=lambda v: v.Name)

    def filter_changed(self, sender, args):
        try:
            if not self.IsLoaded:          # evita el evento que salta durante la carga del XAML
                return
            self.refresh_available()
        except Exception:
            import traceback
            forms.alert(traceback.format_exc(), title="Error en filter_changed")

    def _get_checked_radio_name(self):
        # Busca qué radio button de FILTER_MAP está marcado y devuelve su nombre
        for name in FILTER_MAP.keys():
            rb = getattr(self, name)                    # obtiene el control por nombre (self.rb_Plantas, etc.)
            if rb.IsChecked:
               return name
        return "rb_Todas"                               # valor de seguridad si ninguno está marcado

