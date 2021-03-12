import patoolib
import os
from os.path import basename
import json
import shutil
import glob
from zipfile import ZipFile
import xmltodict
import pprint
import requests

def cbzgenerator(namefile):
    parents, filename = os.path.split(namefile)
    temporal = parents + '/temporal'
    try:
        os.mkdir(temporal)
    except OSError:
        print ("Creation of the directory %s failed" % temporal)

    patoolib.extract_archive(namefile, outdir=temporal)
    # os.rename(namefile, namefile + ".extraido")
    comicinfo = temporal + '/ComicInfo.xml'
    with open(comicinfo,"r") as xml_obj:
        #coverting the xml data to Python dictionary
        my_dict = xmltodict.parse(xml_obj.read())
        #closing the file
    xml_obj.close()

    # print(json.dumps(my_dict))
    print(my_dict['ComicInfo']['Series'])
    destino = '/media/cristian/Datos/Comics/Reader/' + my_dict['ComicInfo']['Publisher'] + '/' + my_dict['ComicInfo']['Series'] + ' (' + my_dict['ComicInfo']['Volume'] + ')'
    destino = destino.replace(':', '')
    print(destino)
    if not os.path.exists(destino):
        os.makedirs(destino)
    if not os.path.exists(destino + '/poster.jpg'):
        # print(manga["Series"])
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
        url = "https://comicvine.gamespot.com/api/volume/4050-51110/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
        response = requests.get(url, headers=headers)
        print(url, response)
        data = response.json()
        image = requests.get(data["results"]["image"]["super_url"])
        imagesave = str(destino + "/poster.jpg")
        with open(imagesave, "wb") as f:
            f.write(image.content)
    archivos = glob.glob(temporal + '/**/*.*', recursive=True)
    archivos.sort()

    # filename2, file_extension = os.path.splitext(filename)
    cbz = destino + '/' + my_dict['ComicInfo']['Series'] + ' (' + my_dict['ComicInfo']['Volume'] + ') Issue #' + '{:0>4}'.format(my_dict['ComicInfo']['Number']) + '.cbz'
    cbz = cbz.replace(':', '')
    zipobje = ZipFile(cbz, 'w')
    for archivos2 in archivos:
        ruta, nombrearchivo = os.path.split(archivos2)
        zipobje.write(archivos2, basename(nombrearchivo))
    zipobje.close()
    try:
        shutil.rmtree(temporal)
    except:
        print('Error while deleting directory')

def main():
    path = "/media/cristian/Datos/Downloads/Comics/Scott Pilgrim (1-6) Color Edition (2012-2015) GetComics.INFO"
    # path = "/media/cristian/Datos/Comics/Buffer/cbr"

    # files = glob.glob(path + '/**/*.[cC][bB][rR]', recursive=True)
    files2 = glob.glob(path + '/**/*.[cC][bB][zZ]', recursive=True)
    # print(files)
    # print(files2)
    # for ficheros in files:
    #     parents, filename = os.path.split(ficheros)
    # for ficheros in files:
    #     cbzgenerator(ficheros)
    for ficheros2 in files2:
        cbzgenerator(ficheros2)

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