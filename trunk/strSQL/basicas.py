#!/usr/bin/env python
# -*- coding: UTF8 	-*-
import config

strSelectEstanque = """SELECT * FROM """ + config.schema + """.estanque ORDER BY codigo_estanque"""

strSelectTipoFicha = """SELECT * FROM """ + config.schema + """.tipo_ficha ORDER BY codigo_tipo_ficha"""

strSelectInsumo = """SELECT * FROM """ + config.schema + """.insumo ORDER BY codigo_insumo"""

strSelectTipoAplicacion = """SELECT * FROM """ + config.schema + """.tipo_aplicacion ORDER BY codigo_tipo_aplicacion"""

#strSelectTipoControl = """SELECT * FROM """ + config.schema + """.tipo_control ORDER BY codigo_tipo_control"""
strSelectTipoControl = """ SELECT
                            s.codigo_tipo_control,
                            s.descripcion_tipo_control,
                            s.tipo_resultado,
                            s.codigo_unidad,
                            v.descripcion_unidad
                        FROM """ + config.schema + """.tipo_control s
                        INNER JOIN """ + config.schema + """.unidad v
                        ON s.codigo_unidad = v.codigo_unidad
                        ORDER BY s.descripcion_tipo_control"""

strSelectFicha = """SELECT
                            f.codigo_tipo_ficha,
                            t.descripcion_tipo_ficha,
                            f.descripcion_ficha,
                            f.rut
                        FROM """ + config.schema + """.ficha f
                        INNER JOIN """ + config.schema + """.tipo_ficha t
                        ON f.codigo_tipo_ficha = t.codigo_tipo_ficha
                        ORDER BY f.descripcion_ficha"""
                        
strSelectSector = """SELECT
                            f.codigo_cultivo,
                            t.descripcion_cultivo,
                            f.descripcion_sector,
                            f.codigo_sector
                        FROM """ + config.schema + """.sector f
                        INNER JOIN """ + config.schema + """.cultivo t
                        ON f.codigo_cultivo = t.codigo_cultivo
                        ORDER BY f.descripcion_sector"""
                        
strSelectCuartel = """SELECT
                            f.codigo_sector,
                            t.descripcion_sector,
                            f.descripcion_cuartel,
                            f.codigo_cuartel
                        FROM """ + config.schema + """.cuartel f
                        INNER JOIN """ + config.schema + """.sector t
                        ON f.codigo_sector = t.codigo_sector
                        ORDER BY f.descripcion_cuartel"""
                        
strSelectProducto = """SELECT
                            f.codigo_producto,
                            f.descripcion_producto,
                            f.codigo_unidad,
                            t.descripcion_unidad,                            
                            f.dosis_propuesta
                        FROM """ + config.schema + """.producto f
                        INNER JOIN """ + config.schema + """.unidad t
                        ON f.codigo_unidad = t.codigo_unidad
                        ORDER BY f.descripcion_producto"""
                        
strSelectHilera = """SELECT
                            f.codigo_hilera,
                            f.descripcion_hilera,
                            f.codigo_cuartel,
                            f.codigo_variedad,
                            t.descripcion_cuartel,
                            v.descripcion_variedad,                            
                            f.superficie 
                        FROM """ + config.schema + """.hilera f 
                        INNER JOIN """ + config.schema + """.cuartel t 
                        ON f.codigo_cuartel = t.codigo_cuartel 
                        INNER JOIN """ + config.schema + """.variedad v 
                        ON f.codigo_variedad = v.codigo_variedad  
                        ORDER BY f.descripcion_hilera"""
                    
strSelectCosecha = """SELECT c.*,
                            f.descripcion_ficha,
                            s.descripcion_cuartel,
                            v.descripcion_variedad
                        FROM """ + config.schema + """.cosecha c
                        INNER JOIN """ + config.schema + """.ficha f
                        ON c.rut_ficha = f.rut_ficha
                        INNER JOIN """ + config.schema + """.cuartel s
                        ON c.codigo_cuartel = s.codigo_cuartel
                        INNER JOIN """ + config.schema + """.variedad v
                        ON c.codigo_variedad = v.codigo_variedad
                        ORDER BY c.codigo_cosecha"""
                        
strSelectLabor = """SELECT * FROM """ + config.schema + """.labor ORDER BY codigo_labor"""

strSelectMaquinaria = """SELECT * FROM """ + config.schema + """.maquinaria ORDER BY codigo_maquinaria"""

strSelectVariedad = """SELECT * FROM """ + config.schema + """.variedad ORDER BY codigo_variedad"""

strSelectCultivo = """SELECT * FROM """ + config.schema + """.cultivo ORDER BY codigo_cultivo"""

strSelectDetalleRelacion = """SELECT %s FROM %s WHERE %s = %s"""

strSelectUnidad = """SELECT * FROM """ + config.schema + """.unidad ORDER BY descripcion_unidad"""

#strSelectProducto = """SELECT * FROM """ + config.schema + """.producto ORDER BY descripcion_producto"""

strSelectTipoDocumento = """SELECT * FROM """ + config.schema + """.tipo_documento ORDER BY codigo_tipo_documento"""

strNextValCodigo = """SELECT nextval('""" + config.schema + """.%s_codigo_%s_seq'::regclass)"""

strSelectDespacho = """SELECT
                        d.codigo_despacho,
                        d.codigo_tipo_documento,
                        t.descripcion_tipo_documento,
                        d.numero_documento,
                        d.fecha_despacho,
                        d.hora_despacho,
                        d.rut_cliente,
                        c.descripcion_ficha,
                        d.rut_transportista,
                        cc.descripcion_ficha,
                        d.destino,
                        d.observaciones,
                        d.sello_seguridad
                        FROM """ + config.schema + """.despacho d
                        INNER JOIN """ + config.schema + """.ficha c
                        ON d.rut_cliente = c.rut_ficha
                        join """ + config.schema + """.ficha cc
                        on d.rut_transportista = cc.rut_ficha
                        INNER JOIN """ + config.schema + """.tipo_documento t
                        ON d.codigo_tipo_documento = t.codigo_tipo_documento
                        ORDER BY d.codigo_despacho"""
                        
                        
strSelectTipoDespacho = """SELECT d.%s,
                                m.%s,
                                d.cantidad
                                FROM %s d
                                JOIN %s e
                                ON e.%s = d.%s
                                JOIN %s m
                                on d.%s = m.%s
                                where %s = %s"""
                                
                                

strSelectMovimientoEstanque = """select fecha, porcentaje, volumen, movimiento, desce_a, desce_b
                            from """ + config.schema + """.vw_movimiento_estanque_fecha order by fecha"""