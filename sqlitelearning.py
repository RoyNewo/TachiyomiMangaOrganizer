# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
import re


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT manga_id, name FROM chapters")

    rows = cur.fetchall()
    cur.execute("SELECT _id, title FROM mangas")
    rows2 = cur.fetchall()
    
    mangasdic = {}
    capitulos = []
    for iterable in rows2:
        mangasdic[iterable[0]] = iterable[1]
    
    for mangasid, name in rows:
        capitulos.append([mangasdic[mangasid], name])

    return capitulos

    

    

        


    # for row in rows:
    #     print(row)





def main():
    database = "/media/cristian/Datos/Comics/Buffer/databases/tachiyomi.db"
    mensaj = []
    
    with open('/home/cristian/Github/TachiyomiMangaOrganizer/mangas.json') as json_file:
        mangas = json.load(json_file)
    with open('/home/cristian/Github/TachiyomiMangaOrganizer/secrets.json') as json_file2:
        secrets = json.load(json_file2)

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("2. Query all tasks")
        lista = select_all_tasks(conn)
    
    tilde = False
    tags = ['ep', 'ch', 'chapter', 'chapterr', 'chap', 'episodio', 'capitulo', 'num', 'issue']
    
    for elemento in lista:
        cadena = elemento[1].lower().replace('ch.','ch ').replace(':', ' ').replace(u'núm.','num ').replace(u'ó','o').replace(u'á','a').replace(u'́é','e').replace(u'í','i').replace(u'ú','u').replace(u'ñ','n').replace(u'é','e').replace(u'“','').replace(u'”','').replace(u'«','').replace(u'»','').replace(u'ô','o').replace('#','')
        for palabra in range(len(cadena.split())):
            if cadena.split()[palabra] in tags :
                print(cadena.split()[palabra+1])
                tilde = True
        if not tilde:
            print(cadena.lower().replace(elemento[0].lower().replace(u'·',''),''))
        tilde = False


        


if __name__ == '__main__':
    main()