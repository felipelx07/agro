# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import gtk
from comunes import *
def  GenColsByModel(modelo, indices,tree):
    """Genera Las TreeViewColumn a partir de un Modelo, Tomando como Parametros lo
            Siguiente:
        Modelo: gtk.ListStore(n*gType)
        Indice  : Arreglo en en cual se indican las propiedades de las TreeViewColumn
            ("IdColModelo":12,"TituloColumna":"asas","FormatCol":"str","Func":"funct","ColBand":"1","Editable":True,"cc":"CC")
            * Indice[0]: ID Columna del Modelo
            * Indice[1]: Titulo de la Columna
            * Indice[2]: Tipo de La columna (de acuerdo a esto se da Formato a la Vista de los Datos)
            Indice[3]: Se define segun los Tipos:
                                boo: funcion fixed_toggled
                                Otros: [Editable] Columna Que Guarda la Marca de modificacion
            Indice[4]: segun los Tipos
                                boo: editable
                                Otros: SimpleTree.CellCompletion()
            indices[5]: funcio, se utiliza Solo si al momento de editar una celda se nececita lanzar una funcion
    """
    nCols = 0
    for i in indices:
        if i[2] =="bool":
            render = gtk.CellRendererToggle()
            if len(i) ==4:
                if i[3] != False:
                    render.connect('toggled', i[3], modelo)
            else:
                render.connect('toggled', fixed_toggled, modelo, i[0])

            column = gtk.TreeViewColumn(i[1], render, active=i[0])
            if len(i) ==4:
                if i[3] != False:
                    column.set_clickable(True)
                    column.connect('clicked', column_click_ok,modelo, tree, i[0],nCols)
            else:
                column.set_clickable(True)
                column.connect('clicked', column_click_ok,modelo, tree, i[0],nCols)

        else:
            render = gtk.CellRendererText()

            if len(i) >= 4:
                if len(i) == 5:
                    render.set_property('mode',gtk.CELL_RENDERER_MODE_EDITABLE)
                    render.connect("editing-started",edited_cc,i[4])
                if len(i) == 6:
                    render.connect("edited",edited_cb,modelo,i[0],i[3],i[5])
                else:
                    render.connect("edited",edited_cb,modelo,i[0],i[3])
                render.set_property('editable',True)

            column = gtk.TreeViewColumn(i[1], render, text=i[0])
            column.set_resizable(True)
            if i[2] =="str":#str
                column.set_cell_data_func(render, columna_utf8, i[0])
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0],nCols)

            elif i[2] =="float":#float:
                column.set_cell_data_func(render, columna_real, i[0])

            elif i[2] =="int":
                column.set_cell_data_func(render, columna_numerica, i[0])

            elif i[2] =="rut":
                column.set_cell_data_func(render, columna_rut, i[0])
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0],nCols)

            elif i[2] =="dte":
                column.set_clickable(True)
                column.connect('clicked', column_click,modelo, tree, i[0],nCols)
                column.set_cell_data_func(render, columna_fecha, i[0])
        #column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        column.set_expand(False)
        tree.append_column(column)
        nCols = nCols +1

    tree.set_model(modelo)

def fixed_toggled(cell, path, model, col):
    iter = model.get_iter((int(path),))
    fixed = model.get_value(iter, col)
    fixed = not fixed
    model.set(iter, col, fixed)
def column_click_ok(treeColumn= None,modelo = None, tree = None,NColModelo= None,NColTree= None):
    for i in modelo:
        i[NColModelo] = not i[NColModelo]
def column_click(treeColumn= None,modelo = None, tree = None,NColModelo= None,NColTree= None):
    for i in tree.get_columns():
        i.set_sort_indicator(False)

    modelo.set_sort_column_id(NColModelo,0)
    tree.set_search_column(NColModelo)
    tree.get_column(NColTree).set_sort_indicator(True)

def edited_cb(cell, path, new_text,modelo=None,col = None,colBand=None,Func=None):

    iter = modelo.get_iter((int(path),))
    modelo.set(iter, col, new_text.upper())
    if colBand != None:
        modelo.set(iter, colBand, True)
    if Func !=None:
        Func(new_text.upper(),modelo,iter,int(path))

def edited_cc(cell, editable, path, data):
    """ Define un gtk.EntryCompletion a una celda
        cell : Celda a setear
        editable : gtk.entry
        data : EntryCompletion
    """
    #editable.show_all(True)
    editable.set_completion(data.get_completion())

class CellCompletion:
    """
        Generador de EntryCompletio para SimpleTree
        cnx : Conexion a la Base de Datos
        sql  : Consulta SQL para la obtencion de los Datos
        selfunc: Funcion de verificacion una vez seleccionado un datos
        sql_where: Variable de filtro para la Consulta SQL
    """
    def __init__(self,cnx,sql=None, selfunc=None,sql_where=None):

        self.completion = gtk.EntryCompletion()
        self.sql = sql
        self.sql_where = sql_where
        self.selfunc = selfunc
        self.cnx = cnx
        self.cursor = self.cnx.cursor()
        self.modelo = gtk.ListStore(str,str)
        self.completion.set_model(self.modelo)
        self.completion.connect("match-selected", self.__item_selected)
        self.completion.set_match_func(self.__match)
        self.selcol=0
        self.match_all =False
        self.completion.set_text_column(self.selcol)
        self.__carga_modelo__()

    def __carga_modelo__(self):
        if self.sql != None:
            if self.sql_where != None:
                if self.sql.upper().find("WHERE") != -1:
                    sql = "%s and %s" % (self.sql, self.sql_where)

                else:
                    sql = "%s where %s" % (self.sql, self.sql_where)

            else:
                sql = self.sql

            self.cursor.execute(sql)
            r = self.cursor.fetchall()
            self.modelo.clear()
            for i in r:
                self.modelo.append([CUTF8(j) for j in i])

    def __item_selected(self, completion, model, iter):
        if self.selfunc != None:
            self.selfunc(completion, model, iter)

    def set_where(self,where=None):
        self.sql_where = where
        self.__carga_modelo__()

    def set_sql(self, sql=None):
        self.sql = sql
        self.__carga_modelo__()

    def get_completion(self):
        return self.completion

    def __match(self, completion, entrystr, iter, data=None):
        model = completion.get_model()
        modelstr = model[iter][self.selcol]

        if self.match_all:
            return entrystr.upper() == modelstr.upper()[:len(entrystr.upper())]

        else:
            return entrystr.upper() in modelstr.upper()
