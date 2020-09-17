import os
from zipfile import ZipFile
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


def completo(dic, finalpath, namefile):
    print("Creara el cbz con el nombre de la carpeta")
    print(dic['destino'])
    cbz = dic['destino'] + "/" + namefile + ".cbz"
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


def ultimo(dic, finalpath, namefile):
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
    except:
        print('Error while deleting directory')

def primero(dic, finalpath, namefile):
    # print("Creara el cbz con el nombre de la carpeta")
    # print(dic['destino'])
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", namefile)
    if numbers:
        if isint(numbers[0]):
            numero = '{:0>4}'.format(numbers[0])
        else:
            if isfloat(numbers[0]):
                numero = '{:0>6}'.format(numbers[0])
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
    except:
        print('Error while deleting directory')


def main():
    with open('/home/cristian/Github/MangaExporter/mangas.json') as json_file:
        mangas = json.load(json_file)
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
                    if os.path.isdir(path3):
                        files2 = os.listdir(path3)
                        for file3 in files2:
                            path4 = path3 + "/" + file3
                            try:
                                destino = (mangas[path3]['destino'])
                                if mangas[path3]['funcion'] == "completo":
                                    completo(mangas[path3], path4, file3)
                                if mangas[path3]['funcion'] == "ultimo":
                                    print(destino)
                                    print(file3)
                                    ultimo(mangas[path3], path4, file3)
                                if mangas[path3]['funcion'] == "primero":
                                    print(destino)
                                    print(file3)
                                    primero(mangas[path3], path4, file3)
                            except Exception as e:
                                print(e)
                                error = str(e)[1: 69]
                                print(mangas[error]['destino'])
                                if mangas[error]['funcion'] == "completo":
                                    completo(mangas[error], path4, file3)
                                if mangas[error]['funcion'] == "ultimo":
                                    print(destino)
                                    print(file3)
                                    ultimo(mangas[error], path4, file3)
                                if mangas[error]['funcion'] == "primero":
                                    print(destino)
                                    print(file3)
                                    primero(mangas[error], path4, file3)

    # with open("/home/cristian/Github/MangaExporter/mangas2.json", "w") as outfile:
    #     json.dump(mangas2, outfile)


if __name__ == "__main__":
    main()
