import json
import requests
import os
import re
import shutil
import xml.etree.cElementTree as ET
from os.path import basename
from zipfile import ZipFile
import time
from subprocess import Popen, PIPE, call
import telegram
from MangaExporter import send, isfloat, isint, generatexml, organizer

def inicializar(manga):
    os.makedirs(manga["destino"])
    url = "https://kitsu.io/api/edge/manga?filter[slug]=" + manga['slug']
    response = requests.get(url)
    data = response.json()
    image = requests.get(data["data"][0]["attributes"]["posterImage"]["large"])
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)


def main():
    manga = {"destino": "/media/cristian/Datos/Comics/Reader/Shonen Ace/Cloverfield Kishin (2008)",
             "name": "Cloverfield Kishin (2008) Issue #",
             "funcion": "primero",
             "Series": "Cloverfield Kishin",
             "Volume": "2008",
             "Publisher": "Shonen Ace",
             "slug": "cloverfield-kishin"}
    mensaj = []
    mensaj2 = []
    with open('/home/cristian/Github/TachiyomiMangaOrganizer/secrets.json') as json_file2:
        secrets = json.load(json_file2)
    if not os.path.exists(manga["destino"]):
        inicializar(manga)
    file2 = manga["Series"]
    path3 = "/media/cristian/Datos/Comics/Tachiyomi/Manually/cloverfield-kishin"
    files2 = os.listdir(path3)
    for file3 in files2:
        path4 = path3 + "/" + file3
        organizer([file2, file3], manga,
                  path4, mensaj, mensaj2)
    send(mensaj, mensaj2, secrets['token'], secrets['chatid'])
    try:
        shutil.rmtree(path3)
    except:
        print('Error while deleting directory')


if __name__ == "__main__":
    main()
