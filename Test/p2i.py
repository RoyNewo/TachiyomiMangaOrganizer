from pdf2image import convert_from_path

# from pdf2image.exceptions import (
#  PDFInfoNotInstalledError,
#  PDFPageCountError,
#  PDFSyntaxError
# )

images = convert_from_path('/media/cristian/Datos/Comics/Tachiyomi/Manually/Hollow_Knight_-_Comic_First_Chapter_Quirrel.pdf')

for i, image in enumerate(images):
    fname = "/media/cristian/Datos/Comics/Tachiyomi/Manually/Hollow Knight/Chapter 01 Quirrel/" + '{:0>3}'.format(i) + ".png"
    image.save(fname, "PNG")