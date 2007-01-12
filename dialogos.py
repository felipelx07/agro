#!/usr/bin/env python
# -*- coding: utf-8 -*-
# dialogos -- Clases básicas para los diálogos que utiliza el sistema.
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

import sys
from string import zfill
import gobject
import gtk
import time
from gtk import  MessageDialog, Dialog, Window
import os
from types import StringType
import traceback
import gettext

_ = gettext.gettext


class dlgAviso(MessageDialog):

    def __init__(self, parent_window = None, message = ""):
        MessageDialog.__init__(self,
                parent_window,
                gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                gtk.MESSAGE_INFO,
                gtk.BUTTONS_OK,
                unicode(StringType(message)).encode('utf-8'))
        self.set_default_response(gtk.BUTTONS_OK)
        self.connect('response', lambda dialog, response: dialog.destroy())
        self.show()

class dlgError(Dialog):

    def __init__(self, parent_window = None, message = "", quit = None, trace = True):
        Dialog.__init__(self,
                unicode(StringType("Error")).encode('utf-8'),
                parent_window,
                0,
                (gtk.STOCK_OK, gtk.RESPONSE_OK))

        self.set_default_size(400, 150)
        hbox = gtk.HBox(False, 8)
        hbox.set_border_width(8)
        self.vbox.pack_start(hbox, False, False, 0)
        stock = gtk.image_new_from_stock(
                                        gtk.STOCK_DIALOG_ERROR,
                                        gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(stock, False, False, 0)
        try:
            label = gtk.Label(unicode(StringType(message)).encode('utf-8'))
        except:
            label = gtk.Label("Ha ocurrido un error.")
        hbox.pack_start(label, True, True, 0)
        if trace:
            sw = gtk.ScrolledWindow()
            sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
            textview = gtk.TextView()
            textbuffer = textview.get_buffer()
            sw.add(textview)
            sw.show()
            textview.set_editable(False)
            textview.set_cursor_visible(False)
            textview.show()
            t = StringType(sys.exc_info()[0]) + "\n"
            t += StringType(sys.exc_info()[1]) + "\n"
            t += "Traza:\n"
            for i in traceback.format_tb(sys.exc_info()[2]):
                t += i + "\n"
            textbuffer.set_text(t)
            expander = gtk.Expander("Detalles")
            expander.add(sw)
            expander.set_expanded(True)
            self.vbox.pack_start(expander, True, True)
        self.show_all()
        self.response = self.run()
        self.destroy()

class dlgSiNo(Dialog):

    def __init__(self, parent_window = None, message = None, window_title = None):
        Dialog.__init__(self,
                window_title,
                parent_window,
                0,
                (gtk.STOCK_NO, gtk.RESPONSE_NO, gtk.STOCK_YES, gtk.RESPONSE_YES))
        hbox = gtk.HBox(False, 8)
        hbox.set_border_width(8)
        self.vbox.pack_start(hbox, False, False, 0)
        stock = gtk.image_new_from_stock(
                                        gtk.STOCK_DIALOG_QUESTION,
                                        gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(stock, False, False, 0)
        label = gtk.Label(message)
        hbox.pack_start(label, True, True, 0)
        self.show_all()
        self.response = self.run()
        self.destroy()

class dlgCalendario(Dialog):

    def __init__(self, parent_window = None, date = None, entry=None):
        Dialog.__init__(self, "Calendario", parent_window, 0,)
        self.set_position(gtk.WIN_POS_MOUSE)
        hbox = gtk.HBox(False, 8)
        hbox.set_border_width(8)
        self.vbox.pack_start(hbox, 1, False, 0)
        self.date = date
        calendar = gtk.Calendar()
        calendar.connect('day_selected_double_click', self.on_calendar_double_click)
        if date <> None and date <> "":
            calendar.select_day(int(date[0:2]))
            calendar.select_month(int(date[3:5])-1,int(date[6:10]))
        hbox.pack_start(calendar, True, True, 0)
        self.set_default_response(gtk.RESPONSE_CANCEL)
        if entry is not None:
            self.set_decorated(False)
            rect = entry.get_allocation()
            wx, wy = entry.get_size_request()
            win = entry.get_parent_window()
            tx, ty = win.get_position()
            self.move(rect.x + tx, rect.y + ty + wy)
            parent = entry
            while not isinstance(parent, gtk.Window):
                parent = parent.get_parent()
            self.set_transient_for(parent)
        self.show_all()
        calendar.grab_focus()
        response = self.run()
        if response == gtk.RESPONSE_OK:
            self.destroy()
            self.date = calendar.get_date()
            self.date = str(zfill(self.date[2],2)) +"/"+ str(zfill(self.date[1] +1,2))+"/"+ str(zfill(self.date[0],4))
        else:
            self.destroy()


    def on_calendar_double_click(self=None, window=None):
        self.response(gtk.RESPONSE_OK)

class dlgBarraProgreso(Window):

    def __init__(self, mensaje = "Completado", titulo = "Progreso", progreso = 0):
        m = unicode(mensaje, 'latin-1')
        t = unicode(titulo, 'latin-1')
        Window.__init__(self)
        self.set_title(t.encode('utf-8'))
        self.vbox = gtk.VBox()
        self.add(self.vbox)
        hbox = gtk.HBox(False, 8)
        hbox.set_border_width(8)
        self.vbox.pack_start(hbox, False, False, 0)
        stock = gtk.image_new_from_stock(
                                        gtk.STOCK_DIALOG_QUESTION,
                                        gtk.ICON_SIZE_DIALOG)
        hbox.pack_start(stock, False, False, 0)
        self.barra = gtk.ProgressBar()
        self.barra.set_text(m.encode('utf-8'))
        self.barra.set_fraction(progreso)
        hbox.pack_start(self.barra, True, True, 0)
        self.show_all()
        self.show()

def muestra_splash(texto = "Leyendo datos..."):
    w = gtk.Window()
    w.set_title("Gestor")
    w.set_decorated(False)
    w.set_position(gtk.WIN_POS_CENTER)
    image = gtk.Image()
    image.set_from_file("pixmaps/splash.png")
    v = gtk.VBox()
    w.add(v)
    v.pack_start(image)
    l = gtk.Label("Incializando...")
    v.pack_start(l)
    l.set_text(texto)
    w.show_all()
    def get_image( filename ):
        try:
            anim = gtk.gdk.PixbufAnimation( filename )
        except gobject.GError, e:
            return None
        image = gtk.Image()
        if anim.is_static_image():
            image.set_from_pixbuf( anim.get_static_image() )
        else:
            image.set_from_animation( anim )
        return image
    imgSolicitud = get_image("pixmaps/programer.gif")
    imgSolicitud.show()
    while gtk.events_pending(): gtk.main_iteration()
    return w

def InputBox(title, label, parent=None, text=''):
    dlg = gtk.Dialog(title, parent,gtk.DIALOG_DESTROY_WITH_PARENT,
                    (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                    gtk.STOCK_OK, gtk.RESPONSE_OK))
    if type(label) is list:
        entries=[]
        for i in label:
            lbl = gtk.Label(i)
            lbl.show()
            dlg.vbox.pack_start(lbl)
            entry = gtk.Entry()
            entry.show()
            dlg.vbox.pack_start(entry, False)
            entries.append(entry)
    else:
        lbl = gtk.Label(label)
        lbl.show()
        dlg.vbox.pack_start(lbl)
        entry = gtk.Entry()
        if text: entry.set_text(text)
        entry.show()
        dlg.vbox.pack_start(entry, False)
    
    resp = dlg.run()
    if not type(label) is list:
        text = entry.get_text()
    else:
        text = []
        for i in entries:
            text.append(i.get_text())
    dlg.hide()
    if resp == gtk.RESPONSE_CANCEL:
        return None
    return text



def messagedialog(dialog_type, short, long=None, parent=None,
                  buttons=gtk.BUTTONS_OK, additional_buttons=None):
    d = gtk.MessageDialog(parent=parent, flags=gtk.DIALOG_MODAL,
                          type=dialog_type, buttons=buttons)

    if additional_buttons:
        d.add_buttons(*additional_buttons)
    
    d.set_markup(short)
    
    if long:
        if isinstance(long, gtk.Widget):
            widget = long
        elif isinstance(long, basestring):
            widget = gtk.Label()
            widget.set_markup(long)
        else:
            raise TypeError("long must be a gtk.Widget or a string")
        
        expander = gtk.Expander(_("Haga click aquí para más detalles."))
        expander.set_border_width(6)
        expander.add(widget)
        d.vbox.pack_end(expander)
        
    d.show_all()
    response = d.run()
    d.destroy()
    return response
    
def error(short, long=None, parent=None):
    """Displays an error message."""
    return messagedialog(gtk.MESSAGE_ERROR, short, long, parent)

def info(short, long=None, parent=None):
    """Displays an info message."""
    return messagedialog(gtk.MESSAGE_INFO, short, long, parent)

def warning(short, long=None, parent=None):
    """Displays a warning message."""
    return messagedialog(gtk.MESSAGE_WARNING, short, long, parent)

def yesno(text, parent=None):
    return messagedialog(gtk.MESSAGE_WARNING, text, None, parent,
                         buttons=gtk.BUTTONS_YES_NO)
  
def dlgAbrirArchivo(title='', parent=None, patterns=[], folder=None):
    """Displays an open dialog."""
    filechooser = gtk.FileChooserDialog(title or _('Open'),
                                        parent,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))

    if patterns:
        file_filter = gtk.FileFilter()
        for pattern in patterns:
            file_filter.add_pattern(pattern)
        filechooser.set_filter(file_filter)
    filechooser.set_default_response(gtk.RESPONSE_OK)

    if folder:
        filechooser.set_current_folder(folder)
        
    response = filechooser.run()
    if response != gtk.RESPONSE_OK:
        filechooser.destroy()
        return
    
    path = filechooser.get_filename()
    if path and os.access(path, os.R_OK):
        filechooser.destroy()
        return path
        
    abspath = os.path.abspath(path)

    error(_('Could not open file "%s"') % abspath,
          _('The file "%s" could not be opened. '
            'Permission denied.') %  abspath)

    filechooser.destroy()
    return path

def dlgGuardarArchivo(title='', parent=None, current_name='', folder=None):
    """Displays a save dialog."""
    filechooser = gtk.FileChooserDialog(title or _('Save'),
                                        parent,
                                        gtk.FILE_CHOOSER_ACTION_SAVE,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_SAVE, gtk.RESPONSE_OK))
    if current_name:
        filechooser.set_current_name(current_name)       
    filechooser.set_default_response(gtk.RESPONSE_OK)
    
    if folder:
        filechooser.set_current_folder(folder)
        
    path = None
    while True:
        response = filechooser.run()
        if response != gtk.RESPONSE_OK:
            path = None
            break
        
        path = filechooser.get_filename()
        if not os.path.exists(path):
            break

        submsg1 = _('A file named "%s" already exists') % os.path.abspath(path)
        submsg2 = _('Do you which to replace it with the current project?')
        text = '<span weight="bold" size="larger">%s</span>\n\n%s\n' % \
              (submsg1, submsg2)
        result = messagedialog(gtk.MESSAGE_ERROR,
                               text,
                               parent=parent,
                               buttons=gtk.BUTTONS_NONE,
                               additional_buttons=(gtk.STOCK_CANCEL,
                                                   gtk.RESPONSE_CANCEL,
                                                   _("Replace"),
                                                   gtk.RESPONSE_YES))
        # the user want to overwrite the file
        if result == gtk.RESPONSE_YES:
            break

    filechooser.destroy()
    return path
    
def test():
    globals()['_'] = lambda s: s
    #print open(title='Open a file', patterns=['*.py'])
    #print save(title='Save a file', current_name='foobar.py')
    #error('An error occurred', gtk.Button('Woho'))
    #error('An error occurred',
    #      'Long description bla bla bla bla bla bla bla bla bla\n'
    #      'bla bla bla bla bla lblabl lablab bla bla bla bla bla\n'
    #      'lbalbalbl alabl l blablalb lalba bla bla bla bla lbal\n')
    dato = InputBox('Pregunta', 'dato:')
    print dato
if __name__ == '__main__':
    test()
