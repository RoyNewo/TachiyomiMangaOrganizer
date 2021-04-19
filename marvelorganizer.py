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
    if os.path.exists(temporal):
        try:
            shutil.rmtree(temporal)
        except:
            print('Error while deleting directory')
    try:
        os.mkdir(temporal)
    except OSError:
        print ("Creation of the directory %s failed" % temporal)

    patoolib.extract_archive(namefile, outdir=temporal)
    comicinfo = temporal + '/ComicInfo.xml'
    with open(comicinfo,"r") as xml_obj:
        #coverting the xml data to Python dictionary
        my_dict = xmltodict.parse(xml_obj.read())
        #closing the file
    xml_obj.close()

    print(my_dict['ComicInfo']['Series'])
    destino = '/media/cristian/Datos/Comics/Reader/' + my_dict['ComicInfo']['Publisher'] + '/' + my_dict['ComicInfo']['Series'] + ' (' + my_dict['ComicInfo']['Volume'] + ')'
    # destino = '/media/cristian/Datos/Comics/Marvel/' + my_dict['ComicInfo']['Publisher'] + '/' + my_dict['ComicInfo']['Series'] + ' (' + my_dict['ComicInfo']['Volume'] + ')'
    destino = destino.replace(':', '')
    destino = destino.replace('\\', ' ')
    destino = destino.replace('?', '')
    print(destino)
    if not os.path.exists(destino):
        os.makedirs(destino)
    if not os.path.exists(destino + '/poster.jpg'):
        if my_dict['ComicInfo']['Publisher'] == 'Marvel' or my_dict['ComicInfo']['Publisher'] == 'Delcourt' or my_dict['ComicInfo']['Publisher'] == 'DC Comics':
            web = my_dict['ComicInfo']['Web']
            issueid = web.split("/")[-2:][0]
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            url = "https://comicvine.gamespot.com/api/issue/"+ issueid +"/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
            responseissue = requests.get(url, headers=headers)
            dataissue = responseissue.json()
            # webvolume = requests.get(dataissue["results"]["volume"]["api_detail_url"])
            url = dataissue["results"]["volume"]["api_detail_url"] + "?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
            responsevolume = requests.get(url, headers=headers)
            # print(url, response)
            datavolume = responsevolume.json()
            image = requests.get(datavolume["results"]["image"]["super_url"])
            imagesave = str(destino + "/poster.jpg")
            with open(imagesave, "wb") as f:
                f.write(image.content)
    archivos = glob.glob(temporal + '/**/*.*', recursive=True)
    archivos.sort()

    cbz = destino + '/' + my_dict['ComicInfo']['Series'] + ' (' + my_dict['ComicInfo']['Volume'] + ') Issue #' + '{:0>4}'.format(my_dict['ComicInfo']['Number']) + '.cbz'
    cbz = cbz.replace(':', '')
    cbz = cbz.replace('\\', ' ')
    cbz = cbz.replace('?', '')
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
    path = "/media/cristian/Datos/Downloads/Comics"
    files2 = glob.glob(path + '/**/*.[cC][bB][zZ]', recursive=True)
    for ficheros2 in files2:
        cbzgenerator(ficheros2)

if __name__ == "__main__":
    main()

