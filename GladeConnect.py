#!/usr/bin/env python
# -*- coding: utf-8 -*-
# GladeConnect -- Clase base para conectar glade y python

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

# Copyright Benjamin POUSSIN < bpoussin@free.fr >,
# Sebastien REGNIER < seb.regnier@free.fr >
# Benoit CLOUET < b.clouet@free.fr > 

import pygtk
#pygtk.require('2.0')

import gtk.glade
import gtk
import sys
import os
import inspect
import time
from SimpleGladeApp import SimpleGladeApp
from kiwi.ui.entry import KiwiEntry
from kiwi.ui.dateentry import DateEntry

class PrefixActions:
    def __init__(self):
        self.mandatories = []

    def prefix_enc(self, widget):
        def validate(widget,*args):
            try:
                selected = widget.get_data("selected")
                print selected
                if selected:
                    error = False
                else:
                    error =True
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("focus_out_event", validate)
        widget.connect("changed", validate)

    def prefix_Enc(self,widget):
        self.prefix_enc(widget)
        self.add_mandatory(widget)


    def prefix_ent(self, widget):
        def validate(widget):
            text = widget.get_text().strip()
            if text == "None":
                text = ""
                widget.set_text(text)
            self.set_error_status(widget, len(text) < 1)

        def complete(widget, event):
            text = widget.get_text().strip()
            widget.set_text(text.upper())
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)

    def prefix_Ent(self, widget):
        self.prefix_ent(widget)
        self.add_mandatory(widget)

    def prefix_name(self, widget):
        def validate(widget):
            text = widget.get_text()
            self.set_error_status(widget, len(text) < 1 or len(text) > 16)
        def complete(widget, event):
            text = widget.get_text()
            cap = lambda s: s.capitalize()
            tokens = text.split()
            tokens = map(cap, tokens)
            text = " ".join(tokens)
            widget.set_text(text)
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)

    def prefix_Name(self, widget):
        self.prefix_name(widget)
        self.add_mandatory(widget)

    def prefix_date(self, widget):
        def parse_date(text):
            (cY,cm,cd) = time.localtime()[0:3]
            try:
                (d,) = time.strptime(text, "%d")[2:3]
                m,Y = cm,cY
            except ValueError:
                try:
                    (m,d) = time.strptime(text, "%d/%m")[1:3]
                    Y = cY
                except:
                    (Y,m,d) = time.strptime(text, "%d/%m/%Y")[0:3]
            return (Y,m,d)
        def validate(widget):
            text = widget.get_text()
            try:
                parse_date(text)
                error = False
            except ValueError:
                error = True
                print "error " + text
            self.set_error_status(widget,error)
        def complete(widget, event):
            text = widget.get_text()
            try:
                (Y,m,d) = parse_date(text)
                text = "%02d/%02d/%d" % (d,m,Y)
                widget.set_text(text)
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
        widget.connect("focus-out-event", complete)

    def prefix_Date(self, widget):
        self.prefix_date(widget)
        self.add_mandatory(widget)

    def prefix_age(self, widget):
        def validate(widget):
            text = widget.get_text()
            try:
                age = int(text)
                if age < 16 or age > 99:
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)

    def prefix_Age(self, widget):
        self.prefix_age(widget)
        self.add_mandatory(widget)

    def prefix_cash(self, widget):
        def validate(widget):
            text = widget.get_text()
            try:
                cash = float(text)
                if cash < 0:
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)

    def prefix_Cash(self, widget):
        self.prefix_cash(widget)
        self.add_mandatory(widget)

    def prefix_rut(self,widget):
        def Format_Rut(widget, event):
            print "format"
            rut = widget.get_text()
            if rut == "":
                return rut

            rut = rut.replace(".","")
            rut = rut.replace("-","")
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
            widget.set_text(rut_aux)

        def es_rut(rut=None):
            if not rut: return 0
            es_rut = False
            cadena = "234567234567"
            dig_rut = rut[-1]
            rut = rut.replace(".", "")
            rut = rut[:rut.find("-")]
            rut = rut.replace(" ", '0')
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
                caract = str(digito).replace(" ", "")

            if caract == dig_rut:
                es_rut = True

            return es_rut

        def validate(widget):
            print "validate"
            text = widget.get_text()
            try:
                cash = not es_rut(text)
                if cash :
                    raise ValueError
                error = False
            except ValueError:
                error = True
            self.set_error_status(widget,error)
        widget.connect("changed", validate)
        print "changed connected", widget.get_name()
        widget.connect("focus-out-event", Format_Rut)
        print "focus-out connected", widget.get_name()

    def prefix_Rut(self, widget):
        self.prefix_rut(widget)
        self.add_mandatory(widget)

    def add_mandatory(self, widget):
        self.mandatories.append(widget)
        widget.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse("blue"))
        widget.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse("light blue"))
        label_prefix = '<b><span color="red">*</span></b>'
        eid = widget.get_name()[3: ]
        label = getattr(self,"lbl%s" % eid)
        markup = label_prefix + label.get_label()
        label.set_markup(markup)

    def set_error_status(self, widget, error_status):
        if error_status:
            color_s = "#FF6B6B"
            widget.set_data("is-valid", None)
        else:
            widget.set_data("is-valid", True)
            color_s = "#FFFFFF"
        color = gtk.gdk.color_parse(color_s)
        widget.modify_base(gtk.STATE_NORMAL, color)
        can_apply = True
        for mandatory in self.mandatories:
            if not mandatory.get_data("is-valid"):
                can_apply = False
        try:
            self.btnAceptar.set_sensitive(can_apply)
        except:
            pass


class GladeConnect(SimpleGladeApp, PrefixActions):

    def __init__(self, filename=None, root=None):
        SimpleGladeApp.__init__(self, filename, root)
        PrefixActions.__init__(self)
        self.add_prefix_actions(self)
        for dialog in self.get_widgets():
            if isinstance(dialog, gtk.Dialog):
                dialog.connect('key-release-event', self.hide_dialog)
        self.check_widgets()

    def on_exit(self, btn=None, data=None):
        self.quit()

    def hide_dialog(self, dialog, event):
        if event.keyval == gtk.keysyms.Escape:
            dialog.hide()

    def clear_form(self):
        t = type(gtk.Entry())
        s = type(gtk.SpinButton())
        for i in self.get_widgets():
            if type(i) == t:
                i.set_text("")
            elif type(i) == s:
                min, max = i.get_range()
                i.set_value(min)
                
    def check_widgets(self):
        for i in self.glade.get_widget_prefix("kdt"):
            widget = DateEntry()
            i.pack_start(widget, False, False)
            name = i.name.replace("kdt", "ent")
            c = compile("self.%s = widget" % name, '<string>', 'exec')
            eval(c)
        for i in self.glade.get_widget_prefix("krt"):
            widget = KiwiEntry()
            widget.set_mask("00.000.000-A")
            #p = widget.render_icon(gtk.STOCK_OK, gtk.ICON_SIZE_MENU)
            #widget.set_pixbuf(p)
            i.pack_start(widget, True, True)
            name = i.name.replace("krt", "ent")
            c = compile("self.%s = widget" % name, '<string>', 'exec')
            eval(c)
        for i in self.glade.get_widget_prefix("ktm"):
            widget = KiwiEntry()
            widget.set_mask("00:00")
            i.pack_start(widget, False, False)
            name = i.name.replace("ktm", "ent")
            c = compile("self.%s = widget" % name, '<string>', 'exec')
            eval(c)
