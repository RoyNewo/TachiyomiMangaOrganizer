# -*- coding: utf-8 -*-
import sqlite3
from sqlite3 import Error
import re
import json


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

def isfloat(x):
    try:
        float(x)
    except ValueError:
        return False
    else:
        return True


def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

    

    

        


    # for row in rows:
    #     print(row)





def main():
    database = "/media/cristian/Datos/Comics/Buffer/databases/tachiyomi.db"
    # mensaj = []
    
    # with open('/opt/tachiyomimangaexporter/mangas.json') as json_file:
    #     mangas = json.load(json_file)
    # with open('/opt/tachiyomimangaexporter/secrets.json') as json_file2:
    #     secrets = json.load(json_file2)

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("2. Query all tasks")
        lista = select_all_tasks(conn)
    
    tilde = False
    tags = ['ep', 'ch', 'chapter', 'chapterr', 'chap', 'episodio', 'capitulo', 'num', 'issue', 'generations']
    print(lista)
    
    for elemento in lista:
        numero = ''
        fecha = ''
        cadena = elemento[1].lower().replace('ch.','ch ').replace(':', ' ').replace(u'núm.','num ').replace(u'ó','o').replace(u'á','a').replace(u'́é','e').replace(u'í','i').replace(u'ú','u').replace(u'ñ','n').replace(u'é','e').replace(u'“','').replace(u'”','').replace(u'«','').replace(u'»','').replace(u'ô','o').replace(u'â','a').replace('.hu', '').replace('.lr', '')
        palabra = 0
        primero = False
        continuar = True
        while continuar:
            if palabra == 0:
                if re.findall("^#", cadena.split()[palabra]):
                    numero = cadena.split()[palabra].replace('#','')
                    primero = True
                    tilde = True
                if re.findall("[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]", cadena.split()[palabra]):
                    fecha = cadena.split()[palabra]
                    primero = True
                    tilde = True
                if cadena.split()[palabra] in tags :
                    if re.findall("^\.", cadena.split()[palabra+1]) or re.findall("\.$", cadena.split()[palabra+1]):
                        numero = cadena.split()[palabra+1].replace('.', '')
                        primero = True
                    else:
                        numero = cadena.split()[palabra+1]
                        primero = True
                    tilde = True

            else:
                cadena = cadena.replace('#','')
                if cadena.split()[palabra] in tags :
                    if re.findall("^\.", cadena.split()[palabra+1]) or re.findall("\.$", cadena.split()[palabra+1]):
                        numero = cadena.split()[palabra+1].replace('.', '')
                        primero = True
                    else:
                        numero = cadena.split()[palabra+1]
                        primero = True
                    tilde = True
            palabra += 1
            if primero:
                continuar = False
            if palabra >= len(cadena.split()):
                continuar = False
        if not tilde:
            titulo = elemento[0].replace(u'·','').replace(u'ô','o').replace(':', ' ').replace('-', ' ').replace('.', ' ')
            cadena = cadena.lower().replace(elemento[0].lower().replace(u'·','').replace(u'ô','o'), '').replace(':', ' ').replace('-', ' ')
            for words in range(len(titulo.split())):
                cadena = cadena.replace(titulo.split()[words].lower(), '')
            if re.findall("^vol\.", cadena.lower().replace(elemento[0].lower().replace(u'·',''),'').replace(' ', '')) or re.findall("^vol", cadena.lower().replace(elemento[0].lower().replace(u'·',''),'').replace(' ', '')):
                cadena = cadena.replace('vol.', '').replace('vol','')
                # print(cadena.lower().replace(elemento[0].lower().replace(u'·',''),'').replace(' ', '').replace('vol.', ''))
            elif re.findall("^\.", cadena.lower().replace(elemento[0].lower().replace(u'·',''),'').replace(' ', '')) or re.findall("\.$", cadena.lower().replace(elemento[0].lower().replace(u'·',''),'').replace(' ', '')):
                cadena = cadena.replace('.', '').replace(' ', '')
                # print(cadena.lower().replace(elemento[0].lower().replace(u'·',''),'').replace(' ', '').replace('.', ''))
            
            cadena = cadena.replace(' ', '')
            numero = cadena
        if numero != '':
            if isint(numero) or isfloat(numero):
                print(numero)
            else:
                print('fallo', numero)
        if fecha != '':
            print(fecha)
        tilde = False





    # weeklyroll = '#003 - Z=3:KING OF THE STONE WORLD'
    # cadena = weeklyroll.lower().replace('ch.','ch ').replace(':', ' ').replace(u'núm.','num ').replace(u'ó','o').replace(u'á','a').replace(u'́é','e').replace(u'í','i').replace(u'ú','u').replace(u'ñ','n').replace(u'é','e').replace(u'“','').replace(u'”','').replace(u'«','').replace(u'»','').replace(u'ô','o').replace('#','').replace(u'â','a')
    # for palabra in range(len(cadena.split())):
    #     print(cadena.split()[palabra])
    #     if palabra == 0:
    #         if re.findall("^#", cadena.split()[palabra]):
    #             print(cadena.split()[palabra].replace('#',''))
    #             primero = True
    #             tilde = True
           


        


if __name__ == '__main__':
    main()