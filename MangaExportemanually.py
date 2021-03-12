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
from MangaExporter import send, isfloat, isint, generatexml, organizer, posterc, posterm

def main():
    manga = {"destino": "/media/cristian/Datos/Comics/Reader/Team Cherry/Hollow Knight Chapter One Quirrel (2017)",
        "name": "Hollow Knight Chapter One Quirrel (2017) Issue #",
        "funcion": "Team Cherry",
        "provider" : "Team Cherry",
        "slug":  "undefined",
        "Series" : "Hollow Knight Chapter One Quirrel",
        "Volume" : "2017",
        "Publisher" : "Team Cherry"}
    mensaj = []
    mensaj2 = []
    with open('/opt/tachiyomimangaexporter/secrets.json') as json_file2:
        secrets = json.load(json_file2)
    with open('/opt/tachiyomimangaexporter/history.json') as json_file3:
        history = json.load(json_file3)
    if not os.path.exists(manga["destino"]):
        os.makedirs(manga["destino"])
    if manga["slug"] != "undefined":
            if not os.path.exists(manga["destino"] + '/poster.jpg'):
                if manga["Publisher"] == "DC Comics" or manga["Publisher"] == "Marvel":
                    posterc(manga)
                else:
                    posterm(manga)
    file2 = manga["Series"]
    path3 = "/media/cristian/Datos/Comics/Tachiyomi/Manually/Hollow Knight"
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
