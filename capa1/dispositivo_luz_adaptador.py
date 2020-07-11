#!/usr/bin/python

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import time
import glob
from capa1.generador_trama import calcular_checksum


class DispositivoLuzAdaptador:

    DIRECCION_MAQUINA = 0

    def __init__(self, direccion):
        self.DIRECCION_MAQUINA = direccion

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
            print("Error leyendo imagenes del path especificado")
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

        destino_correcto = self.verificar_direccion(datos["mac"])

        if not lectura_limpia:
            print("La lectura de los QR no se dio en el orden adecuado")
            return

        if not destino_correcto:
            print("El mensaje no fue enviado a la dirección correta")
            return

        if not checksum_correcto:
            print("Fallo en el cálculo del checksum")
            return

        if tipo_de_mensaje == 1:
            self.crear_archivo(mensaje)

        elif tipo_de_mensaje == 2:
            self.crear_archivo(mensaje)
            # envia mensaje
            pass

        return


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

                print(datos)
                time.sleep(3)

            cv2.imshow("Frame", frame)
            key = cv2.waitKey(1)

            if key == 27:
                break

        destino_correcto = self.verificar_direccion(datos["mac"])

        if not lectura_limpia:
            print("La lectura de los QR no se dio en el orden adecuado")
            return

        if not destino_correcto:
            print("El mensaje no fue enviado a la dirección correta")
            return

        if not checksum_correcto:
            print("Fallo en el cálculo del checksum")
            return

        if tipo_de_mensaje == 1:
            self.crear_archivo(mensaje)
        elif tipo_de_mensaje == 2:
            print(mensaje)

        return


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


    def crear_archivo(self, datos):
        try:
            nombre_archivo = "tempfile"

            f = open(nombre_archivo, 'w+b')
            # f.write(datos.encode())
            f.write(bytes.fromhex(datos))
            f.close()
            print("Archivo tempfile generado exitosamente")

        except OSError:
            print("El archivo tempfile no pudo ser generado exitosamente")

        return


    def verificar_direccion(self, direccion):
        return direccion == self.DIRECCION_MAQUINA