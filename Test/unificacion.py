import json
import requests
import patoolib
import os
import re
import shutil
import xml.etree.cElementTree as ET
from os.path import basename
from zipfile import ZipFile
import time
from subprocess import Popen, PIPE, call
import telegram
# from MangaExporter import send, isfloat, isint, generatexml, organizer, historial


def inicializar(manga):
    os.makedirs(manga["destino"])
    url = "https://kitsu.io/api/edge/manga?filter[slug]=" + manga['slug']
    response = requests.get(url)
    data = response.json()
    image = requests.get(data["data"][0]["attributes"]["posterImage"]["large"])
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)


def poster(manga):
    url = "https://kitsu.io/api/edge/manga?filter[slug]=" + manga['slug']
    response = requests.get(url)
    data = response.json()
    image = requests.get(data["data"][0]["attributes"]["posterImage"]["large"])
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)

# def mover(manga, origen, filename):


def main():
    providers = ["NineMangaEn (EN)", "Mangakakalot (EN)", "Webtoons.com (EN)",
                 "MANGA Plus by SHUEISHA (EN)", "NineMangaEs (ES)", "MANGA Plus by SHUEISHA (ES)"]
    manga = {"/media/cristian/Datos/Comics/Reader/Webtoon/Tower of God (2010)(ES)": {
        "destino": "/media/cristian/Datos/Comics/Reader/Webtoon/Tower of God (2010)/",
        "name": "Tower of God (2010) Issue #",
        "funcion": "NineMangaEs (ES)",
        "provider" : "NineMangaEs (ES)",
        "slug":  "tower-of-god",
        "Series" : "Tower of God",
        "Volume" : "2010",
        "Publisher" : "Webtoon"
    },
    "/media/cristian/Datos/Comics/Reader/Webtoon/Tower of God (2010)(EN)": {
        "destino": "/media/cristian/Datos/Comics/Reader/Webtoon/Tower of God (2010)",
        "name": "Tower of God (2010) Issue #",
        "funcion": "NineMangaEs (ES)",
        "provider" : "Webtoons.com (EN)",
        "slug":  "tower-of-god",
        "Series" : "Tower of God",
        "Volume" : "2010",
        "Publisher" : "Webtoon"
    }
    }

    mensaj = []
    mensaj2 = []
    with open('/opt/tachiyomimangaexporter/secrets.json') as json_file2:
        secrets = json.load(json_file2)
    with open('/opt/tachiyomimangaexporter/history.json') as json_file3:
        history = json.load(json_file3)

    for contador in (range(len(providers))):
        for key in manga:
            if manga[key]['provider'] == providers[contador]:
                mensaj = []
                mensaj2 = []
                if not os.path.exists(manga[key]["destino"]):
                    inicializar(manga[key])
                if not os.path.exists(manga[key]["destino"] + '/poster.jpg'):
                    poster(manga[key])
                file2 = manga[key]["Series"]
                path3 = key
                files2 = os.listdir(path3)
                for file3 in files2:
                    if file3 != 'poster.jpg':
                        path4 = path3 + "/" + file3
                        filename = os.path.splitext(file3)
                        temporal = path3 + "/" + filename[0]
                        try:
                            os.mkdir(temporal)
                        except OSError:
                            print("Creation of the directory %s failed" % temporal)
                        try:
                            patoolib.extract_archive(path4, outdir=temporal)
                        except Exception:
                            pass

                        # organizer([file2, filename[0]], manga[path3],
                        #         temporal, mensaj, mensaj2, history)

                    # mover(manga[key],path4,file3)
                with open('/opt/tachiyomimangaexporter/history.json', 'w') as outfile:
                    json.dump(history, outfile)
                # send(mensaj, mensaj2, secrets['token'], secrets['chatid'])
                try:
                    shutil.rmtree(path3)
                except:
                    print('Error while deleting directory')


if __name__ == "__main__":
    main()
