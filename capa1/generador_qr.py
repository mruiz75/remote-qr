#!/usr/bin/python
from capa1.generador_trama import crear_trama
import qrcode
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mp_img

from PIL import Image
from bitstring import BitArray
from matplotlib.pyplot import imshow

VERSION_PROTOCOLO = 1

def file_a_qr():
    pass

def texto_a_qr(texto):
    lista_tramas = []
    max_len = 111
    id1 = 0
    ip_salida = "192.168.0.1"
    ip_final = "199.123.2.1"
    mac1 = "F8:FF:FF:FF:FF:FF"

    while(len(texto) > 0):
        len_texto = len(texto)
        if(len_texto < 111):
            max_len = len_texto

        subtexto = texto[0:max_len]
        trama = crear_trama(version=VERSION_PROTOCOLO,
                            id=id1,
                            ip0=ip_salida,
                            ipf=ip_final,
                            mac=mac1,
                            payload=subtexto)
        lista_tramas.append(trama)
        id1 += 1
        texto = texto[max_len:]

    qr(lista_tramas)
    return

def qr(tramas):

    for i in range(len(tramas)):
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
        plt.pause(3)
        plt.close()

