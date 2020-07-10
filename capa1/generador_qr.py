#!/usr/bin/python

from capa1.generador_trama import crear_trama
import sys
import qrcode
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mp_img
import os

from PIL import Image
from bitstring import BitArray
from matplotlib.pyplot import imshow

#recibe ints
def file_a_qr(version, mac, filename):
    with open(filename, "rb") as file:
        hexdata = file.read().hex()

    texto_a_qr(version, mac, hexdata)


def texto_a_qr(version, mac, texto_hex):
    lista_tramas = []
    cont = 0

    while(len(texto_hex) > 0):
        trama, subtexto = crear_trama(version=version,
                            cont=cont,
                            mac=mac,
                            payload=texto_hex)
        lista_tramas.append(trama)
        cont = int(cont) + 1
        texto_hex = subtexto

        if len(texto_hex) == 0:
            trama, subtexto = crear_trama(version=0,
                                          cont=cont,
                                          mac=mac,
                                          payload=" ")
            lista_tramas.append(trama)

    qr(lista_tramas)
    return


def qr(tramas):

    for i in range(len(tramas)):
        # print(sys.getsizeof(tramas[i]))
        qr = qrcode.QRCode(
            version = 1,
            box_size = 15,
            border = 5,
        )

        qr.add_data(tramas[i])
        qr.make(fit = True)

        img = qr.make_image()

        try:
            directorio_actual = os.getcwd()
            directorio_final = os.path.join(directorio_actual, r'tempfolder')
            if not os.path.exists(directorio_final):
                os.makedirs(directorio_final)
        except OSError:
            print("Creation of the directory %s failed" % path)

        name = generar_nombre_archivo(i)
        img.save(name)

        unformatted_qr_image = Image.open(name).convert("L")
        qr_image = np.asarray(unformatted_qr_image)

        plt.imshow(qr_image, cmap='gray', vmin=0, vmax=255)
        plt.draw()
        plt.pause(0.1)
        plt.close()


def generar_nombre_archivo(cont):
    nombre = "tempfolder/qr"
    ceros = 10 - len(str(cont))
    nombre = nombre + "0"*ceros + str(cont) + ".png"
    return nombre