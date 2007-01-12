#!/usr/bin/env python
# -*- coding: UTF8 	-*-

from GladeConnect import GladeConnect
import gtk
import sys
import dialogos
import debugwindow
import SimpleTree
import ifd
from strSQL.basicas import strSelectProducto
from psycopg import connect
import completion
import comunes
import treetohtml
import config

(CODIGO_PRODUCTO,
 DESCRIPCION,
 CODIGO_UNIDAD,
 DESCRIPCION_UNIDAD,
 DOSIS_PROPUESTA) = range(5)

schema = config.schema
table = "producto"

class wnProducto (GladeConnect):
    def __init__(self, conexion=None, padre=None, root="wnProducto"):
        GladeConnect.__init__(self, "glade/wnProducto.glade", root)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        if padre is None :
            self.wnProducto.maximize()
            self.frm_padre = self.wnProducto
        else:
            self.frm_padre = padre.frm_padre
            
        self.crea_columnas()
        self.carga_datos()

    def crea_columnas(self):
        columnas = []
        columnas.append ([CODIGO_PRODUCTO, "Producto", "str"])
        columnas.append ([DESCRIPCION, "Descripcion", "str"])
        columnas.append ([DESCRIPCION_UNIDAD, "Unidad","str"])
        columnas.append ([DOSIS_PROPUESTA, "Dosis","str"])
        
        self.modelo = gtk.ListStore(*(4*[str]))
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeProducto)
        self.col_data = [x[0] for x in columnas]
        
    def on_btnImprimir_clicked(self, btn=None):
        t = treetohtml.TreeToHTML(self.treeProducto,"Producto", self.col_data)
        t.show()        
    def carga_datos(self):
        
        self.modelo = ifd.ListStoreFromSQL(self.cnx, strSelectProducto)
        self.treeProducto.set_model(self.modelo)

    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgProducto(self.cnx, self.frm_padre, False)
        dlg.editando=False
        response = dlg.dlgProducto.run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        
        selection = self.treeProducto.get_selection()
        model, it = selection.get_selected()
        if model is None or it is None:
            return
        
        codigo_producto = model.get_value(it, CODIGO_PRODUCTO)
        descripcion = model.get_value(it, DESCRIPCION)
        
        if dialogos.yesno("¿Desea eliminar el Producto <b>%s</b>?\nEsta acción no se puede deshacer\n" % descripcion, self.frm_padre) == gtk.RESPONSE_YES:
            try:
                
                llaves = {'codigo_producto':codigo_producto}
                sql = ifd.deleteFromDict(config.schema + '.' + table, llaves)
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                 print sys.exc_info()[1]
                 dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nExisten datos relacionados con:\n<b>%s</b>"%descripcion)
        
    def on_btnPropiedades_clicked(self, btn=None):
        model, it = self.treeProducto.get_selection().get_selected()
        if model is None or it is None:
            return
        dlg = dlgProducto(self.cnx, self.frm_padre, False)
        dlg.entUnidad.set_text(model.get_value(it, DESCRIPCION_UNIDAD))
        dlg.codigo_unidad = model.get_value(it, CODIGO_UNIDAD)
        dlg.pecUnidad.set_selected(True)
        dlg.entDescripcion.set_text(model.get_value(it, DESCRIPCION))
        dlg.entCodigo.set_text(model.get_value(it, CODIGO_PRODUCTO))
        dlg.entDosis.set_text(model.get_value(it, DOSIS_PROPUESTA))
        dlg.editando = (True)
        response = dlg.dlgProducto.run()
        if response == gtk.RESPONSE_OK:
            self.modelo.clear()
            self.carga_datos()
            
    def on_btnCerrar_clicked(self, btn=None):
        if self.padre is None:
            self.on_exit()
        else:
            self.padre.remove_tab("Producto")
            
    def on_treeProducto_row_activated(self, tree=None, path=None, col=None):
        self.on_btnPropiedades_clicked()


class dlgProducto(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        GladeConnect.__init__(self, "glade/wnProducto.glade", "dlgProducto")
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.editando=editando
        self.codigo_unidad = None
        if self.editando:
            self.entCodigo.set_sensitive(False)
        
        self.pecUnidad = completion.CompletionUnidad(self.entUnidad,
                self.sel_unidad,
                self.cnx)
        self.dlgProducto.show()

    def sel_unidad(self, completion, model, iter):
        self.codigo_unidad = model.get_value(iter, 1)
        
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        
        if self.entDescripcion.get_text() == "":
            dialogos.error("El campo <b>Descripción Producto</b> no puede estar vacío")
            return
        
        if self.entDosis.get_text() == "":
            dialogos.error("")
        
        if self.codigo_unidad is None:
            dialogos.error("Debe escoger un <b>Producto</b>")
            return
        
        campos = {}
        llaves = {}
        campos['dosis_propuesta']  = self.entDosis.get_text().upper()
        campos['descripcion_producto']  = self.entDescripcion.get_text().upper()
        campos['codigo_unidad'] = self.codigo_unidad
        
        
        if not self.editando:
            sql = ifd.insertFromDict(schema + "." + table, campos)        
        else:
            llaves['codigo_producto'] = self.entCodigo.get_text()
            sql, campos=ifd.updateFromDict(schema + "." + table, campos, llaves)
        
        try:   
            self.cursor.execute(sql, campos)
            self.dlgProducto.hide()
        except:
            print sys.exc_info()[1]
            print sql
            
        
    def on_btnCancelar_clicked(self, btn=None):
        self.dlgProducto.hide()
        
if __name__ == '__main__':
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    sys.excepthook = debugwindow.show
    d = wnProducto(cnx)
    
    gtk.main()