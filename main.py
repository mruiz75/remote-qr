#!/usr/bin/python

import capa1.generador_trama
import time
import os
import tkinter as tk

from tkinter import filedialog
from util.textos import *
from capa1.dispositivo_de_transmision import *
from capa1.dispositivo_luz_adaptador import *

texto = Textos()

def main():
    mensaje_bienvenida()

    while True:
        opcion = menu()

        if opcion == 1:
            qr_sender()

        elif opcion == 2:
            qr_receiver()

        elif opcion == 3:
            red_mesh()

        elif opcion == 4:
            irc()

        elif opcion == 0:
            break

    salir()




    version = 1
    mac = 12354356
    filename1 = "/Users/Manuel/Documents/TEC/2020/Redes/Proyectos/remote-qr/capa1/texto1.txt"
    filename2 = "/Users/Manuel/Documents/TEC/2020/Redes/Proyectos/remote-qr/capa1/prueba.pdf"
    filename3 = "/Users/Manuel/Documents/TEC/2020/Redes/Proyectos/remote-qr/capa1/img.png"
    filename4 = "/Users/Manuel/Documents/TEC/2020/Redes/Proyectos/remote-qr/capa1/img2.png"
    filename5 = "/Users/Manuel/Documents/TEC/2020/Redes/Proyectos/remote-qr/capa1/prueba.txt"
    path = "/Users/Manuel/Documents/TEC/2020/Redes/Proyectos/remote-qr/tempfolder"
    #texto_a_qr(version, ip, mac, filename1)
    #file_a_qr(version, mac, filename5)
    #--------
    #leer_imagenes(path)
    #leer_imagen()
    #leer_con_camara()


def mensaje_bienvenida():
    print(texto.INICIADO)
    print(texto.REMOTE_QR)

    for i in range(3):
        print(".")
        time.sleep(0.3)


def menu():
    print(texto.MENU_PRINCIPAL)
    print(texto.OPCIONES)

    try:
        respuesta = int(input(texto.R))

    except ValueError:
        print(texto.RESPUESTA_INVALIDA)
        time.sleep(2)
        os.system('clear')
        menu()

    if respuesta >= 0 and respuesta <= 4:
        return respuesta

    else:
        print(texto.OPCION_INEXISTENTE)
        time.sleep(2)
        os.system('clear')
        menu()


def qr_sender():
    print(texto.QR_SENDER)
    try:
        respuesta = int(input(texto.R))

    except ValueError:
        print(texto.RESPUESTA_INVALIDA)
        qr_sender()

    if respuesta == 1:
        direccion = int(input(texto.DIRECCION))
        mensaje = input(texto.ENVIAR_MENSAJE).encode().hex()

        texto_a_qr(version=1,
                   mac=direccion,
                   texto_hex=mensaje)

        return

    elif respuesta == 2:
        direccion = int(input(texto.DIRECCION))
        archivo = input(texto.PATH)

        file_a_qr(version=2,
                  mac=direccion,
                  filename=archivo)

        return

    elif respuesta == 0:
        return

    else:
        print(texto.OPCION_INEXISTENTE)
        qr_sender()


def qr_receiver():
    print(texto.QR_RECEIVER)
    try:
        respuesta = int(input(texto.R))

    except ValueError:
        print(texto.RESPUESTA_INVALIDA)
        qr_receiver()

    if respuesta == 1:
        print(texto.LECTURA_CAMARA)

        leer_con_camara()

        return

    elif respuesta == 2:
        path = input(texto.PATH)

        leer_imagenes(path)

        return

    elif respuesta == 0:
        return

    else:
        print(texto.OPCION_INEXISTENTE)
        qr_sender()


def red_mesh():
    pass


def irc():
    pass


def salir():
    print(texto.SALIR)
    for i in range(3):
        print(".")
        time.sleep(0.3)
    return sys.exit()

main()