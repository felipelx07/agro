#!/usr/bin/env python
# -*- coding: UTF8 	-*-
import config

strSelectTipoFicha = """SELECT * FROM """ + config.schema + """.tipo_ficha 
                        ORDER BY codigo_tipo_ficha"""

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
                        
strSelectSector = """SELECT *
                        FROM """ + config.schema + """.sector
                        ORDER BY descripcion_sector"""
                        
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
                            f.dosis_propuesta,
                            f.codigo_unidad_dosis,
                            d.descripcion_unidad_dosis
                        FROM """ + config.schema + """.producto f
                        INNER JOIN """ + config.schema + """.unidad t
                        ON f.codigo_unidad = t.codigo_unidad  
                        INNER JOIN """ + config.schema + """.unidad_dosis d
                        ON f.codigo_unidad_dosis = d.codigo_unidad_dosis
                        ORDER BY f.descripcion_producto"""
                       
strSelectAplicacion = """SELECT
                            a.codigo_aplicacion,
                            a.codigo_hilera,
                            a.codigo_producto,
                            h.descripcion_hilera,
                            p.descripcion_producto,                            
                            a.dosis,
                            a.fecha,
                            a.rut,
                            f.descripcion_ficha,
                            a.codigo_maquinaria,
                            a.codigo_implemento,
                            m.descripcion_maquinaria,
                            i.descripcion_implemento,
                            a.codigo_temporada,
                            'Temporada ' || date_part('year', t.fecha_inicio) 
                            || '-' || date_part('year', t.fecha_termino) 
                            as descripcion
                        FROM """ + config.schema + """.aplicacion a
                        INNER JOIN """ + config.schema + """.hilera h
                        ON a.codigo_hilera = h.codigo_hilera  
                        INNER JOIN """ + config.schema + """.producto p
                        ON a.codigo_producto = p.codigo_producto 
                        INNER JOIN """ + config.schema + """.ficha f
                        ON a.rut = f.rut 
                        INNER JOIN """ + config.schema + """.maquinaria m
                        ON a.codigo_maquinaria = m.codigo_maquinaria 
                        INNER JOIN """ + config.schema + """.implemento i
                        ON a.codigo_implemento = i.codigo_implemento 
                        INNER JOIN """ + config.schema + """.temporada t
                        ON a.codigo_temporada = t.codigo_temporada
                        ORDER BY a.codigo_aplicacion"""
                        
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
                        
strSelectLaborHilera = """SELECT
                            lh.codigo_hilera,
                            h.descripcion_hilera,
                            lh.codigo_labor,
                            l.descripcion_labor,
                            lh.fecha,
                            lh.rut,
                            f.descripcion_ficha 
                        FROM """ + config.schema + """.labor_hilera lh 
                        INNER JOIN """ + config.schema + """.hilera h 
                        ON lh.codigo_hilera = h.codigo_hilera 
                        INNER JOIN """ + config.schema + """.labor l 
                        ON lh.codigo_labor = l.codigo_labor 
                        INNER JOIN """ + config.schema + """.ficha f 
                        ON lh.rut = f.rut 
                        ORDER BY h.descripcion_hilera"""
                        
strSelectRegistroEstadoFenologico = """SELECT
                            r.codigo_registro_estado_fenologico,
                            r.codigo_cultivo,
                            c.descripcion_cultivo,
                            r.codigo_cuartel,
                            cl.descripcion_cuartel,
                            r.codigo_estado_fenologico,
                            e.descripcion_estado_fenologico,
                            r.codigo_temporada,
                            'Temporada ' || date_part('year', t.fecha_inicio) 
                            || '-' || date_part('year', t.fecha_termino) 
                            as descripcion_temporada,
                            r.fecha  
                        FROM """ + config.schema + """.registro_estado_fenologico r 
                        INNER JOIN """ + config.schema + """.cultivo c 
                        ON r.codigo_cultivo = c.codigo_cultivo 
                        INNER JOIN """ + config.schema + """.cuartel cl 
                        ON r.codigo_cuartel = cl.codigo_cuartel  
                        INNER JOIN """ + config.schema + """.estado_fenologico e 
                        ON r.codigo_estado_fenologico = e.codigo_estado_fenologico 
                        INNER JOIN """ + config.schema + """.temporada t 
                        ON r.codigo_temporada = t.codigo_temporada 
                        ORDER BY r.codigo_registro_estado_fenologico"""
                    
strSelectCultivoTemporada = """SELECT
                            ct.codigo_cultivo,
                            c.descripcion_cultivo,
                            ct.codigo_cuartel,
                            cl.descripcion_cuartel,                            
                            ct.codigo_temporada,
                            'Temporada ' || date_part('year', t.fecha_inicio) 
                            || '-' || date_part('year', t.fecha_termino) 
                            as descripcion_temporada 
                        FROM """ + config.schema + """.cultivo_temporada ct  
                        INNER JOIN """ + config.schema + """.cultivo c 
                        ON ct.codigo_cultivo = c.codigo_cultivo 
                        INNER JOIN """ + config.schema + """.cuartel cl 
                        ON ct.codigo_cuartel = cl.codigo_cuartel  
                        INNER JOIN """ + config.schema + """.temporada t 
                        ON ct.codigo_temporada = t.codigo_temporada 
                        ORDER BY ct.codigo_temporada"""

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

strSelectImplemento = """SELECT * FROM """ + config.schema + """.implemento ORDER BY codigo_implemento"""

strSelectVariedad = """SELECT * FROM """ + config.schema + """.variedad ORDER BY codigo_variedad"""

strSelectCultivo = """SELECT * FROM """ + config.schema + """.cultivo ORDER BY codigo_cultivo"""

strSelectDetalleRelacion = """SELECT %s FROM %s WHERE %s = %s"""

strSelectUnidad = """SELECT * FROM """ + config.schema + """.unidad ORDER BY descripcion_unidad"""

strSelectUnidadDosis = """SELECT * FROM """ + config.schema + """.unidad_dosis ORDER BY descripcion_unidad_dosis"""

strSelectEstadoFenologico = """SELECT * FROM """ + config.schema + """.estado_fenologico ORDER BY descripcion_estado_fenologico"""

strSelectTipoDocumento = """SELECT * FROM """ + config.schema + """.tipo_documento ORDER BY codigo_tipo_documento"""

strSelectTemporada = """SELECT *,
                        'Temporada ' || date_part('year', fecha_inicio) || '-' || date_part('year', fecha_termino) as descripcion
                        FROM """ + config.schema + """.temporada
                        ORDER BY codigo_temporada desc"""
