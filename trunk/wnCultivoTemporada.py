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
from strSQL.basicas import strSelectCultivoTemporada
from psycopg import connect
import completion
import comunes
import treetohtml
import config

(CODIGO_CULTIVO,
 DESCRIPCION_CULTIVO,
 CODIGO_CUARTEL,
 DESCRIPCION_CUARTEL,
 CODIGO_TEMPORADA,
 DESCRIPCION_TEMPORADA,
) = range(6)

schema = config.schema
table = "cultivo_temporada"
cultivo = None
cuartel = None
temporada = None

class wnCultivoTemporada (GladeConnect):
    def __init__(self, conexion=None, padre=None, root="wnCultivoTemporada"):
        GladeConnect.__init__(self, "glade/wnCultivoTemporada.glade", root)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        if padre is None :
            self.wnCultivoTemporada.maximize()
            self.frm_padre = self.wnCultivoTemporada
        else:
            self.frm_padre = padre.frm_padre
            
        self.crea_columnas()
        self.carga_datos()

    def crea_columnas(self):
        columnas = []
        columnas.append ([DESCRIPCION_CULTIVO, "Cultivo","str"])
        columnas.append ([DESCRIPCION_CUARTEL, "Cuartel","str"])
        columnas.append ([DESCRIPCION_TEMPORADA, "Temporada","str"])
        
        self.modelo = gtk.ListStore(*(3*[str]))
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeCultivoTemporada)
        self.col_data = [x[0] for x in columnas]
        
    def on_btnImprimir_clicked(self, btn=None):
        t = treetohtml.TreeToHTML(self.treeCultivoTemporada,"Cultivo Temporada", self.col_data)
        t.show()        
    def carga_datos(self):
        
        self.modelo = ifd.ListStoreFromSQL(self.cnx, strSelectCultivoTemporada)
        self.treeCultivoTemporada.set_model(self.modelo)

    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgCultivoTemporada(self.cnx, self.frm_padre, False)
        dlg.editando=False
                
        response = dlg.dlgCultivoTemporada.run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        
        selection = self.treeCultivoTemporada.get_selection()
        model, it = selection.get_selected()
        if model is None or it is None:
            return
        
        cultivo = model.get_value(it, CODIGO_CULTIVO)
        cuartel = model.get_value(it, CODIGO_CUARTEL)
        temporada = model.get_value(it, CODIGO_TEMPORADA)
        llaves = {}
        
        if dialogos.yesno("¿Desea eliminar el cultivo temporada "+ 
                          "<b>%s/%s/%s</b>?\nEsta acción no se puede deshacer\n"
                         % (cultivo,cuartel,temporada), self.frm_padre) == gtk.RESPONSE_YES:
            try:
                llaves['codigo_cultivo'] = cultivo
                llaves['codigo_cuartel'] = cuartel
                llaves['codigo_temporada'] = temporada
                sql = ifd.deleteFromDict(config.schema + '.' + table, llaves)
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                 print sys.exc_info()[1]
                 dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nExisten datos"+ 
                "relacionados con:\n<b>%s/%s/%s</b>"%cultivo,cuartel,temporada)
        
    def on_btnPropiedades_clicked(self, btn=None):
        model, it = self.treeCultivoTemporada.get_selection().get_selected()
        if model is None or it is None:
            dialogos.error("Seleccione un Cultivo de Temporada para editar.")
            return
        dlg = dlgCultivoTemporada(self.cnx, self.frm_padre, False)
        
        global cultivo
        cultivo = model.get_value(it, CODIGO_CULTIVO)
        global cuartel
        cuartel = model.get_value(it, CODIGO_CUARTEL)
        global temporada
        temporada = model.get_value(it, CODIGO_TEMPORADA)
           
        dlg.entCultivo.set_text(model.get_value(it, DESCRIPCION_CULTIVO))
        dlg.codigo_cultivo = model.get_value(it, CODIGO_CULTIVO)
        dlg.pecCultivo.set_selected(True)
        
        dlg.entCuartel.set_text(model.get_value(it, DESCRIPCION_CUARTEL))
        dlg.codigo_cuartel = model.get_value(it, CODIGO_CUARTEL)
        dlg.pecCuartel.set_selected(True)
        
        dlg.entTemporada.set_text(model.get_value(it, DESCRIPCION_TEMPORADA))
        dlg.codigo_temporada = model.get_value(it, CODIGO_TEMPORADA)
        dlg.pecTemporada.set_selected(True)
           
        dlg.editando = (True)
        response = dlg.dlgCultivoTemporada.run()
        if response == gtk.RESPONSE_OK:
            self.modelo.clear()
            self.carga_datos()
            
    def on_btnCerrar_clicked(self, btn=None):
        if self.padre is None:
            self.on_exit()
        else:
            self.padre.remove_tab("Cultivo Temporada")
            
    def on_treeCultivoTemporada_row_activated(self, tree=None, path=None, col=None):
        self.on_btnPropiedades_clicked()


class dlgCultivoTemporada(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        GladeConnect.__init__(self, "glade/wnCultivoTemporada.glade", "dlgCultivoTemporada")
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.editando=editando
        if self.editando:
            self.entCodigo.set_sensitive(False)
        
        self.pecCultivo = completion.CompletionCultivo(self.entCultivo,
                self.sel_cultivo,
                self.cnx)
        self.pecCuartel = completion.CompletionCuartel(self.entCuartel,
                self.sel_cuartel,
                self.cnx)
        self.pecTemporada = completion.CompletionTemporada(self.entTemporada,
                self.sel_temporada,
                self.cnx)
        
        self.dlgCultivoTemporada.show_all()
    
    def sel_cultivo(self, completion, model, iter):
        self.codigo_cultivo = model.get_value(iter, 1)
        
    def sel_cuartel(self, completion, model, iter):
        self.codigo_cuartel = model.get_value(iter, 1)
    
    def sel_temporada(self, completion, model, iter):
        self.codigo_temporada = model.get_value(iter, 1)
        
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        if self.entCultivo.get_text() == "":
            dialogos.error("El cultivo no puede ser vacio.")
            return
        
        if self.entCuartel.get_text() == "":
            dialogos.error("El cuartel no puede ser vacio.")
            return
        
        if self.entTemporada.get_text() == "":
            dialogos.error("La temporada no puede ser vacia.")
            return
        
        campos = {}
        llaves = {}
        campos['codigo_cultivo'] = self.codigo_cultivo
        campos['codigo_cuartel'] = self.codigo_cuartel
        campos['codigo_temporada'] = self.codigo_temporada
        
        if not self.editando:
            sql = ifd.insertFromDict(schema + "." + table, campos)        
        else:
            try:
                llaves['codigo_cultivo'] = cultivo
                llaves['codigo_cuartel'] = cuartel
                llaves['codigo_temporada'] = temporada
                sql = ifd.deleteFromDict(config.schema + '.' + table, llaves)
                self.cursor.execute(sql, llaves)
            except:
                 print sys.exc_info()[1]
                 dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nExisten datos"+ 
                "relacionados con:\n<b>%s/%s/%s</b>" % 
                (cultivo,cuartel,temporada))
            
            sql = ifd.insertFromDict(schema + "." + table, campos)
        
        try:   
            self.cursor.execute(sql, campos)
            self.dlgCultivoTemporada.hide()
        except:
            print sys.exc_info()[1]
            print sql
            
        
    def on_btnCancelar_clicked(self, btn=None):
        self.dlgCultivoTemporada.hide()

    def on_dlgUnidadDosis_key_press_event(self, dialogo=None, evento=None):
        if str(evento.keyval) == "65293":
            self.on_btnAceptar_clicked(self)
            self.wnUnidadDosis.carga_datos()
        
if __name__ == '__main__':
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    sys.excepthook = debugwindow.show
    d = wnCultivoTemporada(cnx)
    
    gtk.main()
