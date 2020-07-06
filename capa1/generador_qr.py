#!/usr/bin/python

from capa1.generador_trama import crear_trama
import sys
import qrcode
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mp_img

from PIL import Image
from bitstring import BitArray
from matplotlib.pyplot import imshow


def file_a_qr(version, ip, mac, filename):
    with open(filename, "rb") as file:
        data = file.read()

    texto_a_qr(version, ip, mac, data)


def texto_a_qr(version, ip, mac, texto):
    lista_tramas = []
    cont = "0"
    if isinstance(texto, str):
        texto = texto.encode()

    while(len(texto) > 0):
        trama, subtexto = crear_trama(version=version,
                            cont=cont,
                            ip=ip,
                            mac=mac,
                            payload=texto)
        lista_tramas.append(trama)
        cont = str(int(cont) + 1)
        texto = subtexto

        if len(texto) == 0:
            trama, subtexto = crear_trama(version=version,
                                          cont="F",
                                          ip=ip,
                                          mac=mac,
                                          payload=" ".encode())
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
        name = "qr{}.png".format(i)
        img.save(name)

        unformatted_qr_image = Image.open(name).convert("L")
        qr_image = np.asarray(unformatted_qr_image)

        plt.imshow(qr_image, cmap='gray', vmin=0, vmax=255)
        plt.draw()
        plt.pause(0.2)
        plt.close()

