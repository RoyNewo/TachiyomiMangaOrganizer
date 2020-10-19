import os
from zipfile import ZipFile
# from unrar import rarfile
from os.path import basename
import re
import json
import shutil
import xml.etree.cElementTree as ET


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


def ultimo(dic, finalpath, namefile, comprimido, ruta):
    # print("Creara el cbz con el nombre de la carpeta")
    # print(dic['destino'])
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", namefile)
    if numbers:
        if isint(numbers[-1]):
            numero = '{:0>4}'.format(numbers[-1])
        else:
            if isfloat(numbers[-1]):
                numero = '{:0>6}'.format(numbers[-1])
    generatexml(dic, finalpath, numero)
    cbz = dic['destino'] + "/" + dic['name'] + numero + ".cbz"
    archivos = os.listdir(finalpath)
    archivos.sort()
    zipobje = ZipFile(cbz, 'w')
    for archivos2 in archivos:
        finalpath2 = finalpath + "/" + archivos2
        zipobje.write(finalpath2, basename(archivos2))
    zipobje.close()
    try:
        shutil.rmtree(finalpath)
        finalfilepath = ruta + "/" + comprimido
        os.remove(finalfilepath)
    except:
        print('Error while deleting directory')


def main():
    path = "/media/cristian/Datos/Comics/Buffer/Originales"
    manga = { "destino": "/media/cristian/Datos/Comics/Reader/Shueisha/One Piece (1997)(NM)",
        "name": "One Piece (1997)(NM) Issue #",
        "funcion": "primero",
        "Series" : "One Piece (NM)",
        "Volume" : "1997",
        "Publisher" : "Shueisha"}
    files = os.listdir(path)
    for ficheros in files:
        filename, file_extension = os.path.splitext(ficheros)
        finalpath = path + "/" + ficheros
        extractfolder = path + "/" + filename
        os.mkdir(extractfolder)
        print(finalpath)
        with ZipFile(finalpath, 'r') as zipObj:
            for member in zipObj.namelist():
                nombrearchivo = os.path.basename(member)
                if not nombrearchivo:
                    continue
                source = zipObj.open(member)
                target = open(os.path.join(extractfolder, nombrearchivo), "wb")
                with source, target:
                    shutil.copyfileobj(source, target)
        ultimo(manga, extractfolder, filename, ficheros, path)


if __name__ == "__main__":
    main()
