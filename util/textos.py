#!/usr/bin/python

class Textos:

    # ------------------- MENU PRINCIPAL -------------------
    REMOTE_QR = '''
     _____                          _                    ____   _____  
    |  __ \                        | |                  / __ \ |  __ \ 
    | |__) | ___  _ __ ___    ___  | |_  ___   ______  | |  | || |__) |
    |  _  / / _ \| '_ ` _ \  / _ \ | __|/ _ \ |______| | |  | ||  _  / 
    | | \ \|  __/| | | | | || (_) || |_|  __/          | |__| || | \ \ 
    |_|  \_ \___||_| |_| |_| \___/  \__|\___|           \___\_\|_|  \_\ 


       '''

    INICIADO = '''

     _____         _        _                    _        
    |_   _|       (_)      (_)                  | |       
      | |   _ __   _   ___  _   __ _  _ __    __| |  ___  
      | |  | '_ \ | | / __|| | / _` || '_ \  / _` | / _ \ 
     _| |_ | | | || || (__ | || (_| || | | || (_| || (_) |
    |_____||_| |_||_| \___||_| \__,_||_| |_| \__,_| \___/ 



       '''
    MENU_PRINCIPAL = "\t<<<---------- MENU PRINCIPAL ---------->>> \n\nA continuación se presentan una serie de distintas opciones del programa. Por favor, ingrese una la opción deseada y estripe la tecla ENTER\n"
    OPCIONES = "[1] Transmición QR\n[2] Recepción QR\n[3] Conectarse a Red Mesh\n[4] Conectar a server IRC\n\n[0] Cerrar le programa"
    RESPUESTA_INVALIDA = "La respuesta dada no es correcta. Vuelva a intentarlo\n"
    OPCION_INEXISTENTE = "La opción escogida no existe. Por favor, elija una de las opciones existentes.\n"
    QR_SENDER = "\nPara comunicarse, desea enviar un:\n[1] Mensaje\n[2] Archivo"
    QR_RECEIVER = "\nPara la lectura de QR, desea:\n[1] Usar la cámara\n[2] Leer archivos"
    SALIR = "\nCerrando Remote-QR"
    R = "R/ "
    DIRECCION = "Digite la dirección del nodo a contactar: "
    ENVIAR_MENSAJE = "Digite el mensaje que desea enviar: "
    PATH = "Digite la ruta completa hasta el directorio donde se encuentran el/los archivos(s): "
    LECTURA_CAMARA = "\nIniciando la lectura con camara...\n"

    # -------------------------------------------------------

    def __init__(self):
        pass