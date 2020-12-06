# -*- coding: utf-8 -*-
import json
import os
import re
import shutil
import xml.etree.cElementTree as ET
from os.path import basename
from zipfile import ZipFile
import time
from subprocess import Popen, PIPE
import telegram


def send(msg, msg2, tok, cid):
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    if msg:
        msg.sort()
        mnsj = "Siguientes Comics/Mangas se han descargado:\n\n"
        for string in msg:
            longitud = len(mnsj) + len(string)
            if longitud < 4096:
                mnsj = mnsj + string
            else:
                time.sleep(2)
                bot = telegram.Bot(
                    token=tok)
                bot.sendMessage(chat_id=cid, text=mnsj)
                mnsj = string
        bot = telegram.Bot(
            token=tok)
        bot.sendMessage(chat_id=cid, text=mnsj)
    if msg2:
        msg2.sort()
        mnsj = "Siguientes Comics/Mangas han fallado:\n\n"
        for string in msg2:
            longitud = len(mnsj) + len(string)
            if longitud < 4096:
                mnsj = mnsj + string
            else:
                time.sleep(2)
                bot = telegram.Bot(
                    token=tok)
                bot.sendMessage(chat_id=cid, text=mnsj)
                mnsj = string
        bot = telegram.Bot(
            token=tok)
        bot.sendMessage(chat_id=cid, text=mnsj)

def conexion(secret):
    arp = Popen(['/usr/sbin/arp', '-n'], stdout=PIPE)
    grep = Popen(['/bin/grep', '-i', 'b8:27:eb:95:9f:bd'], stdin=arp.stdout, stdout=PIPE)
    arp.stdout.close()
    cut = Popen(['/usr/bin/cut', '-d', ' ', '-f1'], stdin=grep.stdout, stdout=PIPE)
    grep.stdout.close()

    output = cut.communicate()[0].decode('utf-8').strip()
    print (output, secret['ip'])
    if output != secret['ip']:
        secret['ip'] = output
        with open('/home/cristian/Github/TachiyomiMangaOrganizer/secrets.json', 'w') as outfile:  
            json.dump(secret, outfile) 
        conect = "adb connect " + output + ":" + secret['puerto']        
    else:
        conect = "adb connect " + secret['ip'] + ":" + secret['puerto']

    return conect



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


def generatexml(dic, finalpath, numero):
    root = ET.Element("ComicInfo", **{'xmlns:xsd': 'http://www.w3.org/2001/XMLSchema',
                                      'xmlns:xsi': 'http://www.w3.org/2001/XMLSchema-instance'})

    ET.SubElement(root, "Series",).text = dic['Series']
    ET.SubElement(root, "Number",).text = numero
    ET.SubElement(root, "Volume",).text = dic['Volume']
    ET.SubElement(root, "Publisher",).text = dic['Publisher']

    tree = ET.ElementTree(root)
    filename = finalpath + "/ComicInfo.xml"
    tree.write(filename, encoding='utf-8', xml_declaration=True)


def organizer(elemento, dic, finalpath, mensaj, mensaj2):
    tilde = False
    tags = ['ep', 'ch', 'chapter', 'chapterr', 'chap', 'episodio', 'capitulo', 'num', 'issue', 'generations']
    
    
    numero = ''
    fecha = ''
    cadena = elemento[1].lower().replace('ch.','ch ').replace(':', ' ').replace(u'núm.','num ').replace(u'ó','o').replace(u'á','a').replace(u'́é','e').replace(u'í','i').replace(u'ú','u').replace(u'ñ','n').replace(u'é','e').replace(u'“','').replace(u'”','').replace(u'«','').replace(u'»','').replace(u'ô','o').replace(u'â','a').replace('.hu', '').replace('.lr', '').replace('shueisha_', '')
    # print(cadena)
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
            # print(numero)
            if isint(numero):
                issue = '{:0>4}'.format(numero)
            else:
                if isfloat(numero):
                    issue = '{:0>6}'.format(numero)
            generatexml(dic, finalpath, issue)
            cbz = dic['destino'] + "/" + dic['name'] + issue + ".cbz"
            archivos = os.listdir(finalpath)
            archivos.sort()
            zipobje = ZipFile(cbz, 'w')
            for archivos2 in archivos:
                finalpath2 = finalpath + "/" + archivos2
                zipobje.write(finalpath2, basename(archivos2))
            zipobje.close()
            try:
                shutil.rmtree(finalpath)
            except:
                print('Error while deleting directory')

            mensaj.append(dic['name'] + issue + "\n\n")
        else:
            
            try:
                shutil.move(finalpath, "/media/cristian/Datos/Comics/Fallo/"+elemento[1])
            except:
                print('Error while moving directory')
            try:
                shutil.rmtree(finalpath)
            except:
                print('Error while deleting directory')

            mensaj2.append(finalpath + " Patron encontrado es: " + numero +"\n\n")

    if fecha != '':
        # print(fecha)
        generatexml(dic, finalpath, fecha)
        cbz = dic['destino'] + "/" + dic['name'] + fecha + ".cbz"
        archivos = os.listdir(finalpath)
        archivos.sort()
        zipobje = ZipFile(cbz, 'w')
        for archivos2 in archivos:
            finalpath2 = finalpath + "/" + archivos2
            zipobje.write(finalpath2, basename(archivos2))
        zipobje.close()
        try:
            shutil.rmtree(finalpath)
        except:
            print('Error while deleting directory')

        mensaj.append(dic['name'] + fecha + "\n\n")
    tilde = False


def main():
    mensaj = []
    mensaj2 = []
    
    with open('/home/cristian/Github/TachiyomiMangaOrganizer/mangas.json') as json_file:
        mangas = json.load(json_file)
    with open('/home/cristian/Github/TachiyomiMangaOrganizer/secrets.json') as json_file2:
        secrets = json.load(json_file2)
    # conect = "adb connect " + secrets['ip']
    os.system(conexion(secrets))
    os.system("adb pull /storage/emulated/0/Tachiyomi /media/cristian/Datos/Comics")
    path = "/media/cristian/Datos/Comics/Tachiyomi"
    dirs = os.listdir(path)
    dirs.sort()
    for file1 in dirs:
        path2 = path + "/" + file1
        if path2 != '/media/cristian/Datos/Comics/Tachiyomi/automatic':
            if os.path.isdir(path2):
                files = os.listdir(path2)
                for file2 in files:
                    path3 = path2 + "/" + file2
                    # print(path3)
                    if path3 != '/media/cristian/Datos/Comics/Tachiyomi/backup/automatic':                        
                        if os.path.isdir(path3):
                            files2 = os.listdir(path3)
                            for file3 in files2:
                                path4 = path3 + "/" + file3
                                organizer([file2,file3], mangas[path3],
                                                 path4, mensaj, mensaj2)
    os.system(
        'adb shell "find /storage/emulated/0/Tachiyomi/ -type d -mindepth 3 -exec rm -rf "{}" \;"')
    send(mensaj, mensaj2, secrets['token'], secrets['chatid'])



if __name__ == "__main__":
    main()
