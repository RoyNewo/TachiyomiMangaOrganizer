import os
from os.path import basename
import glob
from zipfile import ZipFile
import shutil

def main():
    path = '/media/cristian/Datos/Comics/Marvel/comictagger/Guia de Lectura Marvel Vol 4/01 Thor Ragnarok/Thor #71-74'
    directorios=os.listdir(path)
    for dir in directorios:
        path2 = path + '/' + dir
        archivos = glob.glob(path2 + '/**/*.*', recursive=True)
        archivos.sort()
        cbz = path + '/' + dir + '.cbz'
        zipobje = ZipFile(cbz, 'w')
        for archivos2 in archivos:
            nombrearchivo = os.path.split(archivos2)
            zipobje.write(archivos2, basename(nombrearchivo[1]))
        zipobje.close()
        try:
            shutil.rmtree(path2)
        except:
            print('Error while deleting directory')


if __name__ == "__main__":
    main()