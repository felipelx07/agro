import gtk
import config
def insertFromDict(table, dict):
    """Take dictionary object dict and produce sql for 
    inserting it into the named table"""
    sql = 'INSERT INTO ' + table
    sql += ' ('
    sql += ', '.join(dict)
    sql += ') VALUES ('
    sql += ', '.join(map(dictValuePad, dict))
    sql += ');'
    return sql

def dictValuePad(key):
    return '%(' + str(key) + ')s'
    
def updateFromDict(table, campos, llaves):
    """Take dictionary object dict and produce sql for 
    updating it into the named table"""
    dic = {}
    sql = 'UPDATE ' + table + " SET"
    for i in campos:
        sql = sql + " " + i + " = " + dictValuePad(i) + ", "
        dic[i] = campos[i]
    sql = sql[:-2]
    if not llaves is None:
        sql = sql + " WHERE"
        for i in llaves:
            sql = sql + " " + i + " = " + dictValuePad(i) + " AND "
            dic[i] = llaves[i]            
        sql = sql[:-5]
        
    return sql, dic

def deleteFromDict(table, llaves):
    dic = {}
    sql = 'DELETE FROM ' + table 
    if not llaves is None:
        sql = sql + " WHERE"
        for i in llaves:
            sql = sql + " " + i + " = " + dictValuePad(i) + " AND "
            dic[i] = llaves[i]            
        sql = sql[:-5]
    return sql

def type_to_str(expresion):
    if isinstance(expresion, bool):
        return expresion
    else:
        return str(expresion)

def ListStoreFromSQL(cnx, sql):
    cu = cnx.cursor()
    cu.execute(sql)
    r = cu.fetchall()
    if len(r) > 0:
        t = map(type_to_str, r[0])
        print map(type, t)
        l = gtk.ListStore(*map(type, t))
        m = l.append
        map(m, r)
    else:
        l = None    
    return l

if __name__ == "__main__":
    from  psycopg import connect
    DB = config.DB
    user = config.user
    password = config.password
    host = config.host
    
    cnx = connect(DB + " " + user + " " + password + " " + host )
    cnx.autocommit()
    c = cnx.cursor()
    
    #revisar para dejar en forma generica ESMW
    if False:
        cam = {}
        cam['cod_sistema'] = 'TST'
        cam['cod_nom'] = 'TST1'
        llav={}
        llav['nom'] = 'NOM1'
        llav['dir'] = 'DIR1'
        sql, dic = updateFromDict('test', cam, llav)
        print sql % dic
        dic['nombre_sistema'] = 'Sistema de test'
        sql = insertFromDict('ctb.sistema', dic)
        print "insertando..."
        print sql % dic
        c.execute(sql, dic)
        print "eliminando..."
        c.execute("delete from ctb.sistema where cod_sistema = 'TST'")
