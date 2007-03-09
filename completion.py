#!/usr/bin/env python
# -*- coding: utf-8 -*-
# completion -- Objectos de autocompletado del sistema

from PixEntryCompletion import PixEntryCompletion
import gtk
from codificacion import CUTF8
from constantes import MESES
from constantes import SUCURSAL_MATRIZ
import ifd
import config
#from psycopg import connect

schema = config.schema

def titulo_campos(campos):
    return [i.replace("_"," ").title() for i in campos]


class GenericCompletion(PixEntryCompletion):

    def __init__(self, entry = gtk.Entry(), sel_func = None,
                    cnx = None, sql = None, modelo=None):

        PixEntryCompletion.__init__(self, entry, selfunc = sel_func,
                                        match_all = False)

        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.sql = sql
        if modelo is None:
            self.carga_modelo()
        else:
            self.set_model(modelo)
            self.set_select_column(0)

    def carga_modelo(self):
        self.cursor.execute(self.sql)
        r = self.cursor.fetchall()
        self.titulos = titulo_campos([i[0] for i in self.cursor.description])
        self.modelo.clear()
        if len(r) == 0:
            return
        l = map(ifd.type_to_str, r[0])
        self.modelo = gtk.ListStore(*map(type, l))
        for i in r:
            self.modelo.append(map(CUTF8,i))
        self.set_model(self.modelo)
        self.set_select_column(0)

    def reload(self):
        self.modelo.clear()
        self.cursor.execute(self.sql)
        r = self.cursor.fetchall()
        for i in r:
            self.modelo.append(map(CUTF8,i))

class CompletionCuartel(GenericCompletion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None, tabla=None):
        s = """SELECT c.descripcion_cuartel,
                        c.codigo_cuartel
                        FROM riego.cuartel c                            
                        ORDER BY c.descripcion_cuartel"""
        GenericCompletion.__init__(self, entry, sel_func = f, cnx = c, sql = s)
        
class CompletionTipoControl(GenericCompletion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None, tabla=None):
        s = """SELECT t.descripcion_tipo_control,
                      u.descripcion_unidad,
                      t.codigo_tipo_control,
                      u.codigo_unidad,
                      t.tipo_resultado
                      FROM """ + schema + """.tipo_control t
                      INNER JOIN """ + schema + """.unidad u
                      ON t.codigo_unidad = u.codigo_unidad
                      ORDER BY t.descripcion_tipo_control""" 
        GenericCompletion.__init__(self, entry, sel_func = f, cnx = c, sql = s)        
        
class CompletionCodigoDescripcion(GenericCompletion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None, tabla=None):
        s = """SELECT
                        descripcion_%s,
                        codigo_%s
                FROM
                        riego.%s
                ORDER BY
                        descripcion_%s""" % (4*(tabla,))
        GenericCompletion.__init__(self, entry, sel_func = f, cnx = c, sql = s)

class CompletionFicha(GenericCompletion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        s = """SELECT                       
                        descripcion_ficha,
                        rut
                FROM
                        """ + schema + """.ficha
                ORDER BY
                        descripcion_ficha"""
        GenericCompletion.__init__(self, entry, sel_func = f, cnx = c, sql = s)

class CompletionPropietario(CompletionFicha):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionFicha.__init__(self, entry, f, c, 1)
        
class CompletionProveedor(CompletionFicha):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionFicha.__init__(self, entry, f, c, 3)        

        
class CompletionEmpleado(CompletionFicha):
    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionFicha.__init__(self, entry, f, c, 4)  


class CompletionCliente(CompletionFicha):
    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionFicha.__init__(self, entry, f, c, 2)

class CompletionTransporte(CompletionFicha):
    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionFicha.__init__(self, entry, f, c, 5)
        
class CompletionTipoFicha(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='tipo_ficha')

class CompletionSector(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='sector')
    
class CompletionCultivo(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='cultivo') 

class CompletionEstadoFenologico(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='estado_fenologico') 

class CompletionTipoDocumento(GenericCompletion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None, e = None):
        s = """SELECT
                        descripcion_tipo_documento,
                        codigo_tipo_documento
                FROM
                        riego.tipo_documento
                ORDER BY
                        codigo_tipo_documento"""
        GenericCompletion.__init__(self, entry, sel_func = f, cnx = c, sql = s)
        
class CompletionRut(GenericCompletion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None, e = None):
        s = """SELECT rut, descripcion_ficha FROM riego.ficha ORDER BY codigo_tipo_ficha"""
        GenericCompletion.__init__(self, entry, sel_func = f, cnx = c, sql = s)

class CompletionInsumo(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='insumo')        
        
class CompletionTipoAplicacion(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='tipo_aplicacion')        

class CompletionVariedad(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='variedad')

class CompletionEstanque(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='estanque')
        
class CompletionUnidad(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='unidad')
        
class CompletionUnidadDosis(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='unidad_dosis')

class CompletionProducto(GenericCompletion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None, e = None):
        s = """SELECT descripcion_producto, 
                codigo_producto, 
                dosis_propuesta FROM riego.producto 
                ORDER BY codigo_producto"""
        GenericCompletion.__init__(self, entry, sel_func = f, cnx = c, sql = s)
        
class CompletionMaquinaria(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='maquinaria')

class CompletionImplemento(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='implemento')
        
class CompletionHilera(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='hilera')

class CompletionLabor(CompletionCodigoDescripcion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None):
        CompletionCodigoDescripcion.__init__(self, entry, f, c, tabla='labor')

class CompletionTemporada(GenericCompletion):

    def __init__(self, entry = gtk.Entry(), f = None, c = None, e = None):
        s = """SELECT 'Temporada ' || date_part('year', fecha_inicio) || '-' 
                    || date_part('year', fecha_termino) as descripcion_temporada,
                    codigo_temporada 
         FROM riego.temporada ORDER BY codigo_temporada"""
        GenericCompletion.__init__(self, entry, sel_func = f, cnx = c, sql = s)

if __name__ == "__main__":
    w = gtk.Window()
    e = gtk.Entry()
    
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    p = CompletionTipoFicha(e, None, cnx, 1)    
    w.add(e)
    w.show_all()
     
    gtk.main()
    

