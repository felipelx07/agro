#!/usr/bin/env python
# -*- coding: UTF8 	-*-

from GladeConnect import GladeConnect
import gtk
import sys
import dialogos
import debugwindow
import SimpleTree
import ifd
from strSQL.basicas import strSelectCuartel
from psycopg import connect
import completion
import comunes
import treetohtml
import config

(CODIGO_SECTOR,
 DESCRIPCION_SECTOR,
 DESCRIPCION,
 CODIGO_CUARTEL) = range(4)

schema = config.schema
table = "cuartel"

class wnCuartel (GladeConnect):
    def __init__(self, conexion=None, padre=None, root="wnCuartel"):
        GladeConnect.__init__(self, "glade/wnCuartel.glade", root)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        if padre is None :
            self.wnCuartel.maximize()
            self.frm_padre = self.wnCuartel
        else:
            self.frm_padre = padre.frm_padre
            
        self.crea_columnas()
        self.carga_datos()

    def crea_columnas(self):
        columnas = []
        columnas.append ([CODIGO_CUARTEL, "Cuartel", "str"])
        columnas.append ([DESCRIPCION, "Descripcion", "str"])
        columnas.append ([DESCRIPCION_SECTOR, "Sector","str"])
        
        self.modelo = gtk.ListStore(*(3*[str]))
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeCuartel)
        self.col_data = [x[0] for x in columnas]
        
    def on_btnImprimir_clicked(self, btn=None):
        t = treetohtml.TreeToHTML(self.treeCuartel,"Cuartel", self.col_data)
        t.show()        
    def carga_datos(self):
        self.modelo = ifd.ListStoreFromSQL(self.cnx, strSelectCuartel)
        self.treeCuartel.set_model(self.modelo)

    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgCuartel(self.cnx, self.frm_padre, False)
        dlg.editando=False
        response = dlg.dlgCuartel.run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        
        selection = self.treeCuartel.get_selection()
        model, it = selection.get_selected()
        if model is None or it is None:
            return
        
        codigo_cuartel = model.get_value(it, CODIGO_CUARTEL)
        descripcion = model.get_value(it, DESCRIPCION)
        
        if dialogos.yesno("¿Desea eliminar el Cuartel <b>%s</b>?\nEsta acción no se puede deshacer\n" % descripcion, self.frm_padre) == gtk.RESPONSE_YES:
            try:
                llaves = {'codigo_cuartel':codigo_cuartel}
                sql = ifd.deleteFromDict(config.schema + '.' + table, llaves)
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                 print sys.exc_info()[1]
                 dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nExisten datos relacionados con:\n<b>%s</b>"%descripcion)
        
    def on_btnPropiedades_clicked(self, btn=None):
        model, it = self.treeCuartel.get_selection().get_selected()
        if model is None or it is None:
            dialogos.error("Seleccione un Cuartel para editar.")
            return
        dlg = dlgCuartel(self.cnx, self.frm_padre, False)
        dlg.entSector.set_text(model.get_value(it, DESCRIPCION_SECTOR))
        dlg.codigo_sector = model.get_value(it, CODIGO_SECTOR)
        dlg.pecSector.set_selected(True)
        dlg.entDescripcion.set_text(model.get_value(it, DESCRIPCION))
        dlg.entCodigo.set_text(model.get_value(it, CODIGO_CUARTEL))
        dlg.editando = (True)
        response = dlg.dlgCuartel.run()
        if response == gtk.RESPONSE_OK:
            self.modelo.clear()
            self.carga_datos()
            
    def on_btnCerrar_clicked(self, btn=None):
        if self.padre is None:
            self.on_exit()
        else:
            self.padre.remove_tab("Cuartel")
            
    def on_treeCuartel_row_activated(self, tree=None, path=None, col=None):
        self.on_btnPropiedades_clicked()


class dlgCuartel(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        GladeConnect.__init__(self, "glade/wnCuartel.glade", "dlgCuartel")
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.editando=editando
        self.codigo_sector = None
        if self.editando:
            self.entCodigo.set_sensitive(False)
        
        self.pecSector = completion.CompletionSector(self.entSector,
                self.sel_sector,
                self.cnx)
        self.dlgCuartel.show()

    def sel_sector(self, completion, model, iter):
        self.codigo_sector = model.get_value(iter, 1)
        
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        
        if self.entDescripcion.get_text() == "":
            dialogos.error("El campo <b>Descripción Cuartel</b> no puede estar vacío")
            return
        
        if self.codigo_sector is None:
            dialogos.error("Debe escoger un <b>Cuartel</b>")
            return
        
        campos = {}
        llaves = {}
        campos['descripcion_cuartel']  = self.entDescripcion.get_text().upper()
        campos['codigo_sector'] = self.codigo_sector
        
        if not self.editando:
            sql = ifd.insertFromDict(schema + "." + table, campos)        
        else:
            llaves['codigo_cuartel'] = self.entCodigo.get_text()
            sql, campos=ifd.updateFromDict(schema + "." + table, campos, llaves)
        
        try:   
            self.cursor.execute(sql, campos)
            self.dlgCuartel.hide()
        except:
            print sys.exc_info()[1]
            print sql
            
        
    def on_btnCancelar_clicked(self, btn=None):
        self.dlgCuartel.hide()

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
    d = wnCuartel(cnx)
    
    gtk.main()
