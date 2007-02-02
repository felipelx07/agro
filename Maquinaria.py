#!/usr/bin/env python
# -*- coding: UTF8 	-*-

from wnVentana import wnVentana
from strSQL.basicas import strSelectMaquinaria
from psycopg import connect
import debugwindow
import sys
from config import *

(CODIGO, DESCRIPCION) = range(2)

table = "maquinaria"

class Maquinaria:
    
    def __init__(self, conexion=None):
        self.ventana = "Maquinaria"
        self.columnas = ([CODIGO, "Codigo", int], 
                         [DESCRIPCION, "Descripcion", str])
        self.strSelect = strSelectMaquinaria
        self.mensaje = "La Maquinaria"
        self.llave = "descripcion_maquinaria"
        self.descripcion = "DESCRIPCION"
        wnMaquinaria = wnVentana(cnx, self, "wnMaquinaria")

if __name__ == '__main__':
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    sys.excepthook = debugwindow.show
    d = Maquinaria(cnx)