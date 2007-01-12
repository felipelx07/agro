#!/usr/bin/env python
# -*- coding: UTF8 	-*-
import sys
import os
from fechas import CDateLocal

class TreeToHTML:
    
    def __init__(self, tree=None, title="", cols=[]):
        self.treeview = tree
        self.html = ""
        self.title = title
        self.cols = cols

        
    def tohtml(self):
        self.html = '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">'
        self.html += "<h1>%s</h1>" % self.title
        self.html += "<table><tr>"
        for i in self.treeview.get_columns():
            self.html += "<th>%s</th>" % i.get_title()

        for i in self.treeview.get_model():
            self.html += "<tr>"
            for j in self.cols:
                if type(j) is int:
                    col = j
                    tipo = ""
                else:
                    col = j[0]
                    tipo = j[1]
                text = i[col]
                if text is None:
                    text = ""
                
                if tipo == "dte":
                    text = CDateLocal(text)
                
                self.html += "<td>%s</td>" % text
            self.html += "</tr>"    
            
        self.html += "</tr>"
        self.html += "</table>"
        
    def show(self):
        self.tohtml()
        f = open("reporte.html", "w")
        f.write(self.html)
        f.close()
        if sys.platform == "win32":
            os.system("explorer reporte.html")
        else:
            os.system("firefox reporte.html")