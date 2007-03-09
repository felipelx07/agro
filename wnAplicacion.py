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
from strSQL.basicas import strSelectAplicacion
from psycopg import connect
import completion
import comunes
import treetohtml
import config
import datetime

(CODIGO_APLICACION,
 CODIGO_HILERA,
 CODIGO_PRODUCTO,
 DESCRIPCION_HILERA,
 DESCRIPCION_PRODUCTO,
 DOSIS,
 FECHA,
 RUT,
 DESCRIPCION_FICHA,
 CODIGO_MAQUINARIA,
 CODIGO_IMPLEMENTO,
 DESCRIPCION_MAQUINARIA,
 DESCRIPCION_IMPLEMENTO,
 CODIGO_TEMPORADA,
 DESCRIPCION_TEMPORADA) = range(15)

schema = config.schema
table = "aplicacion"

class wnAplicacion (GladeConnect):
    def __init__(self, conexion=None, padre=None, root="wnAplicacion"):
        GladeConnect.__init__(self, "glade/wnAplicacion.glade", root)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        if padre is None :
            self.wnAplicacion.maximize()
            self.frm_padre = self.wnAplicacion
        else:
            self.frm_padre = padre.frm_padre
            
        self.crea_columnas()
        self.carga_datos()

    def crea_columnas(self):
        columnas = []
        columnas.append ([CODIGO_APLICACION, "Aplicacion", "str"])
        columnas.append ([DESCRIPCION_HILERA, "Hilera","str"])
        columnas.append ([DESCRIPCION_PRODUCTO, "Producto","str"])
        columnas.append ([DOSIS, "Dosis","str"])
        columnas.append ([FECHA, "Fecha","dte"])
        columnas.append ([DESCRIPCION_FICHA, "Ficha","str"])
        columnas.append ([DESCRIPCION_MAQUINARIA, "Maquinaria","str"])
        columnas.append ([DESCRIPCION_IMPLEMENTO, "Implemento","str"])
        columnas.append ([DESCRIPCION_TEMPORADA, "Temporada","str"])
        
        self.modelo = gtk.ListStore(*(9*[str]))
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeAplicacion)
        self.col_data = [x[0] for x in columnas]
        
    def on_btnImprimir_clicked(self, btn=None):
        t = treetohtml.TreeToHTML(self.treeAplicacion,"Aplicacion", self.col_data)
        t.show()        
    def carga_datos(self):
        
        self.modelo = ifd.ListStoreFromSQL(self.cnx, strSelectAplicacion)
        self.treeAplicacion.set_model(self.modelo)

    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgAplicacion(self.cnx, self.frm_padre, False)
        dlg.editando=False
        
        dlg.entFecha.set_date(datetime.date.today())
        
        response = dlg.dlgAplicacion.run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        
        selection = self.treeAplicacion.get_selection()
        model, it = selection.get_selected()
        if model is None or it is None:
            return
        
        codigo_aplicacion = model.get_value(it, CODIGO_APLICACION)
        
        if dialogos.yesno("¿Desea eliminar la Aplicacion <b>%s</b>?\nEsta acción no se puede deshacer\n" % codigo_aplicacion, self.frm_padre) == gtk.RESPONSE_YES:
            try:
                
                llaves = {'codigo_aplicacion':codigo_aplicacion}
                sql = ifd.deleteFromDict(config.schema + '.' + table, llaves)
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                 print sys.exc_info()[1]
                 dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nExisten datos relacionados con:\n<b>%s</b>"%descripcion)
        
    def on_btnPropiedades_clicked(self, btn=None):
        model, it = self.treeAplicacion.get_selection().get_selected()
        if model is None or it is None:
            return
        dlg = dlgAplicacion(self.cnx, self.frm_padre, False)
        dlg.entHilera.set_text(model.get_value(it, DESCRIPCION_HILERA))
        dlg.codigo_hilera = model.get_value(it, CODIGO_HILERA)
        dlg.pecHilera.set_selected(True)
        
        dlg.entProducto.set_text(model.get_value(it, DESCRIPCION_PRODUCTO))
        dlg.codigo_producto = model.get_value(it, CODIGO_PRODUCTO)
        dlg.pecProducto.set_selected(True)
        
        dlg.entFicha.set_text(model.get_value(it, DESCRIPCION_FICHA))
        dlg.rut = model.get_value(it, RUT)
        dlg.pecFicha.set_selected(True)
        
        dlg.entFecha.set_date(comunes.GetDateFromModel(model.get_value(it, FECHA).split()[0]))
        
        dlg.entCodigo.set_text(model.get_value(it, CODIGO_APLICACION))
        dlg.entDosis.set_text(model.get_value(it, DOSIS))
        
        dlg.entMaquinaria.set_text(model.get_value(it, DESCRIPCION_MAQUINARIA))
        dlg.codigo_maquinaria = model.get_value(it, CODIGO_MAQUINARIA)
        dlg.pecMaquinaria.set_selected(True)
        
        dlg.entImplemento.set_text(model.get_value(it, DESCRIPCION_IMPLEMENTO))
        dlg.codigo_implemento = model.get_value(it, CODIGO_IMPLEMENTO)
        dlg.pecImplemento.set_selected(True)
        
        dlg.entTemporada.set_text(model.get_value(it, DESCRIPCION_TEMPORADA))
        dlg.codigo_temporada = model.get_value(it, CODIGO_TEMPORADA)
        dlg.pecTemporada.set_selected(True)
        
        dlg.editando = (True)
        response = dlg.dlgAplicacion.run()
        if response == gtk.RESPONSE_OK:
            self.modelo.clear()
            self.carga_datos()
            
    def on_btnCerrar_clicked(self, btn=None):
        if self.padre is None:
            self.on_exit()
        else:
            self.padre.remove_tab("Aplicacion")
            
    def on_treeAplicacion_row_activated(self, tree=None, path=None, col=None):
        self.on_btnPropiedades_clicked()


class dlgAplicacion(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        GladeConnect.__init__(self, "glade/wnAplicacion.glade", "dlgAplicacion")
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.editando=editando
        self.codigo_hilera = None
        self.codigo_producto = None
        self.codigo_maquinaria = None
        self.codigo_implemento = None
        self.rut = None
        self.codigo_temporada = None
        if self.editando:
            self.entCodigo.set_sensitive(False)
        
        self.pecHilera = completion.CompletionHilera(self.entHilera,
                self.sel_hilera,
                self.cnx)
        self.pecProducto = completion.CompletionProducto(self.entProducto,
                self.sel_producto,
                self.cnx)
        self.pecFicha = completion.CompletionFicha(self.entFicha,
                self.sel_ficha,
                self.cnx)
        self.pecMaquinaria = completion.CompletionMaquinaria(self.entMaquinaria,
                self.sel_maquinaria,
                self.cnx)
        self.pecImplemento = completion.CompletionImplemento(self.entImplemento,
                self.sel_implemento,
                self.cnx)
        self.pecTemporada = completion.CompletionTemporada(self.entTemporada,
                self.sel_temporada,
                self.cnx)
        self.dlgAplicacion.show_all()

    def sel_hilera(self, completion, model, iter):
        self.codigo_hilera = model.get_value(iter, 1)
        
    def sel_producto(self, completion, model, iter):
        self.codigo_producto = model.get_value(iter, 1)
        if not self.editando:
            self.entDosis.set_text(model.get_value(iter, 2))
    
    def sel_ficha(self, completion, model, iter):
        self.rut = model.get_value(iter, 1)
    
    def sel_maquinaria(self, completion, model, iter):
        self.codigo_maquinaria = model.get_value(iter, 1)
        
    def sel_implemento(self, completion, model, iter):
        self.codigo_implemento = model.get_value(iter, 1)
        
    def sel_temporada(self, completion, model, iter):
        self.codigo_temporada = model.get_value(iter, 1)
        
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        
        fecha = self.entFecha.get_date()
        
        if self.entHilera.get_text() == "":
            dialogos.error("La hilera no puede ser vacia.")
            return
                
        if self.entProducto.get_text() == "":
            dialogos.error("El producto no puede ser vacio.")
            return
                
        if self.entMaquinaria.get_text() == "":
            dialogos.error("La maquinaria no puede ser vacia.")
            return
               
        if self.entImplemento.get_text() == "":
            dialogos.error("El implemento no puede ser vacio.")
            return
                
        if self.entDosis.get_text() == "":
            dialogos.error("La dosis no puede ser vacia.")
            return
        
        if self.entFicha.get_text() == "":
            dialogos.error("La ficha no puede ser vacia.")
            return
        
        if self.entTemporada.get_text() == "":
            dialogos.error("La temporada no puede ser vacia.")
            return
        
        campos = {}
        llaves = {}
        
        campos['codigo_hilera'] = self.codigo_hilera
        campos['codigo_producto'] = self.codigo_producto
        campos['dosis']  = self.entDosis.get_text().upper()
        campos['fecha'] = fecha.strftime("%Y/%m/%d")
        campos['rut']  = self.rut
        campos['codigo_maquinaria'] = self.codigo_maquinaria
        campos['codigo_implemento'] = self.codigo_implemento
        campos['codigo_temporada'] = self.codigo_temporada
        
        if not self.editando:
            sql = ifd.insertFromDict(schema + "." + table, campos)        
        else:
            llaves['codigo_aplicacion'] = self.entCodigo.get_text()
            sql, campos=ifd.updateFromDict(schema + "." + table, campos, llaves)
        
        try:   
            self.cursor.execute(sql, campos)
            self.dlgAplicacion.hide()
        except:
            print sys.exc_info()[1]
            print sql
            
        
    def on_btnCancelar_clicked(self, btn=None):
        self.dlgAplicacion.hide()
        
if __name__ == '__main__':
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    sys.excepthook = debugwindow.show
    d = wnAplicacion(cnx)
    
    gtk.main()
