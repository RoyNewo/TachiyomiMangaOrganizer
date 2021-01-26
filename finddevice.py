# Este scrypt sera solo para mantener secrets json ponemos rutas para otras cosas importantes

import nmap3
import json
from ppadb.client import Client as AdbClient

def conectar(secret):
    nmap = nmap3.Nmap()
    results = nmap.scan_top_ports("192.168.1.0/24", args="-sP -n")
    conect = ''
    # print(json.dumps(results))
    for key in results:
        # print(key)
        if "macaddress" in results[key]:
            if results[key]["macaddress"] != None:
                if "addr" in results[key]["macaddress"]:
                    if results[key]["macaddress"]["addr"] == "B8:27:EB:95:9F:BD":
                        # print(key)
                        if key != secret['ip']:
                            secret['ip'] = key
                            with open('/opt/tachiyomimangaexporter/secrets.json', 'w') as outfile:
                                json.dump(secret, outfile)
                        conect = key
    if conect != '':
        return conect
    else:
        return None

        

# https://strm.sh/post/cron-tasks-inside-docker/
# https://github.com/opsxcq/tasker
# https://github.com/Swind/pure-python-adb
# https://dustinoprea.com/2018/12/05/use-adb-to-connect-to-your-android-device-from-a-docker-container/comment-page-1/
# apt-cache policy {package}
# sudo apt-get install <package name>=<version>
# https://pypi.org/project/python3-nmap/
# https://community.home-assistant.io/t/cant-get-nmap-to-work-inside-docker/83844/3
# docker run --network="host" -v /opt/tachiyomimangaexporter:/config -v /media/cristian/Datos/Comics:/media/cristian/Datos/Comics -i -t tachiyomimangaexporter:v.1.02 /bin/bash


def main():
    with open('/opt/tachiyomimangaexporter/secrets.json') as json_file2:
        secrets = json.load(json_file2)
    client = AdbClient(host="127.0.0.1", port=5037)
    # print(client.version())
    ip = conectar(secrets)
    client.remote_connect(ip, 5555)
    device = client.device( ip +":5555")
    device.pull("/storage/emulated/0/Tachiyomi", "/media/cristian/Datos/Comics/Tachiyomi")



if __name__ == "__main__":
    main()