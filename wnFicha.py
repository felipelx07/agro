#!/usr/bin/env python
# -*- coding: UTF8 	-*-

from GladeConnect import GladeConnect
import gtk
import sys
import dialogos
import debugwindow
import SimpleTree
import ifd
from strSQL.basicas import strSelectFicha
from psycopg import connect
import completion
import comunes
import treetohtml
import config

(CODIGO_TIPO_FICHA,
 DESCRIPCION_TIPO_FICHA,
 DESCRIPCION,
 RUT_FICHA) = range(4)

schema = config.schema
table = "ficha"

class wnFicha (GladeConnect):
    def __init__(self, conexion=None, padre=None, root="wnFicha"):
        GladeConnect.__init__(self, "glade/wnFicha.glade", root)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        if padre is None :
            self.wnFicha.maximize()
            self.frm_padre = self.wnFicha
        else:
            self.frm_padre = padre.frm_padre
            
        self.crea_columnas()
        self.carga_datos()

    def crea_columnas(self):
        columnas = []
        columnas.append ([RUT_FICHA, "R.U.T.", "str"])
        columnas.append ([DESCRIPCION, "Descripcion", "str"])
        columnas.append ([DESCRIPCION_TIPO_FICHA, "Tipo","str"])
        
        self.modelo = gtk.ListStore(*(3*[str]))
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeFicha)
        self.col_data = [x[0] for x in columnas]
        
    def on_btnImprimir_clicked(self, btn=None):
        t = treetohtml.TreeToHTML(self.treeFicha,"Ficha", self.col_data)
        t.show()        
    def carga_datos(self):
        self.modelo = ifd.ListStoreFromSQL(self.cnx, strSelectFicha)
        self.treeFicha.set_model(self.modelo)

    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgFicha(self.cnx, self.frm_padre, False)
        dlg.editando=False
        response = dlg.dlgFicha.run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        selection = self.treeFicha.get_selection()
        model, it = selection.get_selected()
        if model is None or it is None:
            return
        
        rut = model.get_value(it, RUT_FICHA)
        descripcion = model.get_value(it, DESCRIPCION)
        
        if dialogos.yesno("¿Desea eliminar la Ficha <b>%s</b>?\nEsta acción no se puede deshacer\n" % descripcion, self.frm_padre) == gtk.RESPONSE_YES:
            try:
                llaves = {'rut':rut}
                sql = ifd.deleteFromDict(config.schema + '.ficha', llaves)
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                 print sys.exc_info()[1]
                 dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nExisten datos relacionados con:\n<b>%s</b>"%descripcion)
        
    def on_btnPropiedades_clicked(self, btn=None):
        model, it = self.treeFicha.get_selection().get_selected()
        if model is None or it is None:
            dialogos.error("Seleccione una Ficha para editar.")
            return
        dlg = dlgFicha(self.cnx, self.frm_padre, False)
        dlg.entTipoFicha.set_text(model.get_value(it, DESCRIPCION_TIPO_FICHA))
        dlg.codigo_tipo_ficha = model.get_value(it, CODIGO_TIPO_FICHA)
        dlg.pecTipoFicha.set_selected(True)
        dlg.entDescripcion.set_text(model.get_value(it, DESCRIPCION))
        dlg.entRUT.set_text(model.get_value(it, RUT_FICHA))
        dlg.editando = (True)
        response = dlg.dlgFicha.run()
        if response == gtk.RESPONSE_OK:
            self.modelo.clear()
            self.carga_datos()
            
    def on_btnCerrar_clicked(self, btn=None):
        if self.padre is None:
            self.on_exit()
        else:
            self.padre.remove_tab("Ficha")
            
    def on_treeFicha_row_activated(self, tree=None, path=None, col=None):
        self.on_btnPropiedades_clicked()


class dlgFicha(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        GladeConnect.__init__(self, "glade/wnFicha.glade", "dlgFicha")
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.entRUT.grab_focus()        
        self.entRUT.show()
        self.editando=editando
        self.codigo_tipo_ficha = None
        if self.editando:
            self.entRUT.set_sensitive(False)
        
        self.pecTipoFicha = completion.CompletionTipoFicha(self.entTipoFicha,
                self.sel_tipo_ficha,
                self.cnx)
        self.dlgFicha.show()

    def sel_tipo_ficha(self, completion, model, iter):
        self.codigo_tipo_ficha = model.get_value(iter, 1)
        
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        if self.entRUT.get_text() =="  .   .   - ":
            dialogos.error("El campo <b>Rut ficha</b> no puede estar vacío")
            return
        if not comunes.es_rut(self.entRUT.get_text()):
            dialogos.error("<b>El R.U.T. no corresponde</b>")
            return
        if self.entDescripcion.get_text() == "":
            dialogos.error("El campo <b>Descripción Ficha</b> no puede estar vacío")
            return
        
        if self.codigo_tipo_ficha is None:
            dialogos.error("Debe escoger un <b>Tipo Ficha</b>")
            return
        
        campos = {}
        llaves = {}
        campos['descripcion_ficha']  = self.entDescripcion.get_text().upper()
        campos['codigo_tipo_ficha'] = self.codigo_tipo_ficha
        if not self.editando:
            campos['rut']  = self.entRUT.get_text().upper()
            sql = ifd.insertFromDict(schema + "." + table, campos)
            
        else:
            llaves['rut'] = self.entRUT.get_text().upper()
            sql, campos=ifd.updateFromDict(schema + "." + table, campos, llaves)
        try:   
            self.cursor.execute(sql, campos)
            self.dlgFicha.hide()
        except:
            print sys.exc_info()[1]
            rut = self.entRUT
            dialogos.error("En la Base de Datos ya existe el RUT %s"%campos['rut'])
            self.entRUT.grab_focus()
            
        
    def on_btnCancelar_clicked(self, btn=None):
        self.dlgFicha.hide()
        
if __name__ == '__main__':
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    sys.excepthook = debugwindow.show
    d = wnFicha(cnx)
    
    gtk.main()