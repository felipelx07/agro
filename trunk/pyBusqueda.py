#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from string import zfill
import gobject
import gtk
from time import *
#from ctb_rutinas import  *
from gtk import TRUE, FALSE, Dialog
from calendar import *
import os
import dialogos

#~ from pyPgSQL.PgSQL import connect

class pyBusqueda(Dialog):

    def __init__(self, window = None, cnx = None, sql = None, col_filtro = None, col_retorno = None, titulos = None, texto = None, splash = None):

        if not cnx:
            raise ValueError, "No hay conección"
            return 0
        else:
            self.db_connection = cnx

        if not sql:
            raise ValueError, "No ha consulta"
            return 0
        else:
            self.query_db = sql

        if col_filtro is None:
            raise ValueError, "No hay columna a filtrar"
            return 0
        else:
            self.column_filter = col_filtro

        if col_retorno is None:
            raise ValueError, "No hay columna a retornar"
            return 0
        else:
            self.return_column = col_retorno

        if not titulos:
            raise ValueError, "No hay títulos para las columnas"
        else:
            self.column_titles = titulos


        self.len_retorno = len(titulos)
        self.splash = splash
        self.search_text = texto
        self.store = None
        self.padre = window
        Dialog.__init__(self,
                'Búsqueda',
                window,
                0,
                (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OK, gtk.RESPONSE_OK,))

        self.set_default_size(700,400)

        hbox = gtk.HBox(False, 8)
        hbox.set_border_width(8)
        self.vbox.pack_start(hbox, 1, 1, 0)

        vbox1 = gtk.VBox(False)
        vbox1.set_border_width(8)
        hbox.pack_start(vbox1, False, False, 1)
        stock = gtk.image_new_from_stock(gtk.STOCK_FIND, gtk.ICON_SIZE_DIALOG)
        vbox1.pack_start(stock, False, False, 0)

        vbox1.pack_start(
                gtk.Label(
                        """\n\nDígite el texto a buscar \nen la entrada de filtro\ny presione la tecla INTRO. \n\nLuego haga doble-click\nsobre el ítem deseado \no seleccionelo y\npresione el botón ACEPTAR"""), False, False, False)

        vbox1 = gtk.VBox(False)
        vbox1.set_border_width(8)
        hbox.pack_start(vbox1, True, True, 1)

        lbl = gtk.Label('Filtro:')
        vbox1.pack_start(lbl, False, 0)

        self.txtFiltro = gtk.Entry()
        self.txtFiltro.add_events(gtk.gdk.KEY_PRESS_MASK)
        self.txtFiltro.connect('key-press-event', self.on_entry_key_press_cb)
        self.txtFiltro.connect('changed', self.on_entry_changed_cb)

        vbox1.pack_start(self.txtFiltro, 0, 0)
        s = gtk.ScrolledWindow()

        self.list = gtk.TreeView()

        n = 0

        for i in titulos:
            column = gtk.TreeViewColumn(i, gtk.CellRendererText(), text=n)
            n = n + 1
            self.list.append_column(column)

        if self.search_text:
            self.txtFiltro.set_text(texto)

        self.list.connect("row-activated", self.on_tree_row_activated)
        selection = self.list.get_selection()
        selection.set_mode('single')

        vbox1.pack_start(s, 1, 1)

        s.add(self.list)
        
        if self.query():
            self.filter()
            self.show_all()

    def on_entry_key_press_cb(self, entry, event):
        if event.keyval == gtk.keysyms.Return:
            self.filter()

    def on_entry_changed_cb(self, entry):
        entry.set_text(entry.get_text().upper())

    def query(self):

        self.is_filter = False
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(self.query_db)
            self.recordset = cursor.fetchall()
        except:
            mensaje = str(sys.exc_info()[1])
            dialogos.error("No se pudo realizar la consulta a la base de datos", mensaje, parent=self.padre)
            return False

        if not self.recordset:
            dialogos.error("No existen datos para la búsqueda", parent=self.padre)
            return False


        cols = len(self.recordset[0])
        types = cols * [str]
        self.store = gtk.ListStore(*types)
        self.is_filter = True
        return True


    def filter(self):

        if len(self.recordset) == 0:
            return

        cols = len(self.recordset[0])
        types = cols * [gobject.TYPE_STRING]
        store = gtk.ListStore(*types)
        filtro = self.txtFiltro.get_text().upper()

        if len(filtro) > 0:
            for i in self.recordset:
                a =  [str(x) for x in i]
                i = a
                if i[self.column_filter].upper().find(filtro) > 0:
                    iter = store.append()
                    n = 0
                    for j in i:
                        desc = j
                        if isinstance(desc, bool):
                            if desc:
                                desc = "Sí"
                            else:
                                desc = "No"
                        desc = unicode(str(desc),'latin-1')
                        store.set(iter, n, desc.encode('utf-8'))
                        n = n + 1
                else:
                    if i[self.column_filter].upper()[:len(filtro)] == filtro:
                        iter = store.append()
                        n = 0
                        for j in i:
                            desc = j
                            if isinstance(desc, bool):
                                if desc:
                                    desc = "Sí"
                                else:
                                    desc = "No"
                            desc = unicode(str(desc),'latin-1')
                            store.set(iter, n, desc.encode('utf-8'))
                            n = n + 1
        else:
            for i in self.recordset:
                iter = store.append()
                n = 0
                for j in i:
                    desc = j
                    if isinstance(desc, bool):
                        if desc:
                            desc = "Sí"
                        else:
                            desc = "No"
                    desc = unicode(str(desc),'latin-1')
                    store.set(iter, n, desc.encode('utf-8'))
                    n = n + 1

        self.list.set_model(store)
        self.list.show()


    def on_tree_row_activated(self, tree, row, column):
        model, iter = self.list.get_selection().get_selected()
        if not iter:
            return 0
        self.response(gtk.RESPONSE_OK)