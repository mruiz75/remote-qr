#!/usr/bin/python3

import sys

from capa1.dispositivo_de_transmision import *
from capa1.dispositivo_luz_adaptador import *
from irc.bot_irc import *
from red_mesh.nodo_mesh import *
from red_mesh.MAC_generator import *

texto = Textos()


"""
Método principal que le da estructura al programa
"""
def main():
    mensaje_bienvenida()

    try:
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

    except KeyboardInterrupt:
        salir()


    salir()

    return


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


"""
Método encargado de obtener los parámetros necesarios para transmitir un mensaje o un archivo
"""
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

        ddt = DispositivoDeTransmision()

        ddt.texto_a_qr(version=1,
                   mac=direccion,
                   texto_hex=mensaje)

        print(texto.QR_GENERADOS)
        time.sleep(2)

        return

    elif respuesta == 2:
        try:
            direccion = int(input(texto.DIRECCION))
            archivo = input(texto.PATH)

        except ValueError:
            print(texto.RESPUESTA_INVALIDA)

        ddt = DispositivoDeTransmision()

        ddt.file_a_qr(version=2,
                  mac=direccion,
                  filename=archivo)

        print(texto.QR_GENERADOS)
        time.sleep(2)

        return

    elif respuesta == 0:
        return

    else:
        print(texto.OPCION_INEXISTENTE)
        qr_sender()


"""
Método encargado de obtener la información necesaria para interpretar los códigos QR
"""
def qr_receiver():
    print(texto.QR_RECEIVER)
    mg = MACGenerator()
    direccion = int(mg.generate())

    try:
        respuesta = int(input(texto.R))

    except ValueError:
        print(texto.RESPUESTA_INVALIDA)
        qr_receiver()

    if respuesta == 1:
        print(texto.LECTURA_CAMARA)

        dla = DispositivoLuzAdaptador(direccion)

        dla.leer_con_camara()

        return

    elif respuesta == 2:
        path = input(texto.PATH)

        dla = DispositivoLuzAdaptador(direccion)

        dla.leer_imagenes(path)

        return

    elif respuesta == 0:
        return

    else:
        print(texto.OPCION_INEXISTENTE)
        qr_sender()


"""
Método que establece la conexión a la red mesh
"""
def red_mesh():
    try:
        cliente = NodoMesh('127.0.0.1', 1505)
        cliente.main()

    except ConnectionRefusedError:
        print(texto.ERROR_CONEXION)
        time.sleep(2)

    return


"""
Método que obtiene los parámetros necesarios para establecer la conexión con le servidor IRC
"""
def irc():
    print(texto.IRC)

    nick = input(texto.NICK)
    real_name = input(texto.REAL_NAME)

    bot = BotIRC(nick, real_name)
    bot.activar()

    return


"""
Método para acabar con la ejecución del programa
"""
def salir():
    print(texto.SALIR)
    for i in range(3):
        print(".")
        time.sleep(0.3)
    return sys.exit()

main()