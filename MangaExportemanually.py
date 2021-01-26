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
    manga = {"destino": "/media/cristian/Datos/Comics/Reader/Shueisha/Undead plus Unluck (2020)",
        "name": "Undead plus Unluck (2020) Issue #",
        "funcion": "MANGA Plus by SHUEISHA (ES)",
        "provider" : "NineMangaEs (ES)",
        "slug":  "undead-unluck",
        "Series" : "Undead plus Unluck",
        "Volume" : "2020",
        "Publisher" : "Shueisha"}
    mensaj = []
    mensaj2 = []
    with open('/opt/tachiyomimangaexporter/secrets.json') as json_file2:
        secrets = json.load(json_file2)
    with open('/opt/tachiyomimangaexporter/history.json') as json_file3:
        history = json.load(json_file3)
    if not os.path.exists(manga["destino"]):
        inicializar(manga)
    file2 = manga["Series"]
    path3 = "/media/cristian/Datos/Comics/Tachiyomi/Manually/Undead Unluck"
    files2 = os.listdir(path3)
    for file3 in files2:
        path4 = path3 + "/" + file3
        organizer([file2, file3], manga,
                  path4, mensaj, mensaj2, history)
    with open('/opt/tachiyomimangaexporter/history.json', 'w') as outfile:
        json.dump(history, outfile)
    send(mensaj, mensaj2, secrets['token'], secrets['chatid'])
    try:
        shutil.rmtree(path3)
    except:
        print('Error while deleting directory')



if __name__ == "__main__":
    main()
