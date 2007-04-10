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
from strSQL.basicas import strSelectRegistroEstadoFenologico
from psycopg import connect
import completion
import comunes
import treetohtml
import config

(CODIGO_REGISTRO_ESTADO_FENOLOGICO,
 CODIGO_CULTIVO,
 DESCRIPCION_CULTIVO,
 CODIGO_CUARTEL,
 DESCRIPCION_CUARTEL,
 CODIGO_ESTADO_FENOLOGICO,
 DESCRIPCION_ESTADO_FENOLOGICO,
 CODIGO_TEMPORADA,
 DESCRIPCION_TEMPORADA,
 FECHA) = range(10)

schema = config.schema
table = "registro_estado_fenologico"

class wnRegistroEstadoFenologico (GladeConnect):
    def __init__(self, conexion=None, padre=None, root="wnRegistroEstadoFenologico"):
        GladeConnect.__init__(self, "glade/wnRegistroEstadoFenologico.glade", root)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        if padre is None :
            self.wnRegistroEstadoFenologico.maximize()
            self.frm_padre = self.wnRegistroEstadoFenologico
        else:
            self.frm_padre = padre.frm_padre
            
        self.crea_columnas()
        self.carga_datos()

    def crea_columnas(self):
        columnas = []
        columnas.append ([CODIGO_REGISTRO_ESTADO_FENOLOGICO, "Codigo", "str"])
        columnas.append ([DESCRIPCION_CULTIVO, "Cultivo","str"])
        columnas.append ([DESCRIPCION_CUARTEL, "Cuartel","str"])
        columnas.append ([DESCRIPCION_ESTADO_FENOLOGICO, "Estado Fenologico","str"])
        columnas.append ([DESCRIPCION_TEMPORADA, "Temporada","str"])
        columnas.append ([FECHA, "Fecha","dte"])
        
        self.modelo = gtk.ListStore(*(5*[str]))
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeRegistroEstadoFenologico)
        self.col_data = [x[0] for x in columnas]
        
    def on_btnImprimir_clicked(self, btn=None):
        t = treetohtml.TreeToHTML(self.treeRegistroEstadoFenologico,"Registro Estado Fenologico", self.col_data)
        t.show()        
    def carga_datos(self):
        
        self.modelo = ifd.ListStoreFromSQL(self.cnx, strSelectRegistroEstadoFenologico)
        self.treeRegistroEstadoFenologico.set_model(self.modelo)

    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgRegistroEstadoFenologico(self.cnx, self.frm_padre, False)
        dlg.editando=False
        
        dlg.entFecha.set_date(datetime.date.today())
        
        response = dlg.dlgRegistroEstadoFenologico.run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        
        selection = self.treeRegistroEstadoFenologico.get_selection()
        model, it = selection.get_selected()
        if model is None or it is None:
            return
        
        codigo = model.get_value(it, CODIGO_REGISTRO_ESTADO_FENOLOGICO)
        
        if dialogos.yesno("¿Desea eliminar el Registro de Estado Fenologico <b>%s</b>?\nEsta acción no se puede deshacer\n" % codigo, self.frm_padre) == gtk.RESPONSE_YES:
            try:
                llaves = {'codigo_registro_estado_fenologico':codigo}
                sql = ifd.deleteFromDict(config.schema + '.' + table, llaves)
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                 print sys.exc_info()[1]
                 dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nExisten datos relacionados con:\n<b>%s</b>"%codigo)
        
    def on_btnPropiedades_clicked(self, btn=None):
        model, it = self.treeRegistroEstadoFenologico.get_selection().get_selected()
        if model is None or it is None:
            return
        dlg = dlgRegistroEstadoFenologico(self.cnx, self.frm_padre, False)
        
        dlg.codigo_registro_estado_fenologico = model.get_value(it, CODIGO_REGISTRO_ESTADO_FENOLOGICO)
           
        dlg.entCultivo.set_text(model.get_value(it, DESCRIPCION_CULTIVO))
        dlg.codigo_cultivo = model.get_value(it, CODIGO_CULTIVO)
        dlg.pecCultivo.set_selected(True)
        
        dlg.entCuartel.set_text(model.get_value(it, DESCRIPCION_CUARTEL))
        dlg.codigo_cuartel = model.get_value(it, CODIGO_CUARTEL)
        dlg.pecCuartel.set_selected(True)
        
        dlg.entEstadoFenologico.set_text(model.get_value(it, DESCRIPCION_ESTADO_FENOLOGICO))
        dlg.codigo_estado_fenologico = model.get_value(it, CODIGO_ESTADO_FENOLOGICO)
        dlg.pecEstadoFenologico.set_selected(True)
        
        dlg.entTemporada.set_text(model.get_value(it, DESCRIPCION_TEMPORADA))
        dlg.codigo_temporada = model.get_value(it, CODIGO_TEMPORADA)
        dlg.pecTemporada.set_selected(True)
        
        dlg.entFecha.set_date(comunes.GetDateFromModel(model.get_value(it, FECHA).split()[0]))
        
        dlg.editando = (True)
        response = dlg.dlgRegistroEstadoFenologico.run()
        if response == gtk.RESPONSE_OK:
            self.modelo.clear()
            self.carga_datos()
            
    def on_btnCerrar_clicked(self, btn=None):
        if self.padre is None:
            self.on_exit()
        else:
            self.padre.remove_tab("Registro de Estado Fenologico")
            
    def on_treeRegistroEstadoFenologico_row_activated(self, tree=None, path=None, col=None):
        self.on_btnPropiedades_clicked()


class dlgRegistroEstadoFenologico(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        GladeConnect.__init__(self, "glade/wnRegistroEstadoFenologico.glade", "dlgRegistroEstadoFenologico")
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
        self.pecEstadoFenologico = completion.CompletionEstadoFenologico(self.entEstadoFenologico,
                self.sel_estado_fenologico,
                self.cnx)
        
        self.dlgRegistroEstadoFenologico.show_all()
    
    def sel_cultivo(self, completion, model, iter):
        self.codigo_cultivo = model.get_value(iter, 1)
        
    def sel_cuartel(self, completion, model, iter):
        self.codigo_cuartel = model.get_value(iter, 1)
    
    def sel_temporada(self, completion, model, iter):
        self.codigo_temporada = model.get_value(iter, 1)
    
    def sel_estado_fenologico(self, completion, model, iter):
        self.codigo_estado_fenologico = model.get_value(iter, 1)
        
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        
        fecha = self.entFecha.get_date()
        
        if self.entCultivo.get_text() == "":
            dialogos.error("El cultivo no puede ser vacio.")
            return
        
        if self.entCuartel.get_text() == "":
            dialogos.error("El cuartel no puede ser vacio.")
            return
        
        if self.entTemporada.get_text() == "":
            dialogos.error("La temporada no puede ser vacia.")
            return
        
        if self.entEstadoFenologico.get_text() == "":
            dialogos.error("El estado fenologico no puede ser vacio.")
            return
        
        campos = {}
        llaves = {}
        campos['codigo_cultivo'] = self.codigo_cultivo
        campos['codigo_cuartel'] = self.codigo_cuartel
        campos['fecha'] = fecha.strftime("%Y/%m/%d")
        campos['codigo_temporada'] = self.codigo_temporada
        campos['codigo_estado_fenologico'] = self.codigo_estado_fenologico
        
        if not self.editando:
            sql = ifd.insertFromDict(schema + "." + table, campos)        
        else:
            llaves['codigo_registro_estado_fenologico'] = self.codigo_registro_estado_fenologico
            sql, campos=ifd.updateFromDict(schema + "." + table, campos, llaves)
        
        try:   
            self.cursor.execute(sql, campos)
            self.dlgRegistroEstadoFenologico.hide()
        except:
            print sys.exc_info()[1]
            print sql
            
        
    def on_btnCancelar_clicked(self, btn=None):
        self.dlgRegistroEstadoFenologico.hide()
        
if __name__ == '__main__':
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    sys.excepthook = debugwindow.show
    d = wnRegistroEstadoFenologico(cnx)
    
    gtk.main()