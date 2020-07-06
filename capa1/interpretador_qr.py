#!/usr/bin/python

import cv2
import numpy as np
import pyzbar.pyzbar as pyzbar
import time

def leer_png(filename):
    img = cv2.imread(filename)
    decodedObs = pyzbar.decode(img)
    for obj in decodedObs:
        datos = interpretar_data(obj.data)

    # prueba
    img2 = cv2.imread("qr3.png")
    decodedObs2 = pyzbar.decode(img2)
    print(decodedObs2)
    # fin de prueba

    return


def leer_qr():
    cap = cv2.VideoCapture(0)
    leer = True
    mensaje = ""
    datos = {}
    nombre_archivo = "tempfile"

    while leer:
        _, frame = cap.read()

        decodedObjects = pyzbar.decode(frame)
        if decodedObjects:
            for obj in decodedObjects:
                datos = interpretar_data(obj.data)
                if datos["id"] != "F":
                    mensaje += datos["payload"]
                else:
                    leer = False
                print(datos)
            time.sleep(3)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)

        if key == 27:
            break

    tipo_de_mensaje = int(datos["version"])

    if tipo_de_mensaje == 2:
        #envia mensaje
        pass
    elif tipo_de_mensaje == 1:
        f = open(nombre_archivo, 'w+b')
        f.write(mensaje.encode())
        f.close


    return


def interpretar_data(data_bytes):
    data_string = data_bytes.decode()
    data_array = data_string.split("|")
    data = {"version" : data_array[0],
            "id": data_array[1],
            "ip": data_array[2],
            "mac": data_array[3],
            "payload": data_array[4],
            "checksum": data_array[5]
            }

    return data