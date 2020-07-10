#!/usr/bin/python

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import time
import glob
from capa1.generador_trama import calcular_checksum


DIRECCION_MAQUINA = 12354356

def leer_imagenes(path):
    lectura_limpia = True
    checksum_correcto = True
    mensaje = ""
    datos = {}
    id = 0
    path = path + "/*.png"

    try:
        images = [cv2.imread(file) for file in sorted(glob.glob(path))]         # lee todas las imagenes del path especificado
    except:
        print("Error leyendo imagenes del path especificado")
        return

    for img in images:
        decodedObs = pyzbar.decode(img)
        datos = interpretar_data(decodedObs[0].data)
        if datos["version"] != 0:
            payload = datos["payload"]
            qr_id = datos["id"]
            tipo_de_mensaje = datos["version"]
            checksum = datos["checksum"]

            lectura_limpia = qr_id == id
            id += 1
            checksum_correcto = checksum == calcular_checksum(payload)
            mensaje += payload

        else:
            leer = False

    destino_correcto = verificar_direccion(datos["mac"])

    if lectura_limpia:
        if destino_correcto:
            if tipo_de_mensaje == 1:
                crear_archivo(mensaje)

            elif tipo_de_mensaje == 2:
                crear_archivo(mensaje)
                # envia mensaje
                pass
        else:
            print("El mensaje no fue enviado a la dirección correta")
    else:
        print("La lectura de los QR no se dio en el orden adecuado")

    return


def leer_con_camara():
    lectura_limpia = True
    checksum_correcto = True
    leer = True
    mensaje = ""
    datos = {}
    id_anterior = -1

    cap = cv2.VideoCapture(0)

    while leer:                     # mantiene el ciclo de lectura con cámara web
        _, frame = cap.read()

        decodedObjects = pyzbar.decode(frame)
        if decodedObjects:
            datos = interpretar_data(decodedObjects[0].data)
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

    destino_correcto = verificar_direccion(datos["mac"])

    if not lectura_limpia:
        print("La lectura de los QR no se dio en el orden adecuado")

    if not destino_correcto:
        print("El mensaje no fue enviado a la dirección correta")

    if not checksum_correcto:
        print("Fallo en el cálculo del checksum")

    if tipo_de_mensaje == 1:
        crear_archivo(mensaje)
    elif tipo_de_mensaje == 2:
                print(mensaje)

    return


def interpretar_data(data_bytes):
    data_string = data_bytes.decode()
    data_array = data_string.split("|")
    data = {"version" : int(data_array[0], 16),
            "id": int(data_array[1], 16),
            "mac": int(data_array[2], 16),
            "payload": data_array[3],
            "checksum": int(data_array[4], 16)
            }
    print(data)
    return data


def crear_archivo(datos):
    try:
        nombre_archivo = "tempfile"

        f = open(nombre_archivo, 'w+b')
        #f.write(datos.encode())
        f.write(bytes.fromhex(datos))
        f.close()
        print("Archivo tempfile generado exitosamente")

    except:
        print("El archivo tempfile no pudo ser generado exitosamente")

    return


def verificar_direccion(direccion):
    return direccion == DIRECCION_MAQUINA