#!/usr/bin/env python
# -*- coding: UTF8 	-*-

from GladeConnect import GladeConnect
import gtk
import dialogos
import SimpleTree
import ifd
import completion
import comunes
import treetohtml
import config

#Datos a colocar en padre
#padre.ventana
#padre.treeVentana
#padre.columnas
#padre.strSelect
#padre.mensaje
#padre.llave

class wnVentana(GladeConnect):
    
    def __init__(self, conexion=None, padre=None, root="wnVentana"):
        if padre is None:
            self.wnVentana.maximize()
        else:
            global ventana
            ventana = padre.ventana
        
        GladeConnect.__init__(self, "glade/wn%s.glade" % ventana, root)
        self.frm_padre = getattr(self, "wn" + ventana)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        self.padre = padre
        self.treeVentana = getattr(self, "tree" + ventana)
        self.strSelect = padre.strSelect
        self.descripcion = padre.descripcion
        self.mensaje = padre.mensaje
        self.llave = padre.llave
        
        self.cols = padre.columnas
        self.crea_columnas()
        self.carga_datos()
        
        gtk.main()
    
    def crea_columnas(self):
        columnas = []
                
        for col, desc, tipo in self.cols:
            columnas.append ([col, desc, tipo])
        
        self.modelo = gtk.ListStore(int, str)
        SimpleTree.GenColsByModel(self.modelo, columnas, self.treeVentana)
        self.col_data = [x[0] for x in columnas]
        
    def carga_datos(self):
        self.modelo = ifd.ListStoreFromSQL(self.cnx, self.strSelect)
        self.treeVentana.set_model(self.modelo)
        
    def on_btnAnadir_clicked(self, btn=None, data=None):
        dlg = dlgDialogo(self.cnx, self, False)
        dlg.editando=False
        response = getattr(dlg, "dlg" + ventana).run()
        if response == gtk.RESPONSE_OK:
            self.carga_datos()
    
    def on_btnQuitar_clicked(self, btn=None):
        
        model, it = self.treeVentana.get_selection().get_selected()
        if model is None or it is None:
            return
        #hacerlo dinamico (lo siguiente)
        descripcion = model.get_value(it, self.cols[1][0])
        
        if dialogos.yesno("""¿Desea eliminar %s <b>%s</b>?\n
                    Esta acción no se puede deshacer\n
                    """ % (self.mensaje, descripcion), self.frm_padre) == gtk.RESPONSE_YES:
            llaves={'%s' % self.llave:descripcion}
            sql = ifd.deleteFromDict(schema + "." + table, llaves)
            try:
                self.cursor.execute(sql, llaves)
                model.remove(it)
            except:
                print sys.exc_info()[1]
                dialogos.error("""<b>NO SE PUEDE ELIMINAR</b>\n%s <b>%s</b>, 
                esta relacionada con un producto"""% (mensaje, descripcion))
            

class dlgDialogo(GladeConnect):
    def __init__(self, conexion=None, padre=None, editando=None):
        print ventana
        GladeConnect.__init__(self, "glade/wn%s.glade" % ventana, "dlg%s" % ventana)
        self.cnx = conexion
        self.cursor = self.cnx.cursor()
        
        #self.entDescripcion.grab_focus()
        
        self.editando=editando
        #self.codigo_tipo_ficha = None
        if self.editando:
            print "editando"
            #self.entCodigo.set_sensitive(False)
        #self.dlgDialogo.show()
        getattr(self, "dlg" + ventana).show()
        
if __name__ == '__main__':
    exit
            