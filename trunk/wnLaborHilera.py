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
 CODIGO_CUARTEL,
 DESCRIPCION_CUARTEL,
 CODIGO_LABOR,
 DESCRIPCION_LABOR,
 FECHA,
 RUT,
 DESCRIPCION_FICHA) = range(9)

(SELECCIONADO,
 D_HILERA,
 C_HILERA) = range(3)

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
        columnas.append ([DESCRIPCION_CUARTEL, "Cuartel","str"])
        columnas.append ([DESCRIPCION_HILERA, "Hilera","str"])
        columnas.append ([FECHA, "Fecha","dte"])
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
            dialogos.error("Seleccione una Labor Hilera para editar.") #TODO: HACERLO PARA TODOS!!!!
            return
        dlg = dlgLaborHilera(self.cnx, self.frm_padre, False)
        
        dlg.entLabor.set_text(model.get_value(it, DESCRIPCION_LABOR))
        dlg.codigo_labor = model.get_value(it, CODIGO_LABOR)
        dlg.pecLabor.set_selected(True)
        
        dlg.entCuartel.set_text(model.get_value(it, DESCRIPCION_CUARTEL))
        dlg.codigo_cuartel = model.get_value(it, CODIGO_CUARTEL)
        dlg.pecCuartel.set_selected(True)
        dlg.codigo_hilera = model.get_value(it, CODIGO_HILERA)
        dlg.sel_cuartel(None, self.modelo, None)
        
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
        
        self.pecCuartel = completion.CompletionCuartel(self.entCuartel,
                self.sel_cuartel,
                self.cnx)
        self.pecLabor = completion.CompletionLabor(self.entLabor,
                self.sel_labor,
                self.cnx)
        self.pecFicha = completion.CompletionFicha(self.entFicha,
                self.sel_ficha,
                self.cnx)
        
        self.modelo_hilera = None
        
        self.dlgLaborHilera.show_all()

    def sel_cuartel(self, completion, model, iter):
        if completion is not None:
            self.codigo_cuartel = model.get_value(iter, 1)
        
        strSelectHilera = """SELECT
                            f.descripcion_hilera,
                            f.codigo_hilera 
                            FROM """ + config.schema + """.hilera f WHERE """
        if completion is None:
            strSelectHilera = strSelectHilera + """f.codigo_hilera = """ + self.codigo_hilera +""" AND """
        
        strSelectHilera = strSelectHilera +""" f.codigo_cuartel = """ + self.codigo_cuartel + """ 
                            ORDER BY f.codigo_hilera"""
                        
        columnas = []
        columnas.append ([SELECCIONADO, "Sel", "bool"])
        columnas.append ([D_HILERA, "Hilera","str"])
        
        m = ifd.ListStoreFromSQL(self.cnx, strSelectHilera)
        self.modelo_hilera = gtk.ListStore(bool, str, str)
        for x in m:
            if completion is not None:
                self.modelo_hilera.append((False, x[0], x[1]))
            else:
                self.modelo_hilera.append((True, x[0], x[1]))
            
        SimpleTree.GenColsByModel(self.modelo_hilera, columnas, self.treeHilera)
        self.col_data = [x[0] for x in columnas]
        
        self.treeHilera.set_model(self.modelo_hilera)
        
    def sel_labor(self, completion, model, iter):
        self.codigo_labor = model.get_value(iter, 1)
    
    def sel_ficha(self, completion, model, iter):
        self.rut = model.get_value(iter, 1)
        
    def on_btnAceptar_clicked(self, btn=None, date=None, cnx=None):
        
        fecha = self.entFecha.get_date()
        hilera_true = None
        
        if self.modelo_hilera == None:
            dialogos.error("Seleccione un cuartel y una Hilera.")
            return
        
        if self.entFicha.get_text() == "":
            dialogos.error("La ficha no puede ser vacia.")
            return
        
        campos = {}
        llaves = {}
        campos['codigo_labor'] = self.codigo_labor
        campos['fecha'] = fecha.strftime("%Y/%m/%d")
        campos['rut']  = self.rut
        campos['codigo_cuartel'] = self.codigo_cuartel
        
        for i in self.modelo_hilera:
            if i[0] == True:
                hilera_true = 1
                campos['codigo_hilera'] = i[2]
                
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
                
        if hilera_true == None:
            dialogos.error("Seleccione una hilera.")
            return
        
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