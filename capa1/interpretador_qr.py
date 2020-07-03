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
    leer, continuar = True, True
    mensaje = ""

    while leer:
        _, frame = cap.read()

        decodedObjects = pyzbar.decode(frame)
        if decodedObjects:
            for obj in decodedObjects:
                datos, continuar = interpretar_data(obj.data)
                if continuar:
                    mensaje += datos["payload"]
                print(datos)
            time.sleep(3)

        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1)

        if key == 27:
            break

        if not continuar:
            leer = False

    print(mensaje)
    return


def interpretar_data(data_bytes):
    continuar = True;
    data = {}
    data_string = data_bytes.decode()
    data_array = data_string.split("|")
    if data_array[0] is "F":
        continuar = False
    else:
        data = {"version" : data_array[0],
                "id": data_array[1],
                "ip": data_array[2],
                "mac": data_array[3],
                "payload": data_array[4],
                "checksum": data_array[5]
                }

    #FALTA INTERPRETAR DIFERNECIA ENTRE MENSAJE Y ARCHIVO

    return data, continuar