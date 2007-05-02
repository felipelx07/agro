#!/usr/bin/env python
# -*- coding: UTF8 	-*-

from GladeConnect import GladeConnect
import gtk
import sys
import dialogos
import debugwindow
import SimpleTree
import ifd
from strSQL.basicas import strSelectHilera
from psycopg import connect
import completion
import comunes
import treetohtml
import config

(CODIGO_HILERA,
 DESCRIPCION,
 CODIGO_CUARTEL,
 CODIGO_VARIEDAD,
 DESCRIPCION_CUARTEL,
 DESCRIPCION_VARIEDAD,
 SUPERFICIE) = range(7)

schema = config.schema
table = "hilera"

class wnHilera (GladeConnect):
    def __init__(self, conexion=None, padre=None, root="wnHilera"):
        GladeConnect.__init__(self, "glade/wnHilera.glade", root)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        if padre is None :
            self.wnHilera.maximize()
            self.frm_padre = self.wnHilera
        else:
            self.frm_padre = padre.frm_padre
            
        self.crea_columnas()
        self.carga_datos()

    def crea_columnas(self):
        columnas = []
        columnas.append ([CODIGO_HILERA, "Hilera", "str"])
        columnas.append ([DESCRIPCION, "Descripcion", "str"])
        columnas.append ([DESCRIPCION_CUARTEL, "Cuartel","str"])
        columnas.append ([DESCRIPCION_VARIEDAD, "Variedad","str"])
        columnas.append ([SUPERFICIE, "Superficie","str"])
        
        self.modelo = gtk.ListStore(*(5*[str]))
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeHilera)
        self.col_data = [x[0] for x in columnas]
        
    def on_btnImprimir_clicked(self, btn=None):
        t = treetohtml.TreeToHTML(self.treeHilera,"Hilera", self.col_data)
        t.show()        
    def carga_datos(self):
        
        self.modelo = ifd.ListStoreFromSQL(self.cnx, strSelectHilera)
        self.treeHilera.set_model(self.modelo)

    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgHilera(self.cnx, self.frm_padre, False)
        dlg.editando=False
        response = dlg.dlgHilera.run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        
        selection = self.treeHilera.get_selection()
        model, it = selection.get_selected()
        if model is None or it is None:
            return
        
        codigo_hilera = model.get_value(it, CODIGO_HILERA)
        descripcion = model.get_value(it, DESCRIPCION)
        
        if dialogos.yesno("¿Desea eliminar la Hilera <b>%s</b>?\nEsta acción no se puede deshacer\n" % descripcion, self.frm_padre) == gtk.RESPONSE_YES:
            llaves = {'codigo_hilera':codigo_hilera}
            sql = ifd.deleteFromDict(config.schema + '.' + table, llaves)
            try:
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                 print sys.exc_info()[1]
                 dialogos.error("<b>NO SE PUEDE ELIMINAR</b>\nExisten datos relacionados con:\n<b>%s</b>"%descripcion)
        
    def on_btnPropiedades_clicked(self, btn=None):
        model, it = self.treeHilera.get_selection().get_selected()
        if model is None or it is None:
            dialogos.error("Seleccione una Hilera para editar.")
            return
        dlg = dlgHilera(self.cnx, self.frm_padre, False)
        dlg.entVariedad.set_text(model.get_value(it, DESCRIPCION_VARIEDAD))
        dlg.codigo_variedad = model.get_value(it, CODIGO_VARIEDAD)
        dlg.pecVariedad.set_selected(True)
        dlg.entCuartel.set_text(model.get_value(it, DESCRIPCION_CUARTEL))
        dlg.codigo_cuartel = model.get_value(it, CODIGO_CUARTEL)
        dlg.pecCuartel.set_selected(True)
        dlg.entDescripcion.set_text(model.get_value(it, DESCRIPCION))
        dlg.entCodigo.set_text(model.get_value(it, CODIGO_HILERA))
        dlg.entSuperficie.set_text(model.get_value(it, SUPERFICIE))
        dlg.editando = (True)
        response = dlg.dlgHilera.run()
        if response == gtk.RESPONSE_OK:
            self.modelo.clear()
            self.carga_datos()
            
    def on_btnCerrar_clicked(self, btn=None):
        if self.padre is None:
            self.on_exit()
        else:
            self.padre.remove_tab("Hilera")
            
    def on_treeHilera_row_activated(self, tree=None, path=None, col=None):
        self.on_btnPropiedades_clicked()


class dlgHilera(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        GladeConnect.__init__(self, "glade/wnHilera.glade", "dlgHilera")
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.editando=editando
        self.codigo_cuartel = None
        if self.editando:
            self.entCodigo.set_sensitive(False)
        
        self.pecCuartel = completion.CompletionCuartel(self.entCuartel,
                self.sel_cuartel,
                self.cnx)
        self.pecVariedad = completion.CompletionVariedad(self.entVariedad,
                self.sel_variedad,
                self.cnx)
        self.dlgHilera.show()

    def sel_cuartel(self, completion, model, iter):
        self.codigo_cuartel = model.get_value(iter, 1)
        
    def sel_variedad(self, completion, model, iter):
        self.codigo_variedad = model.get_value(iter, 1)
        
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        
        if self.entDescripcion.get_text() == "":
            dialogos.error("El campo <b>Descripción Hilera</b> no puede estar vacío")
            return
        
        if self.entSuperficie.get_text() == "":
            dialogos.error("")
        
        if self.codigo_cuartel is None:
            dialogos.error("Debe escoger una <b>Hilera</b>")
            return
        
        campos = {}
        llaves = {}
        campos['superficie']  = self.entSuperficie.get_text().upper()
        campos['descripcion_hilera']  = self.entDescripcion.get_text().upper()
        campos['codigo_cuartel'] = self.codigo_cuartel
        campos['codigo_variedad'] = self.codigo_variedad
        
        
        if not self.editando:
            sql = ifd.insertFromDict(schema + "." + table, campos)        
        else:
            llaves['codigo_hilera'] = self.entCodigo.get_text()
            sql, campos=ifd.updateFromDict(schema + "." + table, campos, llaves)
        
        try:   
            self.cursor.execute(sql, campos)
            self.dlgHilera.hide()
        except:
            print sys.exc_info()[1]
            print sql
            
        
    def on_btnCancelar_clicked(self, btn=None):
        self.dlgHilera.hide()
        
if __name__ == '__main__':
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    sys.excepthook = debugwindow.show
    d = wnHilera(cnx)
    
    gtk.main()