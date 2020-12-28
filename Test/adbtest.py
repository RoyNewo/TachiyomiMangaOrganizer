import os

os.system("adb connect 192.168.1.166:5555")
os.system("adb pull /storage/emulated/0/Tachiyomi /media/cristian/Datos/Comics")
os.system('adb shell "find /storage/emulated/0/Tachiyomi/ -type d -mindepth 3 -exec rm -rf "{}" \;"')