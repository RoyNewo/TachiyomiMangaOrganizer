from pdf2image import convert_from_path

# from pdf2image.exceptions import (
#  PDFInfoNotInstalledError,
#  PDFPageCountError,
#  PDFSyntaxError
# )

images = convert_from_path('/media/cristian/Datos/Comics/Reader/Vault Comics/Dark One (2020)/Sanderson DARK ONE Ebook.pdf')

for i, image in enumerate(images):
    fname = "/media/cristian/Datos/Comics/Tachiyomi/Manually/Dark One/Dark One 01/" + '{:0>3}'.format(i) + ".png"
    image.save(fname, "PNG")