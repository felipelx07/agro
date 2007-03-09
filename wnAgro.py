#!/usr/bin/env python
# -*- coding: UTF8 	-*-

from GladeConnect import GladeConnect
import gtk
import sys
import dialogos
import debugwindow 
from psycopg import connect
from wnSector import wnSector
from wnFicha import wnFicha
from wnTipoFicha import wnTipoFicha
from wnCuartel import wnCuartel
from wnVariedad import wnVariedad
from wnUnidad import wnUnidad
from wnProducto import wnProducto
from wnLabor import wnLabor
from wnMaquinaria import wnMaquinaria
from wnHilera import wnHilera
from wnCultivo import wnCultivo
from wnAplicacion import wnAplicacion
from wnLaborHilera import wnLaborHilera
from wnUnidadDosis import wnUnidadDosis
from wnImplemento import wnImplemento
#from wnEstadoFenologico import wnEstadoFenologico
#from wnRegistroEstadoFenologico import wnRegistroEstadoFenologico
import config

class Agro(GladeConnect):
        
    def __init__(self):
        GladeConnect.__init__(self, "./glade/wnAgro.glade")
        self.abre_coneccion()
        self.cnx.autocommit()
        self.wnAgro.maximize()
        self.frm_padre = self.wnAgro
        self.wins = {}

    def abre_coneccion(self):
        try:
            f = open("coneccion.rc", 'r')
            l = f.readline()[:-1]
            self.cnx = connect(l)
            f.close()
            print "Conección por archivo"
        except:
            DB = config.DB
            user = config.user
            password = config.password
            host = config.host
    
            self.cnx = connect(DB + " " + user + " " + password + " " + host )
            print "Conección base"
    
    def add_tab(self, widget, label):
        p = -1
        if not self.wins.has_key(label):
            l = gtk.Label('')
            l.set_text_with_mnemonic(label)
            self.ntbAgro.append_page(widget, l)
            widget.show()
            self.wins[label] = (widget, len(self.wins))
        else:
            self.ntbAgro.show_all()
            self.ntbAgro.set_current_page(self.wins[label][1])
            a = self.ntbAgro.get_current_page()
        p = len(self.wins) - 1
        self.ntbAgro.set_current_page(-1)
            
    def remove_tab(self, label):
        self.ntbAgro.remove(self.wins[label][0])
        del self.wins[label]
    
    def on_mnuUnidad_activate(self, widget, *args):
        unidad = wnUnidad(self.cnx, self, "vboxUnidad")
        self.add_tab(unidad.vboxUnidad, "Unidad")
        return
    
    def on_mnuCosecha_activate(self, widget, *args):
        cosecha = wnCosecha(self.cnx, self, "vboxCosecha")
        self.add_tab(cosecha.vboxCosecha, "Cosecha")
        return

    def on_mnuVariedad_activate(self, widget, *args):
        variedad = wnVariedad(self.cnx, self, "vboxVariedad")
        self.add_tab(variedad.vboxVariedad, "Variedad")
        return
    
    def on_mnuSector_activate(self, widget, *args):
        sector = wnSector(self.cnx, self, "vboxSector")
        self.add_tab(sector.vboxSector, "Sector")
        return
    
    def on_mnuFicha_activate(self, widget, *args):
        ficha = wnFicha(self.cnx, self, "vboxFicha")
        self.add_tab(ficha.vboxFicha, "Ficha")
        return
    
    def on_mnuTipoFicha_activate(self, widget, *args):
        tipo_ficha = wnTipoFicha(self.cnx, self, "vboxTipoFicha")
        self.add_tab(tipo_ficha.vboxTipoFicha, "TipoFicha")
        return
    
    def on_mnuCuartel_activate(self, widget, *args):
        cuartel = wnCuartel(self.cnx, self, "vboxCuartel")
        self.add_tab(cuartel.vboxCuartel, "Cuartel")
        return
    
    def on_mnuProducto_activate(self, widget, *args):
        producto = wnProducto(self.cnx, self, "vboxProducto")
        self.add_tab(producto.vboxProducto, "Producto")
        return
    
    def on_mnuLabor_activate(self, widget, *args):
        labor = wnLabor(self.cnx, self, "vboxLabor")
        self.add_tab(labor.vboxLabor, "Labor")
        return
    
    def on_mnuMaquinaria_activate(self, widget, *args):
        maquinaria = wnMaquinaria(self.cnx, self, "vboxMaquinaria")
        self.add_tab(maquinaria.vboxMaquinaria, "Maquinaria")
        return
    
    def on_mnuHilera_activate(self, widget, *args):
        hilera = wnHilera(self.cnx, self, "vboxHilera")
        self.add_tab(hilera.vboxHilera, "Hilera")
        return
    
    def on_mnuCultivo_activate(self, widget, *args):
        cultivo = wnCultivo(self.cnx, self, "vboxCultivo")
        self.add_tab(cultivo.vboxCultivo, "Cultivo")
        return
    
    def on_mnuAplicacion_activate(self, widget, *args):
        aplicacion = wnAplicacion(self.cnx, self, "vboxAplicacion")
        self.add_tab(aplicacion.vboxAplicacion, "Aplicacion")
        return
    
    def on_mnuLaborHilera_activate(self, widget, *args):
        labor_hilera = wnLaborHilera(self.cnx, self, "vboxLaborHilera")
        self.add_tab(labor_hilera.vboxLaborHilera, "Labor Hilera")
        return
    
    def on_mnuUnidadDosis_activate(self, widget, *args):
        unidad_dosis = wnUnidadDosis(self.cnx, self, "vboxUnidadDosis")
        self.add_tab(unidad_dosis.vboxUnidadDosis, "Unidad de dosis")
        return
    
    def on_mnuImplemento_activate(self, widget, *args):
        implemento = wnImplemento(self.cnx, self, "vboxImplemento")
        self.add_tab(implemento.vboxImplemento, "Implementos")
        return
    
    def on_mnuEstadoFenologico_activate(self, widget, *args):
        estado_fenologico = wnEstadoFenologico(self.cnx, self, "vboxEstadoFenologico")
        self.add_tab(estado_fenologico.vboxLaborHilera, "Estado Fenologico")
        return
    
    def on_mnuRegistroEstadoFenologico_activate(self, widget, *args):
        registro_estado_fenologico = wnRegistroEstadoFenologico(self.cnx, self, "vboxRegistroEstadoFenologico")
        self.add_tab(registro_estado_fenologico.vboxLaborHilera, "Registro de Estado Fenologico")
        return
        
if __name__ == "__main__":
    t = Agro()
    sys.excepthook = debugwindow.show
    
    gtk.main()
    