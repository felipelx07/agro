#!/usr/bin/env python
# -*- coding: utf-8 -*-
# codificacion -- Funciones generales para el manejo de UTF8
# (c) Fernando San Martín Woerner 2003, 2004, 2005
# snmartin@galilea.cl

# This file is part of Gestor.
#
# Gestor is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyGestor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Foobar; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

def CUTF8(string="", encode = None):
    if string is None:
        string = ""

    if encode is None:
        try:
            return unicode(string).encode('utf8')
        except:
            return unicode(string, 'latin1').encode('utf8')
    else:
        try:
            return unicode(string, 'latin1').encode('utf8')
        except:
            return unicode(string).encode('utf8')


def CISO(string=""):

    try:
        str1 = unicode(string).encode("ISO-8859-1")
    except:
        string = CUTF8(string,"")
        str1 = unicode(string).encode("ISO-8859-1")
    return str1
