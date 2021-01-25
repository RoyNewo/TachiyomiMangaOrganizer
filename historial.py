import json
import os
import requests



def posterm(manga):
    url = "https://kitsu.io/api/edge/manga?filter[slug]=" + manga['slug']
    response = requests.get(url)
    data = response.json()
    image = requests.get(data["data"][0]["attributes"]["posterImage"]["large"])
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)

def posterc(manga):
    print(manga["Series"])
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    url = "https://comicvine.gamespot.com/api/volume/" + manga['slug'] + "/?api_key=dcb22bb374f04e7217eaca81f2fcfffbe5062e42&format=json"
    response = requests.get(url, headers=headers)
    print(url, response)
    data = response.json()
    image = requests.get(data["results"]["image"]["super_url"])
    imagesave = str(manga["destino"] + "/poster.jpg")
    with open(imagesave, "wb") as f:
        f.write(image.content)

def historial(history, issue, dic):
    if dic["Series"] in history:
        if issue in history[dic["Series"]]:
            if dic["provider"] != history[dic["Series"]][issue]:
                if dic["funcion"] != history[dic["Series"]][issue]:
                    history[dic["Series"]].update({issue: dic["provider"]})
                    return True
                else:
                    return False
            else:
                return False
        else:
            history[dic["Series"]].update({issue: dic["provider"]})
            return True
    else:
        print(dic["Series"], issue, dic["provider"])
        history[dic["Series"]] = {issue: dic["provider"]}
        return True


def main():
    mensaj = []
    mensaj2 = []

    # guardados = ["Tower of God", "Hunter X Hunter", "Platinum End", "Blue Exorcist", "Vigilante My hero Academia Illegals", "Mashle", "Jujutsu Kaisen", "Baby Steps", "Black Clover", "Gokushufudou", "Dr Stone", "One Piece", "My Hero Academia", "The Gamer", "Spy X Family", "Boruto", "Dragon Ball Super", "Dungeon Meshi",  "Hajime no Ippo", "Chainsaw Man"]

    with open('/home/cristian/Github/TachiyomiMangaOrganizer/mangas.json') as json_file:
        mangas = json.load(json_file)
    with open('/home/cristian/Github/TachiyomiMangaOrganizer/secrets.json') as json_file2:
        secrets = json.load(json_file2)
    with open('/home/cristian/Github/TachiyomiMangaOrganizer/history.json') as json_file3:
        history = json.load(json_file3)

    for key in mangas:
        if mangas[key]["Series"] not in history:
            if mangas[key]["slug"] != "undefined":
                 if not os.path.exists(mangas[key]["destino"] + '/poster.jpg'):
                    if mangas[key]["Publisher"] == "DC Comics" or mangas[key]["Publisher"] == "Marvel":
                        posterc(mangas[key])
                    else:
                        posterm(mangas[key])
            files = os.listdir(mangas[key]["destino"])
            for file1 in files:
                if file1 != 'poster.jpg':
                    filename = os.path.splitext(file1)
                    issue = filename[0].split("#")
                    dummy = historial(history, issue[-1], mangas[key])
            with open('/home/cristian/Github/TachiyomiMangaOrganizer/history.json', 'w') as outfile:
                json.dump(history, outfile)
    


if __name__ == "__main__":
    main()