import patoolib
import os
from os.path import basename
import re
import json
import shutil
import xml.etree.cElementTree as ET
import glob
from zipfile import ZipFile
from modifieddate import datemodified

def cbzgenerator(namefile, origen):
    logfile = origen + '/cbrconverter.log'
    parents, filename = os.path.split(namefile)
    temporal = parents + '/temporal'
    try:
        os.mkdir(temporal)
    except OSError:
        print ("Creation of the directory %s failed" % temporal)
    print(namefile)
    try:
        patoolib.extract_archive(namefile, outdir=temporal)
    except:
        f = open(logfile, "a")
        f.write("Error descomprimiendo: " + namefile + '\n')
        f.close()
        try:
            shutil.rmtree(temporal)
        except OSError:
            print('Error while deleting directory')
    os.rename(namefile, namefile + ".extraido")
    archivos = glob.glob(temporal + '/**/*.*', recursive=True)
    archivos.sort()

    filename2, file_extension = os.path.splitext(filename)
    cbz = parents + '/' + filename2 + '.cbz.new'
    zipobje = ZipFile(cbz, 'w')
    for archivos2 in archivos:
        datemodified(archivos2)
        ruta, nombrearchivo = os.path.split(archivos2)
        zipobje.write(archivos2, basename(nombrearchivo))
    zipobje.close()
    try:
        shutil.rmtree(temporal)
    except:
        print('Error while deleting directory')

def main():
    path = "/media/cristian/Datos/Comics/Marvel/comictagger"
    # path = "/media/cristian/Datos/Comics/Buffer/cbr"

    files = glob.glob(path + '/**/*.[cC][bB][rR]', recursive=True)
    files2 = glob.glob(path + '/**/*.[cC][bB][zZ]', recursive=True)
    # print(files)
    # print(files2)
    # for ficheros in files:
    #     parents, filename = os.path.split(ficheros)
    for ficheros in files:
        cbzgenerator(ficheros,path)
    for ficheros2 in files2:
        cbzgenerator(ficheros2,path)

if __name__ == "__main__":
    main()










#     temporal = path + "/temporal"
    # try:
    #     os.mkdir(temporal)
    # except OSError:
    #     print ("Creation of the directory %s failed" % temporal)
#     # filename, file_extension = os.path.splitext(ficheros)
#     filename = path + 





# patoolib.extract_archive("foo_bar.rar", outdir=)