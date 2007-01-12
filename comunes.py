#!/usr/bin/env python
# -*- coding: utf-8 -*-
# comunes -- Libreería de objetos y constantes comunes para todo el proyecto
# (c) Fernando San Martín Woerner 2003, 2004, 2005
# snmartin@galilea.cl


from GladeConnect import GladeConnect
import sys
import string, re
import gobject
import gtk
import time
import os
from types import StringType
import math
from pyBusqueda import *
from dialogos import *
from fechas import ND, CDateLocal, CDateDB, GetDateFromModel
from completion import *
from codificacion import *
from constantes import *
from psycopg import connect
import locale
from decimal import Decimal


if sys.platform=="win32":
    impresora = 'lpt1:'
else:
    impresora = 'lpr:'
            
def CNumDb(s):
    try:
        s = float(s)
    except:
        print "not float"
    if type(s) == float:
        return str(s)
    s = str(s)
    p = len(s)
    t = ""
    for i in range(p):
        c = s[i]
        if c == ',':
            t = t + "."
        elif not c == ".":
            t = t + c
    return t

def moneyfmt(value, places=2, curr='', sep=',', dp='.',
             pos='', neg='-', trailneg=''):
    """Convert Decimal to a money formatted string.

    places:  required number of places after the decimal point
    curr:    optional currency symbol before the sign (may be blank)
    sep:     optional grouping separator (comma, period, space, or blank)
    dp:      decimal point indicator (comma or period)
             only specify as blank when places is zero
    pos:     optional sign for positive numbers: '+', space or blank
    neg:     optional sign for negative numbers: '-', '(', space or blank
    trailneg:optional trailing minus indicator:  '-', ')', space or blank

    >>> d = Decimal('-1234567.8901')
    >>> moneyfmt(d, curr='$')
    '-$1,234,567.89'
    >>> moneyfmt(d, places=0, sep='.', dp='', neg='', trailneg='-')
    '1.234.568-'
    >>> moneyfmt(d, curr='$', neg='(', trailneg=')')
    '($1,234,567.89)'
    >>> moneyfmt(Decimal(123456789), sep=' ')
    '123 456 789.00'
    >>> moneyfmt(Decimal('-0.02'), neg='<', trailneg='>')
    '<.02>'

    """
    q = Decimal((0, (1,), -places))    # 2 places --> '0.01'
    sign, digits, exp = value.quantize(q).as_tuple()
    assert exp == -places    
    result = []
    digits = map(str, digits)
    build, next = result.append, digits.pop
    if sign:
        build(trailneg)
    for i in range(places):
        if digits:
            build(next())
        else:
            build('0')
    build(dp)
    i = 0
    while digits:
        build(next())
        i += 1
        if i == 3 and digits:
            i = 0
            build(sep)
    build(curr)
    if sign:
        build(neg)
    else:
        build(pos)
    result.reverse()
    return ''.join(result)

def CMon(s, dec = 1):
    try:
        A = float(s)
        s = CNumDb(s)
    except:
        #print "ret", s
        return s
    d = Decimal(str(s))
    if s == "0.0":
        return "0." + ("0"*dec)
    if dec >= 1:
        return moneyfmt(d, places=dec, sep=".", dp=",")
    else:
        return moneyfmt(d, places=dec, sep=".", dp=",")[:-1]
def columna_numerica(tree, cell, model, iter, data = 0):
    pyobj = model.get_value(iter, data)
    pyobj = str(pyobj)
    cell.set_property('text', CMon((pyobj.replace(".", ",")),0))
    cell.set_property('xalign', 1)

def columna_real(tree, cell, model, iter, data = 0):
    pyobj = model.get_value(iter, data)
    if not  pyobj is None:
        cell.set_property('text', CMon(pyobj.replace(".", ","), 2))
        cell.set_property('xalign', 1)
    else:
        cell.set_property('text', CMon(pyobj, 2))
        cell.set_property('xalign', 1)


def columna_rut(tree, cell, model, iter, data = 0):
    pyobj = model.get_value(iter, data)
    cell.set_property('text', CRut(pyobj))
    cell.set_property('xalign', 1)

def columna_fecha(tree, cell, model, iter, data = 0):

    pyobj = model.get_value(iter, data)
    if pyobj is None:
        cell.set_property('text', "Sin Fecha")
        cell.set_property('xalign', 1)
    else:
        cell.set_property('text', CDateLocal(pyobj))
        cell.set_property('xalign', 1)

def columna_utf8(tree, cell, model, iter, data = 0):
    try:
        pyobj = model.get_value(iter, data)
    except:
        pyobj = ""
    try:
        cell.set_property('text', CUTF8(pyobj))
    except:
        cell.set_property('text', CUTF8(pyobj, 'latin1'))

def columna_vacia(tree, cell, model, iter, data = ''):
    cell.set_property('text', ' ')
    cell.set_property('xalign', 1)

def es_rut(rut=None):
    if not rut: return 0
        
    es_rut = 0
    cadena = "234567234567"
    dig_rut = rut[-1]
    
    rut = string.replace(rut, ".", "")
    rut = rut[:rut.find("-")]
    rut = string.replace(rut, " ", '0')
            
    j, suma, i = 0, 0, len(rut) -1
    
    while i >= 0:
        try:
            suma = suma + (int(rut[i]) * int(cadena[j]))
        except:
            return 0
        
        i = i - 1
        j = j + 1
    
    divid = int(suma/11)
    mult = int(divid*11)
    dife = suma - mult
    digito = 11 - dife
    
    if digito == 10:
        caract = "K"
    elif digito == 11:
        caract = "0"
    else:
        caract = string.replace(str(digito), " ", "")
    
        
    if caract == dig_rut: es_rut = 1
    
    return es_rut    

def CRut(rut):
    if rut == "":
        return rut
    rut = string.replace(rut,".","")
    rut = string.replace(rut,"-","")
    rut = "0000000000"+ rut
    l = len(rut)
    rut_aux = "-" + rut[l-1:l]
    l = l-1
    while 2 < l:
        rut_aux = "."+ rut[l-3:l] +rut_aux
        l = l-3
    rut_aux = rut[0:l] +rut_aux
    l = len(rut_aux)
    rut_aux = rut_aux[l-12:l]
    return rut_aux


def end_match(completion=None, key=None, iter=None, column=None):
    model = completion.get_model()
    text = model.get_value(iter, column)
    key = unicode(key,'latin1').encode('utf-8')
    if unicode(text,'latin1').encode('utf-8').upper().find(key.upper()) <> -1:
        return True
    return False


def Abre_pdf(arch):
    if sys.platform=="win32":
        acrord = 'c:\\Archivos de programa\\Adobe\\Acrobat 5.0\\Reader\\AcroRd32.exe'

        #~ acrord = "explorer.exe"
        #~ acrord = os.getcwd() + "\\pdfreader\\pdfreader.exe"

        args = [acrord, "AcroRd32.exe",arch]

        try:
            os.spawnv(os.P_NOWAIT, args[0], args[1:])
            print "acro"
        except:
            acrord = os.getcwd() + "\\pdfreader\\pdfreader.exe"
            args = [acrord, "pdfreader.exe",arch]
            try:
                os.spawnv(os.P_NOWAIT, args[0], args[1:])
                print "PDFReader"
            except:
                print "no hay un visor registrado."
    else:
        if os.spawnv(os.P_NOWAIT, '/usr/bin/evince', ['evince', arch]) != 0 :
            return 
        if os.spawnv(os.P_NOWAIT, '/usr/bin/xpdf', ['xpdf', arch]) != 0 :
            return
        if os.spawnv(os.P_NOWAIT, '/usr/bin/acroread', ['acroread', arch]) != 0 :
            return
        if os.spawnv(os.P_NOWAIT, '/usr/bin/gpdf', ['gpdf', arch]) != 0 :
            return
        

def IsNull(valor):
    if valor == None:
        return True
    else:
        return False
    
def Numlet(tyCantidad):
    _ret = None
    tyCantidad = round(tyCantidad)
    lyCantidad = int(tyCantidad)
    lyCentavos = ( tyCantidad - lyCantidad )  * 100
    laUnidades = ('UNA', 'DOS', 'TRES', 'CUATRO', 'CINCO', 'SEIS', 'SIETE', 'OCHO', 'NUEVE', 'DIEZ', 'ONCE', 'DOCE', 'TRECE', 'CATORCE', 'QUINCE', 'DIESISEIS', 'DIESISIETE', 'DIESIOCHO', 'DIESINUEVE', 'VEINTE', 'VEINTIUN', 'VEINTIDOS', 'VEINTITRES', 'VEINTICUATRO', 'VEINTICINCO', 'VEINTISEIS', 'VEINTISIETE', 'VEINTIOCHO', 'VEINTINUEVE')
    laDecenas = ('DIEZ', 'VEINTE', 'TREINTA', 'CUARENTA', 'CINCUENTA', 'SESENTA', 'SETENTA', 'OCHENTA', 'NOVENTA')
    laCentenas =('CIENTO', 'DOSCIENTOS', 'TRESCIENTOS', 'CUATROCIENTOS', 'QUINIENTOS', 'SEISCIENTOS', 'SETECIENTOS', 'OCHOCIENTOS', 'NOVECIENTOS')
    lnNumeroBloques = 1
    while 1:
        lnPrimerDigito = 0
        lnSegundoDigito = 0
        lnTercerDigito = 0
        lcBloque = ''
        lnBloqueCero = 0
        for i in range(1,4):
            lnDigito = lyCantidad % 10
            if lnDigito <> 0:
                _select0 = i
                if (_select0 == 1):
                    lcBloque = ' ' + laUnidades[lnDigito - 1]
                    lnPrimerDigito = lnDigito
                elif (_select0 == 2):
                    if lnDigito <= 2:
                        lcBloque = ' ' + laUnidades[( lnDigito * 10 )  + lnPrimerDigito - 1]
                    else:
                        lcBloque = ' ' + laDecenas[lnDigito - 1] + lcBloque
                    lnSegundoDigito = lnDigito
                elif (_select0 == 3):
                    if lnDigito == 1 and lnPrimerDigito == 0 and lnSegundoDigito == 0:
                        lcBloque = ' ' + 'CIEN'+ lcBloque
                    else:
                        lcBloque = ' ' + laCentenas[lnDigito - 1] + lcBloque
                    lnTercerDigito = lnDigito
            else:
                lnBloqueCero = lnBloqueCero + 1
            lyCantidad = int(lyCantidad / 10)
            if lyCantidad == 0:
                break
        _select1 = lnNumeroBloques
        if (_select1 == 1):
            _ret = lcBloque
        elif (_select1 == 2):
            _ret = lcBloque + IIf(lnBloqueCero == 3, '', ' MIL') + _ret
        elif (_select1 == 3):
            _ret = lcBloque + IIf(lnPrimerDigito == 1 and lnSegundoDigito == 0 and lnTercerDigito == 0, ' MILLON', ' MILLONES') + _ret
        lnNumeroBloques = lnNumeroBloques + 1
        if lyCantidad == 0:
            break
    _ret = _ret + IIf(tyCantidad > 1, ' PESOS ', ' PESO ') #+ Format(Str(lyCentavos), '00') + '/100 M.N. )'
    return _ret

def iif(cond, si, no):
    if cond:
        return si
    else:
        return no


def isNull(valor):
    if valor == None:
        return True
    else:
        return False

def ADer(pal,largo):
    try:
        pal = str(pal)
    except:
        pal = pal
    return pal.rjust(largo)

def AIzq(pal,largo):
    try:
        pal = str(pal)
    except:
        pal = pal
    return pal.ljust(largo)

def Ceros(pal, largo):
    try:
        pal = str(pal)
    except:
        pal = pal
    return pal.zfill(largo)

def Mid(pal, desde, hasta = 0):
    if hasta == 0:
        return pal[desde:]
    else:
        return pal[desde:hasta + desde]

def UCase(pal):
    return pal.upper()

if __name__ == '__main__':

    print CMon("100000.0".replace(".",","), 0)
    #Abre_pdf("comprobante_ingreso.pdf")
