#!/usr/bin/python

from capa1.generador_trama import crear_trama
import qrcode
import numpy as np
import matplotlib.pyplot as plt
import os

from PIL import Image

"""
Dispositivo para generar los códigos QR a partir de un archivo o de un mensaje en forma de string
"""
class DispositivoDeTransmision:

    def __init__(self):
        pass

    """
    Metodo que abre un archivo como un arreglo de bytes en formato hexadecimal y hace el llamado a texto_a_qr para procesar la información
    @param version: indica si se transmite un archivo o un mensaje
    @param direccion: direccion del nodo donde se dirige el mensaje
    @param filename: ruta completa hasta el archivo por procesar
    """
    # recibe ints
    def file_a_qr(self, version, direccion, filename):
        with open(filename, "rb") as file:
            hexdata = file.read().hex()

        self.texto_a_qr(version, direccion, hexdata)

    """
    Metodo que toma la version, direccion y el payload en formato hexadecimal y genera multiples tramas que luego son convertidas en códigos QR.
    @param version:
    @param mac:
    @param texto_hex
    """
    def texto_a_qr(self, version, direccion, texto_hex):
        lista_tramas = []
        cont = 0

        while len(texto_hex) > 0:
            trama, subtexto = crear_trama(version=version,
                                          cont=cont,
                                          direccion=direccion,
                                          payload=texto_hex)
            lista_tramas.append(trama)
            cont = int(cont) + 1
            texto_hex = subtexto

            if len(texto_hex) == 0:
                trama, subtexto = crear_trama(version=0,
                                              cont=cont,
                                              direccion=direccion,
                                              payload=" ")
                lista_tramas.append(trama)

        self.crear_qr(lista_tramas)
        return

    """
    Método que toma la trama en formato de texto string y lo convierte en un código qr dando como resultado un archivo de tipo .png
    @param tramas: arreglo con las tramas en formato de texto hexadecimal.
    """
    def crear_qr(self, tramas):
        for i in range(len(tramas)):
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

    """
    Metodo que enera el nombre del archivo donde se almacenará el código qr
    @param cont: identificador de la trama
    """
    def generar_nombre_archivo(self, cont):
        nombre = "tempfolder/qr"
        ceros = 10 - len(str(cont))
        nombre = nombre + "0" * ceros + str(cont) + ".png"
        return nombre
