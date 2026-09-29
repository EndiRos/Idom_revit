# -*- coding: utf-8 -*-

__title__ = "Sheet Generator"

from Autodesk.Revit.UI import UIDocument
from Autodesk.Revit.DB import FilteredElementCollector, ViewSheet, Document, Transaction, SheetCollection
from Autodesk.Revit.DB import ElementId, Viewport,ViewType, View, ViewDuplicateOption, XYZ
from pyrevit import forms, script
from Collections import *
from sheet import *
from viewport import *
from view import *
from System.Collections.Generic import List
import os

FILTER_MAP = {
    "rb_Todas": None,
    "rb_Plantas": ViewType.FloorPlan,
    "rb_Alzados": ViewType.Elevation,
    "rb_Secciones": ViewType.Section,
    "rb_3D": ViewType.ThreeD,
    "rb_Detalles": ViewType.Detail,
    "rb_tablas": ViewType.Schedule,
}

    
class CollectionWindow(forms.WPFWindow):
    def __init__(self, doc):
        # --- Estado propio de la ventana (se define ANTES de cargar el XAML) ---
        # Así, si algún evento salta durante la carga, estos atributos ya existen.
        self.output = script.get_output()              # ventana de salida de pyRevit (para logs)
        self.doc = doc                                 # documento activo de Revit
        self.collections = get_all_collection(self.doc)      # colecciones de hojas existentes
        self.all_views = get_all_views(self.doc)             # todas las vistas "reales" (sin plantillas ni hojas)
        self.all_titleblock = get_all_titleblock(self.doc)   # tipos de cajetín disponibles
        self.selected_collection = None                # None por defecto: si cierran con la X, no hay selección
        self.selected_views_list = [] 
        self.selected_titleblock = None
        self.sheet_title_name = ""               
        self.accepted = False
        self.new_sheet = None
        self.next_num = 0

        # --- Carga del XAML ---
        xaml_path = os.path.join(
            os.path.dirname(__file__),
            "form.xaml"
        )
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

    def refresh_available(self):
        """Recalcula ViewsList a partir de all_views: filtros + excluye seleccionadas."""
        filtered = self.apply_filters(self.all_views)                       # 1. filtros de tipo y "en uso"
        filtered = [v for v in filtered if v not in self.selected_views_list]  # 2. quita las ya elegidas
        self.ViewsList.ItemsSource = sorted(filtered, key=lambda v: v.Name)    # 3. ordena y actualiza la lista visible

    def print_items(self, cabecera, elem):
        # Utilidad de depuración: imprime el nombre de cada elemento con una cabecera
        for i in elem:
            self.output.print_md(cabecera + " " + i.Name)

    def filter_changed(self, sender, args):
        # Se dispara al cambiar un radio button o el checkbox; simplemente recalcula la lista
        self.refresh_available()

    def add_view_click(self, sender, args):
        selected = list(self.ViewsList.SelectedItems)   # copia a lista Python de lo marcado en "disponibles"
        if not selected:
            return                                      # nada marcado, no hay nada que hacer
        self.selected_views_list.extend(selected)       # las añade a la fuente de verdad
        self.SelectedViews.ItemsSource = None           # truco: se pone a None para forzar que WPF refresque
        self.SelectedViews.ItemsSource = self.selected_views_list
        self.refresh_available()                        # las quita de "disponibles" (ya no cumplen "no seleccionada")

    def remove_view_click(self, sender, args):
        selected = list(self.SelectedViews.SelectedItems)   # lo marcado en la lista de "seleccionadas"
        if not selected:
            return
        # Se crea una lista NUEVA sin las quitadas (aquí se reasigna el atributo, no se muta)
        self.selected_views_list = [v for v in self.selected_views_list if v not in selected]
        self.SelectedViews.ItemsSource = self.selected_views_list
        self.refresh_available()                        # vuelven a "disponibles" solo si cumplen los filtros activos

    def _get_checked_radio_name(self):
        # Busca qué radio button de FILTER_MAP está marcado y devuelve su nombre
        for name in FILTER_MAP.keys():
            rb = getattr(self, name)                    # obtiene el control por nombre (self.rb_Plantas, etc.)
            if rb.IsChecked:
                return name
        return "rb_Todas"                               # valor de seguridad si ninguno está marcado



output = script.get_output()
doc = __revit__.ActiveUIDocument.Document  # type: Document
uidoc = __revit__.ActiveUIDocument #type: UIDocument

try:
    #output.print_md("Colecciones: {}".format(len(collections)))
    window = CollectionWindow(doc)
    window.ShowDialog()
except Exception as e:
    import traceback
    output.print_md("**ERROR:**\n```\n{}\n```".format(traceback.format_exc()))

if window.accepted:
    output.print_md("hasta aqui llega 1")

    collection = window.selected_collection
    views_list = window.selected_views_list
    titleblock = window.selected_titleblock
    title = window.sheet_title_name
    views = []

    with Transaction(doc, "Crear nuevo sheet con el composer") as t:
        t.Start()
        new_sheet = ViewSheet.Create(doc, titleblock.Id)
        new_sheet.Name = title
        new_sheet.SheetNumber = str(window.next_num)

        if collection is not None:
            new_sheet.SheetCollectionId = collection.Id

        for v in views_list:
            output.print_md("Duplicando: {}".format(v.Name))
            view_dupl_id = v.Duplicate(ViewDuplicateOption.Duplicate)
            output.print_md("Nuevo id: {}".format(view_dupl_id))
            new_view = doc.GetElement(view_dupl_id)
            output.print_md("Nueva vista: {}".format(new_view))
            new_view.Name = v.Name + title
            output.print_md("nombre vista: {}".format(new_view.Name))
            
            if Viewport.CanAddViewToSheet(doc, new_sheet.Id, new_view.Id):
                Viewport.Create(doc, new_sheet.Id, new_view.Id, XYZ(0.5, 0.5, 0))

            

        status = t.Commit()

    output.print_md(status)
    
    """ transaction.Start()
    for v in views:
        if not Viewport.CanAddViewToSheet(doc, new_sheet.Id, v.Id):
            continue   # ya está en otra hoja, o no se puede colocar
        punto = XYZ(0, 0, 0)  # posición en coordenadas de la hoja (pies)
        viewport = Viewport.Create(doc, new_sheet.Id, v.Id, punto)
    transaction.Commit() """

"""·
transaction = Transaction(doc, "Crear nuevo sheet con el composer")


collections = list(get_all_collection(doc)) #type: SheetCollection
output.print_md("Colecciones encontradas: {}".format(len(collections)))
window = CollectionWindow(collections)
output.print_md("Hata aqui 2")
window.ShowDialog()

Sele_collections = window.selected_collections

if not Sele_collections:
    forms.alert("No se ha seleccionado ninguna colección")
    script.exit()

collec_ids = List[ElementId]([collection.Id for collection in Sele_collections])

uidoc.Selection.SetElementIds(collec_ids)

output.log_debug("Hata aqui 2")


sheets = get_all_sheets(doc)
transaction = Transaction(doc, "Renombrar vistas de las colecciones seleccionadas")
renamed_views = 0
output.log_debug("Hata aqui 3")
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


  """