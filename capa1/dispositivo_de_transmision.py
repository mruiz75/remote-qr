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

class DispositivoDeTransmision:

    def __init__(self):
        pass

    # recibe ints
    def file_a_qr(self, version, mac, filename):
        with open(filename, "rb") as file:
            hexdata = file.read().hex()

        self.texto_a_qr(version, mac, hexdata)


    def texto_a_qr(self, version, mac, texto_hex):
        lista_tramas = []
        cont = 0

        while len(texto_hex) > 0:
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

        self.crear_qr(lista_tramas)
        return


    def crear_qr(self, tramas):
        for i in range(len(tramas)):
            # print(sys.getsizeof(tramas[i]))
            qr = qrcode.QRCode(
                version=1,
                box_size=15,
                border=5,
            )

            qr.add_data(tramas[i])
            qr.make(fit=True)

            img = qr.make_image()

            try:
                directorio_actual = os.getcwd()
                directorio_final = os.path.join(directorio_actual, r'tempfolder')
                if not os.path.exists(directorio_final):
                    os.makedirs(directorio_final)
            except OSError:
                print("Error en la creación del directorio %s" % directorio_final)

            name = self.generar_nombre_archivo(i)
            img.save(name)

            unformatted_qr_image = Image.open(name).convert("L")
            qr_image = np.asarray(unformatted_qr_image)

            plt.imshow(qr_image, cmap='gray', vmin=0, vmax=255)
            plt.draw()
            plt.pause(0.1)
            plt.close()

        return


    def generar_nombre_archivo(self, cont):
        nombre = "tempfolder/qr"
        ceros = 10 - len(str(cont))
        nombre = nombre + "0" * ceros + str(cont) + ".png"
        return nombre
