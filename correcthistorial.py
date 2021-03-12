import json
from MangaExporter import isint, isfloat


with open('/opt/tachiyomimangaexporter/history.json') as json_file3:
    history = json.load(json_file3)

for key in history['Gokushufudou']:
    if isint(key):
        if int(key) > 61:
             history['Gokushufudou'].update({key : "NineMangaEn (EN)"})
    if isfloat(key):
        if float(key) > 61:
             history['Gokushufudou'].update({key : "NineMangaEn (EN)"})

with open('/opt/tachiyomimangaexporter/history.json', 'w') as outfile:
        json.dump(history, outfile)

