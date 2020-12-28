import requests
from bs4 import BeautifulSoup
import os
import xmltodict
import pprint
import json


def vosque(url):
    path = ''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup)
    imgholder = soup.findAll("div", {"class": "img_holder"})
    navigationcontent = soup.findAll("h4", {"class": "navigation_subtitle"})

    print(imgholder)
    for tag in imgholder[0]:
        try:
            imagen = str(tag['src'].encode('utf-8'))
            noimage = True
        except:
            noimage = False

    print(navigationcontent)
    for tag in navigationcontent[0]:
        # print(tag)
        tag2 = str(tag.encode('utf-8'))
        # tag2 = tag2.strip("\t\t")
        tag2 = tag2.strip("\n")
        tag2 = tag2.strip("\t")
        serie = tag2
    if noimage:
        archivo = str(imagen).split('/')
        extension = archivo[-1].split('.')
        # print(extension[1])
        response = requests.get(imagen)
        numero = ''
        nombre = path + '/' + numero + ' ' + serie + \
            ' Issue #' + numero + '.' + extension[1]
        # nombre = path + '/' + numero + ' ' + 'CSI El Vosque' + ' Issue #' + numero + '.' + extension[1]
        print(nombre)
        file = open(nombre, "wb")
        file.write(response.content)
        file.close()


def vosque2(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    # print(soup)
    imgholder = soup.findAll("div", {"class": "img_holder"})
    navigationcontent = soup.findAll("h4", {"class": "navigation_subtitle"})



    # print(imgholder)
    for tag in imgholder[0]:
        try:
            imagen = str(tag['src'].encode('utf-8'))
            noimage = True
        except:
            noimage = False

    # print(navigationcontent)
    for tag in navigationcontent[0]:
        # print(tag)
        tag2 = str(tag.encode('utf-8'))
        # tag2 = tag2.strip("\t\t")
        tag2 = tag2.strip("\n")
        tag2 = tag2.strip("\t")        
        serie = tag2
    
    print(imagen, serie.decode('utf-8'))
    
def main():
    # path = '/media/cristian/Datos/Comics/Buffer/El Vosque/XML'
    xml = 'http://elvosque.es/rss.php'
    elvosque = ''
    # os.makedirs(path)


    xmlrequest = requests.get(xml)
    xmldic = xmltodict.parse(str(xmlrequest.text.encode('utf-8')))
    # print(str(xmlrequest.text.encode('utf-8')))
    # print(xmldic)
    # print(xmldic[u'rss'][u'channel'])
    for items in range(len(xmldic[u'rss'][u'channel'][u'item'])):
        print(str(xmldic[u'rss'][u'channel'][u'item'][items][u'title'].encode('utf-8')))
        vosque2(xmldic[u'rss'][u'channel'][u'item'][items][u'link'])
        # print(xmldic[u'rss'][u'channel'][u'item'][items][u'link'])

        




if __name__ == "__main__":
    main()
