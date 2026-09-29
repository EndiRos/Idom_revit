# -*- coding: utf-8 -*-
"""
startup.py - Se ejecuta cuando PyRevit carga la extensión.
Útil para inicializar recursos o registrar eventos.
"""
from pyrevit import script

logger = script.get_logger()
logger.debug("Extensión cargada correctamente.")
