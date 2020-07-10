import capa1.generador_trama
import time
import os
from capa1.generador_qr import *
from capa1.interpretador_qr import *

def main():
    mensaje_bienvenida()
    opcion = menu()


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
    leer_con_camara()


def mensaje_bienvenida():
    print('''

     _____         _        _                    _        
    |_   _|       (_)      (_)                  | |       
      | |   _ __   _   ___  _   __ _  _ __    __| |  ___  
      | |  | '_ \ | | / __|| | / _` || '_ \  / _` | / _ \ 
     _| |_ | | | || || (__ | || (_| || | | || (_| || (_) |
    |_____||_| |_||_| \___||_| \__,_||_| |_| \__,_| \___/ 



       ''')

    print('''
     _____                          _                    ____   _____  
    |  __ \                        | |                  / __ \ |  __ \ 
    | |__) | ___  _ __ ___    ___  | |_  ___   ______  | |  | || |__) |
    |  _  / / _ \| '_ ` _ \  / _ \ | __|/ _ \ |______| | |  | ||  _  / 
    | | \ \|  __/| | | | | || (_) || |_|  __/          | |__| || | \ \ 
    |_|  \_ \___||_| |_| |_| \___/  \__|\___|           \___\_\|_|  \_\ 


       ''')

    for i in range(4):
        print(".")
        time.sleep(1)

def menu():
    print("\t<<<---------- MENU PRINCIPAL ---------->>> \n\n\n A continuación se presentan una serie de distintas opciones del programa. Por favor, ingrese una la opción deseada y estripe la tecla ENTER\n")
    print("[1] Transmitición QR\n[2] Recepción QR\n[3] Conectarse a Red Mesh\n[4] Conectar a server IRC\n\n[0] Cerrar le programa")
    print("Digite la opción deseada")
    respuesta = input()

    try:
        respuesta = int(respuesta)
        if respuesta >= 1 and respuesta <= 4:
            return respuesta
        else:
            return -1
    except:
        print("La respuesta dada no es correcta. Vuelva a intentarlo\n")
        time.sleep(2)
        os.system('clear')
        menu()


main()