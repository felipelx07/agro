#!/usr/bin/env python
# -*- coding: UTF8 	-*-

from GladeConnect import GladeConnect
import gtk
import sys
import dialogos
import debugwindow
import SimpleTree
import ifd
from strSQL.basicas import strSelectTemporada
from psycopg import connect
import completion
import comunes
import treetohtml
import datetime
import config

(CODIGO,
 INICIO,
 TERMINO,
 DESCRIPCION,
 ABIERTA) = range(5)

schema = config.schema
table = "temporada"

class wnTemporada (GladeConnect):
        
    def __init__(self, conexion=None, padre=None, root="wnTemporada"):
        GladeConnect.__init__(self, "glade/wnTemporada.glade", root)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        if padre is None :
            self.wnTemporada.maximize()
            self.frm_padre = self.wnTemporada
        else:
            self.frm_padre = self.padre.frm_padre
            
        self.crea_columnas()
        self.carga_datos()
        
    
    def crea_columnas(self):
        columnas = []
        columnas.append ([CODIGO, "Codigo", "str"])
        columnas.append ([INICIO, "Fecha de inicio", "dte"])
        columnas.append ([TERMINO, "Fecha de termino", "dte"])
        columnas.append ([DESCRIPCION, "Descripción", "str"])
        columnas.append ([ABIERTA, "Temporada Abierta", "bool"])
        
        self.modelo = gtk.ListStore(str, str, str, str, bool)
        
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeTemporada)
        self.col_data = [x[0] for x in columnas]
        
    def on_btnImprimir_clicked(self, btn=None):
        t = treetohtml.TreeToHTML(self.treeTemporada,"Temporada", self.col_data)
        t.show()        

    def carga_datos(self):
        m = ifd.ListStoreFromSQL(self.cnx, strSelectTemporada)
        self.modelo.clear()
        for x in m:
            if x[4] == "1":
                self.modelo.append((x[0], x[1], x[2], x[3], True))
            else:
                self.modelo.append((x[0], x[1], x[2], x[3], False))
                
        self.treeTemporada.set_model(self.modelo)

    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgTemporada(self.cnx, self.frm_padre, False)
        dlg.editando=False
        
        dlg.entInicio.set_date(datetime.date.today())        
        dlg.entTermino.set_date(datetime.datetime(datetime.date.today().year + 1, datetime.date.today().month, datetime.date.today().day))
        
        response = dlg.dlgTemporada.run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        model, it = self.treeTemporada.get_selection().get_selected()
        if model is None or it is None:
            return
        codigo = model.get_value(it, CODIGO)
        descripcion = model.get_value(it, DESCRIPCION)
        
        if dialogos.yesno("¿Desea eliminar la Temporada <b>%s</b>?\nEsta acción no se puede deshacer\n" % descripcion, self.frm_padre) == gtk.RESPONSE_YES:
            llaves = {'codigo_temporada':codigo}
            sql = ifd.deleteFromDict(schema + "." + table, llaves)
            try:
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                print sys.exc_info()[1]
                dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nEl Temporada <b>%s</b>, esta relacionada con "%descripcion)
        
    def on_btnPropiedades_clicked(self, btn=None):

        model, it = self.treeTemporada.get_selection().get_selected()
        if model is None or it is None:
            dialogos.error("Seleccione una Temporada para editar.")
            return
        
        dlg = dlgTemporada(self.cnx, self.frm_padre, False)
        dlg.entCodigo.set_text(model.get_value(it, CODIGO))
        fecha = comunes.GetDateFromModel(model.get_value(it, INICIO).split()[0])
        
        dlg.entInicio.set_date(fecha)
        fecha = comunes.GetDateFromModel(model.get_value(it, TERMINO).split()[0])
        dlg.entTermino.set_date(fecha)
        dlg.entDescripcion.set_text(model.get_value(it, DESCRIPCION))
       
        dlg.editando = True
        response = dlg.dlgTemporada.run()
        if response == gtk.RESPONSE_OK:
            self.modelo.clear()
            self.carga_datos()
            
    def on_btnCerrar_clicked(self, btn=None):
        if self.padre is None:
            self.on_exit()
        else:
            self.padre.remove_tab("Temporada")
            
    def on_treeTemporada_row_activated(self, tree=None, path=None, col=None):
        self.on_btnPropiedades_clicked()


class dlgTemporada(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        GladeConnect.__init__(self, "glade/wnTemporada.glade", "dlgTemporada")
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.entInicio.grab_focus()
        
        self.editando=editando
        self.codigo_tipo_ficha = None
        if self.editando:
            self.entCodigo.set_sensitive(False)
        self.dlgTemporada.show_all()
    
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        campos = {}
        llaves = {}
        fecha = self.entInicio.get_date()
        campos['fecha_inicio']  = fecha.strftime("%Y/%m/%d")
        fecha = self.entTermino.get_date()
        campos['fecha_termino'] = fecha.strftime("%Y/%m/%d")
        
        if self.chkAbierta.get_active():
            campos['abierta'] = "TRUE"
        else:
            campos['abierta'] = "FALSE"
            
        if not self.editando:
            sql = ifd.insertFromDict(schema + "." + table, campos)
        else:
            llaves['codigo_temporada'] = self.entCodigo.get_text().upper()
            sql, campos=ifd.updateFromDict(schema + "." + table, campos, llaves)
            
        self.cursor.execute(sql, campos)
        self.dlgTemporada.hide()
        
    def on_btnCancelar_clicked(self, btn=None):
        self.dlgTemporada.hide()
        
if __name__ == '__main__':
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    sys.excepthook = debugwindow.show
    d = wnTemporada(cnx)
    
    gtk.main()
