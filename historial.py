import json
import os
import requests
from MangaExporter import posterm, posterc, historial



def main():
    # mensaj = []
    # mensaj2 = []
    issues = []
    popindex = []
    # guardados = ["Tower of God", "Hunter X Hunter", "Platinum End", "Blue Exorcist", "Vigilante My hero Academia Illegals", "Mashle", "Jujutsu Kaisen", "Baby Steps", "Black Clover", "Gokushufudou", "Dr Stone", "One Piece", "My Hero Academia", "The Gamer", "Spy X Family", "Boruto", "Dragon Ball Super", "Dungeon Meshi",  "Hajime no Ippo", "Chainsaw Man"]

    with open('/opt/tachiyomimangaexporter/mangas.json') as json_file:
        mangas = json.load(json_file)
    # with open('/opt/tachiyomimangaexporter/secrets.json') as json_file2:
    #     secrets = json.load(json_file2)
    with open('/opt/tachiyomimangaexporter/history.json') as json_file3:
        history = json.load(json_file3)

    for key in mangas:
        if mangas[key]["slug"] != "undefined":
            if not os.path.exists(mangas[key]["destino"] + '/poster.jpg'):
                if mangas[key]["Publisher"] == "DC Comics" or mangas[key]["Publisher"] == "Marvel":
                    posterc(mangas[key])
                else:
                    posterm(mangas[key])
        files = os.listdir(mangas[key]["destino"])
        issues = []
        for file1 in files:            
            if file1 != 'poster.jpg':
                filename = os.path.splitext(file1)
                issue = filename[0].split("#")
                # if mangas[key]["Series"] not in history:
                historial(history, issue[-1], mangas[key])
                issues.append(issue[-1])
        # print(mangas[key]["Series"], issues)
        # popindex = []
        # for numero in history[mangas[key]["Series"]]:
        #     if numero not in issues:
        #         popindex.append(numero)
        # for i in range(len(popindex)):
        #     print(popindex[i])
        #     history[mangas[key]["Series"]].pop(popindex[i], None)
        with open('/opt/tachiyomimangaexporter/history.json', 'w') as outfile:
            json.dump(history, outfile)
    


if __name__ == "__main__":
    main()