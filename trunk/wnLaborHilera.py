#!/usr/bin/env python
# -*- coding: UTF8 	-*-

from GladeConnect import GladeConnect
import gtk
import sys
import time
import datetime
import dialogos
import debugwindow
import SimpleTree
import ifd
from strSQL.basicas import strSelectLaborHilera
from psycopg import connect
import completion
import comunes
import treetohtml
import config

(CODIGO_HILERA,
 DESCRIPCION_HILERA,
 CODIGO_LABOR,
 DESCRIPCION_LABOR,
 FECHA,
 RUT,
 DESCRIPCION_FICHA) = range(7)

schema = config.schema
table = "labor_hilera"

class wnLaborHilera (GladeConnect):
    def __init__(self, conexion=None, padre=None, root="wnLaborHilera"):
        GladeConnect.__init__(self, "glade/wnLaborHilera.glade", root)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        if padre is None :
            self.wnLaborHilera.maximize()
            self.frm_padre = self.wnLaborHilera
        else:
            self.frm_padre = padre.frm_padre
            
        self.crea_columnas()
        self.carga_datos()

    def crea_columnas(self):
        columnas = []
        columnas.append ([DESCRIPCION_LABOR, "Labor", "str"])
        columnas.append ([DESCRIPCION_HILERA, "Hilera","str"])
        columnas.append ([FECHA, "Fecha","str"])
        columnas.append ([DESCRIPCION_FICHA, "Ficha","str"])
        
        self.modelo = gtk.ListStore(*(4*[str]))
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeLaborHilera)
        self.col_data = [x[0] for x in columnas]
        
    def on_btnImprimir_clicked(self, btn=None):
        t = treetohtml.TreeToHTML(self.treeLaborHilera,"Labor Hilera", self.col_data)
        t.show()        
    def carga_datos(self):
        
        self.modelo = ifd.ListStoreFromSQL(self.cnx, strSelectLaborHilera)
        self.treeLaborHilera.set_model(self.modelo)

    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgLaborHilera(self.cnx, self.frm_padre, False)
        dlg.editando=False
        
        dlg.entFecha.set_date(datetime.date.today())
        
        response = dlg.dlgLaborHilera.run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        
        selection = self.treeLaborHilera.get_selection()
        model, it = selection.get_selected()
        if model is None or it is None:
            return
        
        codigo_labor = model.get_value(it, CODIGO_LABOR)
        descripcion = codigo_labor
        
        if dialogos.yesno("¿Desea eliminar la Labor Hilera <b>%s</b>?\nEsta acción no se puede deshacer\n" % descripcion, self.frm_padre) == gtk.RESPONSE_YES:
            try:
                
                llaves = {'codigo_labor':codigo_labor}
                sql = ifd.deleteFromDict(config.schema + '.' + table, llaves)
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                 print sys.exc_info()[1]
                 dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nExisten datos relacionados con:\n<b>%s</b>"%descripcion)
        
    def on_btnPropiedades_clicked(self, btn=None):
        model, it = self.treeLaborHilera.get_selection().get_selected()
        if model is None or it is None:
            return
        dlg = dlgLaborHilera(self.cnx, self.frm_padre, False)
        dlg.entHilera.set_text(model.get_value(it, DESCRIPCION_HILERA))
        dlg.codigo_hilera = model.get_value(it, CODIGO_HILERA)
        dlg.pecHilera.set_selected(True)
        
        dlg.entLabor.set_text(model.get_value(it, DESCRIPCION_LABOR))
        dlg.codigo_labor = model.get_value(it, CODIGO_LABOR)
        dlg.pecLabor.set_selected(True)
        
        dlg.entFicha.set_text(model.get_value(it, DESCRIPCION_FICHA))
        dlg.rut = model.get_value(it, RUT)
        dlg.pecFicha.set_selected(True)
        
        dlg.entFecha.set_date(comunes.GetDateFromModel(model.get_value(it, FECHA).split()[0]))
        
        dlg.editando = (True)
        response = dlg.dlgLaborHilera.run()
        if response == gtk.RESPONSE_OK:
            self.modelo.clear()
            self.carga_datos()
            
    def on_btnCerrar_clicked(self, btn=None):
        if self.padre is None:
            self.on_exit()
        else:
            self.padre.remove_tab("Labor Hilera")
            
    def on_treeLaborHilera_row_activated(self, tree=None, path=None, col=None):
        self.on_btnPropiedades_clicked()


class dlgLaborHilera(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        GladeConnect.__init__(self, "glade/wnLaborHilera.glade", "dlgLaborHilera")
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.editando=editando
        self.codigo_hilera = None
        self.rut = None
        if self.editando:
            self.entCodigo.set_sensitive(False)
        
        self.pecHilera = completion.CompletionHilera(self.entHilera,
                self.sel_hilera,
                self.cnx)
        self.pecLabor = completion.CompletionLabor(self.entLabor,
                self.sel_labor,
                self.cnx)
        self.pecFicha = completion.CompletionFicha(self.entFicha,
                self.sel_ficha,
                self.cnx)
        
        self.dlgLaborHilera.show_all()

    def sel_hilera(self, completion, model, iter):
        self.codigo_hilera = model.get_value(iter, 1)
        
    def sel_labor(self, completion, model, iter):
        self.codigo_labor = model.get_value(iter, 1)
    
    def sel_ficha(self, completion, model, iter):
        self.rut = model.get_value(iter, 1)
        
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        
        fecha = self.entFecha.get_date()
        
        if self.entHilera.get_text() == "":
            dialogos.error("La hilera no puede ser vacia.")
            return
        
        if self.entFicha.get_text() == "":
            dialogos.error("La ficha no puede ser vacia.")
            return
        
        campos = {}
        llaves = {}
        campos['codigo_hilera'] = self.codigo_hilera
        campos['codigo_labor'] = self.codigo_labor
        campos['fecha'] = fecha.strftime("%Y/%m/%d")
        campos['rut']  = self.rut
        
        if not self.editando:
            sql = ifd.insertFromDict(schema + "." + table, campos)        
        else:
            llaves['codigo_labor'] = self.codigo_labor
            llaves['codigo_hilera'] = self.codigo_hilera
            sql, campos=ifd.updateFromDict(schema + "." + table, campos, llaves)
        
        try:   
            self.cursor.execute(sql, campos)
            self.dlgLaborHilera.hide()
        except:
            print sys.exc_info()[1]
            print sql
            
        
    def on_btnCancelar_clicked(self, btn=None):
        self.dlgLaborHilera.hide()
        
if __name__ == '__main__':
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    sys.excepthook = debugwindow.show
    d = wnLaborHilera(cnx)
    
    gtk.main()