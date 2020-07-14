#!/usr/bin/python

import cv2
import pyzbar.pyzbar as pyzbar
import time
import glob
from capa1.generador_trama import calcular_checksum
from util.textos import *

"""
Dispotivo para la lectura de un archivo o un mensaje a través de una serie de imágenes de tipo .png
o bien a través de la cámara web de la computadora
"""
class DispositivoLuzAdaptador:

    DIRECCION_MAQUINA = 0

    def __init__(self, direccion):
        self.DIRECCION_MAQUINA = direccion
        self.textos = Textos()
        self.mostrar_direccion()

    """
    Lee los archivos .png a partir de una ruta a un directorio
    @param:path ruta al directorio donde se encuentran las imagenes
    """
    def leer_imagenes(self, path):
        lectura_limpia = True
        checksum_correcto = True
        mensaje = ""
        datos = {}
        cont = 0
        path = path + "/*.png"
        tipo_de_mensaje = 0

        try:
            images = [cv2.imread(file) for file in sorted(glob.glob(path))]   # lee todas las imagenes del path especificado

        except OSError:
            print(self.textos.ERROR_LECTURA_IMAGENES)
            return

        for img in images:
            decoded_obs = pyzbar.decode(img)
            datos = self.interpretar_data(decoded_obs[0].data)
            payload = datos["payload"]
            qr_id = datos["id"]
            tipo_de_mensaje = datos["version"]
            checksum = datos["checksum"]

            lectura_limpia = qr_id == cont
            cont += 1
            checksum_correcto = checksum == calcular_checksum(payload)
            mensaje += payload
            print(self.textos.QR_LEIDO)

        destino_correcto = self.verificar_direccion(datos["mac"])

        if not lectura_limpia:
            print(self.textos.MALA_LECTURA)
            time.sleep(2)
            return

        if not destino_correcto:
            print(self.textos.DIRECCION_INCORRECTO)
            time.sleep(2)
            return

        if not checksum_correcto:
            print(self.textos.CHECKSUM_INCORRECTO)
            time.sleep(2)
            return

        if tipo_de_mensaje == 1:
            self.crear_archivo(mensaje)

        elif tipo_de_mensaje == 2:
            print(mensaje)

        return

    """
    Lee los QR a partir de luz interpretada por la cámara web de la computadora
    """
    def leer_con_camara(self):
        lectura_limpia = True
        checksum_correcto = True
        leer = True
        mensaje = ""
        datos = {}
        id_anterior = -1
        tipo_de_mensaje = 0

        cap = cv2.VideoCapture(0)

        while leer:                     # mantiene el ciclo de lectura con cámara web
            _, frame = cap.read()

            decoded_objects = pyzbar.decode(frame)
            if decoded_objects:
                datos = self.interpretar_data(decoded_objects[0].data)
                if datos["version"] != 0 and checksum_correcto:
                    payload = datos["payload"]
                    qr_id = datos["id"]
                    tipo_de_mensaje = datos["version"]
                    checksum = datos["checksum"]

                    lectura_limpia = qr_id == (id_anterior + 1)
                    checksum_correcto = checksum == calcular_checksum(payload)

                    id_anterior += 1
                    mensaje += payload

                else:
                    leer = False

                print(self.textos.QR_LEIDO)
                time.sleep(3)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)

            if key == 27:
                break

        destino_correcto = self.verificar_direccion(datos["mac"])

        if not lectura_limpia:
            print(self.textos.MALA_LECTURA)
            return

        if not destino_correcto:
            print(self.textos.DIRECCION_INCORRECTO)
            return

        if not checksum_correcto:
            print(self.textos.CHECKSUM_INCORRECTO)
            return

        if tipo_de_mensaje == 1:
            self.crear_archivo(mensaje)
        elif tipo_de_mensaje == 2:
            print(mensaje)

        return

    """
    Interpreta cada arreglo de bytes de manera que se separen los datos contenidos en cada trama
    @param:data_bytes arreglo de bytes que contiene la informacion de cada trama.
    """
    def interpretar_data(self, data_bytes):
        data_string = data_bytes.decode()
        data_array = data_string.split("|")
        data = {"version": int(data_array[0], 16),
                "id": int(data_array[1], 16),
                "mac": int(data_array[2], 16),
                "payload": data_array[3],
                "checksum": int(data_array[4], 16)
                }
        return data

    """
    Genera un archivo llamado tempfile donde se va a contener la informacion transmitida a través de archivos QR.
    """
    def crear_archivo(self, datos):
        try:
            f = open(self.textos.TEMP_FILE, 'w+b')
            f.write(bytes.fromhex(datos))
            f.close()
            print(self.textos.TEMPFILE_GENERADO)

        except OSError:
            print(self.textos.TEMPFILE_NO_GENERADO)

        return

    """
    Verifica que la direccion del nodo donde es transmitido el paquete sea el mismo de la maquina actual
    """
    def verificar_direccion(self, direccion):
        return direccion == self.DIRECCION_MAQUINA

    """
    Muentra en pantalla la direccion asignada a la computadora actual
    """
    def mostrar_direccion(self):
        print(self.textos.DIRECCION_MAQUINA)
        print(str(self.DIRECCION_MAQUINA) + "\n")
        time.sleep(2)
        return