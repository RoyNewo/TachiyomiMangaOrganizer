# -*- coding: utf-8 -*-
import nmap3
import json
import os
import re
import shutil
import xml.etree.cElementTree as ET
from os.path import basename
from zipfile import ZipFile
import time
from subprocess import Popen, PIPE, call
import telegram
import sys
import traceback
import requests
import glob

def posterm(manga):
    url = "https://kitsu.io/api/edge/manga?filter[slug]=" + manga['slug']
    response = requests.get(url)
    data = response.json()
    image = requests.get(data["data"][0]["attributes"]["posterImage"]["large"])
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)

def posterc(manga):
    print(manga["Series"])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    url = "https://comicvine.gamespot.com/api/volume/" + manga['slug'] + "/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
    response = requests.get(url, headers=headers)
    print(url, response)
    data = response.json()
    image = requests.get(data["results"]["image"]["super_url"])
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)



def my_exception_hook(type, value, tb):
    with open('/config/secrets.json') as json_file2:
        secretos = json.load(json_file2)
    traceback_details = '\n'.join(traceback.extract_tb(tb).format())
    error_msg = "Mangaexporter: An exception has been raised outside of a try/except!!!\n" \
        f"Type: {type}\n" \
        f"Value: {value}\n" \
        f"Traceback: {traceback_details}"
    print(error_msg)

    n = 4000
    for i in range(0, len(error_msg), n):
        bot = telegram.Bot(
                    token=secretos['token'])
        bot.sendMessage(chat_id=secretos['chatid'], text=error_msg[i:i+n])
        time.sleep(2)



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
    nmap = nmap3.Nmap()
    results = nmap.scan_top_ports("192.168.1.0/24", args="-sP -n")
    conect = ''
    # print(json.dumps(results))
    for key in results:
        # print(key)
        if "macaddress" in results[key]:
            if results[key]["macaddress"] != None:
                if "addr" in results[key]["macaddress"]:
                    if results[key]["macaddress"]["addr"] == "B8:27:EB:95:9F:BD":
                        # print(key)
                        if key != secret['ip']:
                            secret['ip'] = key
                            with open('/config/secrets.json', 'w') as outfile:
                                json.dump(secret, outfile)
                        conect = key
    if conect != '':
        return conect
    else:
        return None


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


def historial(history, issue, dic):
    if dic["Series"] in history:
        if issue in history[dic["Series"]]:
            if dic["provider"] != history[dic["Series"]][issue]:
                if dic["funcion"] != history[dic["Series"]][issue]:
                    # history[dic["Series"]].update({issue: dic["provider"]})
                    history[dic["Series"]].pop(issue, None)
                    return 'update'
                else:
                    return False
            else:
                return False
        else:
            history[dic["Series"]].update({issue: dic["provider"]})
            return True
    else:
        history[dic["Series"]] = {issue: dic["provider"]}
        return True


def organizer(elemento, dic, finalpath, mensaj, mensaj2, history):
    if not os.path.exists(dic["destino"]):
        os.makedirs(dic["destino"])
    if dic["slug"] != "undefined":
            if not os.path.exists(dic["destino"] + '/poster.jpg'):
                if dic["Publisher"] == "DC Comics" or dic["Publisher"] == "Marvel":
                    posterc(dic)
                else:
                    posterm(dic)
    tilde = False
    tags = ['ep', 'ch', 'chapter', 'chapterr', 'chap',
            'episodio', 'capitulo', 'num', 'issue', 'generations']

    numero = ''
    fecha = ''
    cadena = elemento[1].lower().replace('ch.', 'ch ').replace(':', ' ').replace(u'núm.', 'num ').replace(u'ó', 'o').replace(u'á', 'a').replace(u'́é', 'e').replace(u'í', 'i').replace(u'ú', 'u').replace(
        u'ñ', 'n').replace(u'é', 'e').replace(u'“', '').replace(u'”', '').replace(u'«', '').replace(u'»', '').replace(u'ô', 'o').replace(u'â', 'a').replace('.hu', '').replace('.lr', '').replace('shueisha_', '').replace('mangakakalot.com_','').replace('_','')
    # print(cadena)
    palabra = 0
    primero = False
    continuar = True
    while continuar:
        if palabra == 0:
            if re.findall("^#", cadena.split()[palabra]):
                numero = cadena.split()[palabra].replace('#', '')
                primero = True
                tilde = True
            if re.findall("[0-9][0-9][0-9][0-9]\.[0-9][0-9]\.[0-9][0-9]", cadena.split()[palabra]):
                fecha = cadena.split()[palabra]
                primero = True
                tilde = True
            if cadena.split()[palabra] in tags:
                if re.findall("^\.", cadena.split()[palabra+1]) or re.findall("\.$", cadena.split()[palabra+1]):
                    numero = cadena.split()[palabra+1].replace('.', '')
                    primero = True
                else:
                    numero = cadena.split()[palabra+1]
                    primero = True
                tilde = True

        else:
            cadena = cadena.replace('#', '')
            if cadena.split()[palabra] in tags:
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
        titulo = elemento[0].replace(u'·', '').replace(u'ô', 'o').replace(
            ':', ' ').replace('-', ' ').replace('.', ' ')
        cadena = cadena.lower().replace(elemento[0].lower().replace(
            u'·', '').replace(u'ô', 'o'), '').replace(':', ' ').replace('-', ' ')
        for words in range(len(titulo.split())):
            cadena = cadena.replace(titulo.split()[words].lower(), '')
        if re.findall("^vol\.", cadena.lower().replace(elemento[0].lower().replace(u'·', ''), '').replace(' ', '')) or re.findall("^vol", cadena.lower().replace(elemento[0].lower().replace(u'·', ''), '').replace(' ', '')):
            cadena = cadena.replace('vol.', '').replace('vol', '')
            # print(cadena.lower().replace(elemento[0].lower().replace(u'·',''),'').replace(' ', '').replace('vol.', ''))
        elif re.findall("^\.", cadena.lower().replace(elemento[0].lower().replace(u'·', ''), '').replace(' ', '')) or re.findall("\.$", cadena.lower().replace(elemento[0].lower().replace(u'·', ''), '').replace(' ', '')):
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
            historeturn = historial(history, issue, dic)
            # print(historeturn)
            if historeturn == True:
                # print('pasa por aqui') 
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
            if historeturn == False:
                try:
                    shutil.rmtree(finalpath)
                except:
                    print('Error while deleting directory')
                mensaj2.append(
                    finalpath + " El Issue existe con el proveedor correcto \n\n")
            if historeturn == 'update':
                generatexml(dic, finalpath, issue)
                cbz = '/media/cristian/Datos/Comics/Tachiyomi/Updates/' + dic['name'] + issue + ".cbz"
                eliminado = dic['destino'] + "/" + dic['name'] + issue + ".cbz"
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
                try:
                    os.remove(eliminado)
                except:
                    print('Error eliminado el archivo')
                mensaj2.append(dic['name'] + issue + " eliminado para su futura actualizacion \n\n")
        else:
            # mensaj2.append(
            #     finalpath + " Patron encontrado es: " + numero + "\n\n")
            try:
                shutil.move(
                    finalpath, "/media/cristian/Datos/Comics/Fallo/"+elemento[1])
            except:
                print('Error while moving directory')
            try:
                shutil.rmtree(finalpath)
            except:
                print('Error while deleting directory')

            mensaj2.append(
                finalpath + " Patron encontrado es: " + numero + "\n\n")

    if fecha != '':
        # print(fecha)
        historeturn = historial(history, fecha, dic)
        if historeturn == True:
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
        if historeturn == False:
            try:
                shutil.rmtree(finalpath)
            except:
                print('Error while deleting directory')
            mensaj2.append(
                finalpath + " El Issue existe con el proveedor correcto \n\n")
    tilde = False

def issueupdate(secrets, history, mangas):
    folder = '/media/cristian/Datos/Comics/Tachiyomi/Updates'
    mensaje = []
    mensaje2 = ''
    if len(os.listdir(folder)) != 0:
        updates = glob.glob(folder + '/**/*.[cC][bB][zZ]', recursive=True)
        for issues in updates:
            fichero = os.path.split(issues)
            filename = os.path.splitext(fichero[1])
            issue = filename[0].split("#")
            name = issue[0] + '#'
            for key in mangas:
                if mangas[key]['name'] == name:
                    historial(history, issue[-1], mangas[key])
                    destino = str(mangas[key]['destino']) + '/' + str(fichero[1])                    
                    namefile = str(fichero[0]) + '/' + str(fichero[1])
                    shutil.move(namefile, destino)
                    mensaje.append(str(mangas[key]['name']) + str(issue[-1]) + "\n\n")
                    break
        with open('/config/history.json', 'w') as outfile:
            json.dump(history, outfile)
        send(mensaje, mensaje2, secrets['token'], secrets['chatid'])
        time.sleep(2)
        

def main():
    sys.excepthook = my_exception_hook
    mensaj = []
    mensaj2 = []
    excludes = ['/media/cristian/Datos/Comics/Tachiyomi/automatic', '/media/cristian/Datos/Comics/Tachiyomi/Manually', '/media/cristian/Datos/Comics/Tachiyomi/Updates' ,'/media/cristian/Datos/Comics/Tachiyomi/backup']

    with open('/config/mangas.json') as json_file:
        mangas = json.load(json_file)
    with open('/config/secrets.json') as json_file2:
        secrets = json.load(json_file2)
    with open('/config/history.json') as json_file3:
        history = json.load(json_file3)
    issueupdate(secrets, history, mangas)
    conect = "adb connect " + conexion(secrets) + ":5555"
    os.system(conect)
    time.sleep(5)
    os.system("adb pull /storage/emulated/0/Tachiyomi /media/cristian/Datos/Comics")
    path = "/media/cristian/Datos/Comics/Tachiyomi"
    dirs = os.listdir(path)
    dirs.sort()
    for file1 in dirs:
        path2 = path + "/" + file1
        if path2 not in excludes:
            if os.path.isdir(path2):
                files = os.listdir(path2)
                for file2 in files:
                    path3 = path2 + "/" + file2
                    # print(path3)
                    if path3 in mangas:
                        if path3 not in excludes:
                            if os.path.isdir(path3):
                                files2 = os.listdir(path3)
                                for file3 in files2:
                                    path4 = path3 + "/" + file3
                                    organizer([file2, file3], mangas[path3],
                                            path4, mensaj, mensaj2, history)
                    else:
                        shutil.move(path3, '/media/cristian/Datos/Comics/Tachiyomi/Manually')
                        mensaj2.append(
                            path3 + " El Manga no existe en la biblioteca y se ha movido a la carpeta Manually \n\n")
    os.system(
        'adb shell "find /storage/emulated/0/Tachiyomi/ -type d -mindepth 3 -exec rm -rf "{}" \;"')
    with open('/config/history.json', 'w') as outfile:
        json.dump(history, outfile)
    send(mensaj, mensaj2, secrets['token'], secrets['chatid'])


if __name__ == "__main__":
    main()
