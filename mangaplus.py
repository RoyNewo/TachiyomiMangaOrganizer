import requests
import json
import mloader
import telegram
import time

api_url = 'https://jumpg-webapi.tokyo-cdn.com/api/'

def nuevosmangas():
    todoslist = []
    with open('/opt/tachiyomimangaexporter/all.json') as json_file:
        todosdict = json.load(json_file)
    with open('/opt/tachiyomimangaexporter/secrets.json') as json_file2:
        secrets = json.load(json_file2)
    with open('/opt/tachiyomimangaexporter/mangasnuevos.json') as json_file2:
        mangasnuevos = json.load(json_file2)
    for manga in range(len(todosdict['success']['allTitlesView']['titles'])):
        todoslist.append({todosdict['success']['allTitlesView']['titles'][manga]['titleId']: todosdict['success']['allTitlesView']['titles'][manga]['name']})
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
    url = api_url + "title_list/all?format=json"
    responsemanga = requests.get(url, headers=headers)
    datamanga = responsemanga.json()
    
    for manga in range(len(datamanga['success']['allTitlesView']['titles'])):
        tempdict = {datamanga['success']['allTitlesView']['titles'][manga]['titleId']: datamanga['success']['allTitlesView']['titles'][manga]['name']}
        if tempdict not in todoslist:
            # print(json.dumps(datamanga['success']['allTitlesView']['titles'][manga]))
            if 'language' in datamanga['success']['allTitlesView']['titles'][manga]:
                source = "/media/cristian/Datos/Comics/Tachiyomi/MANGA Plus by SHUEISHA (ES)/" + datamanga['success']['allTitlesView']['titles'][manga]['name']
                funcion = "MANGA Plus by SHUEISHA (ES)"
                provider = "MANGA Plus by SHUEISHA (ES)"
            else:
                source = "/media/cristian/Datos/Comics/Tachiyomi/MANGA Plus by SHUEISHA (EN)/" + datamanga['success']['allTitlesView']['titles'][manga]['name']
                funcion = "MANGA Plus by SHUEISHA (EN)"
                provider = "MANGA Plus by SHUEISHA (EN)"
            output = "/media/cristian/Datos/Comics/Reader/Shueisha/" + datamanga['success']['allTitlesView']['titles'][manga]['name'] + " (2021)"
            name = datamanga['success']['allTitlesView']['titles'][manga]['name']
            series = datamanga['success']['allTitlesView']['titles'][manga]['name']
            mangaid = datamanga['success']['allTitlesView']['titles'][manga]['titleId']
            portrait = datamanga['success']['allTitlesView']['titles'][manga]['portraitImageUrl']

            mangasnuevos['nuevos'].append({
                source : {
                    "destino" : output,
                    "name" : name,
                    "funcion" : funcion,
                    "provider" : provider,
                    "slug" : "undefined",
                    "Series" :  series,
                    "Volume" : "2021",
                    "Publisher" : "Shueisha",
                    "mangaid" : mangaid,
                    "portrait" : portrait
                }
            })
            mensaje = "Se ha detectado un nuevo manga en la aplicacione MangaPlus\n\n"
            url = api_url + "title_detail?title_id=" + str(mangaid) + "&format=json"
            responsedetail = requests.get(url, headers=headers)
            datadetail = responsedetail.json()
            msg = 'Nombre: ' + datadetail['success']['titleDetailView']['title']['name'] + '\n\n'
            mensaje += msg
            msg = 'Autor: ' + datadetail['success']['titleDetailView']['title']['author'] + '\n\n'
            mensaje += msg
            msg = 'Descripcion: ' + datadetail['success']['titleDetailView']['overview'] + '\n\n'
            mensaje += msg
            if 'isSimulReleased' in datadetail['success']['titleDetailView']:
                mensaje += 'Simulrelease\n\n'
            else:
                mensaje += 'No Simulrelease\n\n'

            bot = telegram.Bot(token=secrets['token'])
            bot.sendMessage(chat_id=secrets['chatid'], text=mensaje)
            bot.send_photo(chat_id=secrets['chatid'], photo=portrait)
            time.sleep(2)
    with open('/opt/tachiyomimangaexporter/all.json', 'w') as outfile:
        json.dump(datamanga, outfile)
    with open('/opt/tachiyomimangaexporter/mangasnuevos.json', 'w') as outfile:
        json.dump(mangasnuevos, outfile)
    
def ultimosmangas():
    url = "https://jumpg-webapi.tokyo-cdn.com/api/web/web_home?lang=esp&format=json"
            






    

def main():
    nuevosmangas()
    ultimosmangas()
    


if __name__ == "__main__":
    main()

