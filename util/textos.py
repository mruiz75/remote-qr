#!/usr/bin/python


"""
Clase encargada de almacenar el texto por imprimir en consola
"""
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
    MENU_PRINCIPAL = "\n\t<<<---------- MENU PRINCIPAL ---------->>> \n\nA continuación se presentan una serie de distintas opciones del programa. Por favor, ingrese una la opción deseada y estripe la tecla ENTER\n"
    OPCIONES = "[1] Transmición QR\n[2] Recepción QR\n[3] Conectarse a Red Mesh\n[4] Conectar a server IRC\n\n[0] Cerrar le programa"
    RESPUESTA_INVALIDA = "La respuesta dada no es correcta. Vuelva a intentarlo\n"
    OPCION_INEXISTENTE = "La opción escogida no existe. Por favor, elija una de las opciones existentes.\n"
    QR_SENDER = "\nPara comunicarse, desea enviar un:\n[1] Mensaje\n[2] Archivo\n\n[0] Volver al menú principal"
    QR_RECEIVER = "\nPara la lectura de QR, desea:\n[1] Usar la cámara\n[2] Leer archivos\n\n[0] Volver al menú principal"
    SALIR = "\nCerrando Remote-QR"
    R = "R/ "

    # -------------------------------------------------------


    # -------------------------- QR -------------------------
    DIRECCION = "\nDigite la dirección del nodo a contactar: "
    ENVIAR_MENSAJE = "\nDigite el mensaje que desea enviar: "
    PATH = "\nDigite la ruta completa hasta el directorio donde se encuentran el/los archivo(s): "
    LECTURA_CAMARA = "\nIniciando la lectura con camara...\n"
    QR_LEIDO = "QR leído exitosamente."
    MALA_LECTURA = "La lectura de los QR no se dio en el orden adecuado."
    DIRECCION_INCORRECTO = "El mensaje no fue enviado a la dirección correcta."
    CHECKSUM_INCORRECTO = "Fallo en el cálculo del checksum."
    ERROR_LECTURA_IMAGENES = "Error leyendo imagenes del path especificado."
    TEMPFILE_GENERADO = "Archivo tempfile generado exitosamente."
    TEMPFILE_NO_GENERADO = "El archivo tempfile no pudo ser generado exitosamente."
    QR_GENERADOS = "\n\n --> Los QR correspondientes han sido generados existosamente. <--\n\n"
    DIRECCION_MAQUINA = "\nDirección de máquina: "
    TEMP_FILE = "tempfile"

    # -------------------------------------------------------


    # ------------------------  MESH ------------------------
    ERROR_CONEXION = "Error al intentar la conexión. Por favor, asegúrese que el servidor está corriendo y vuelva a intentarlo.\n"
    # -------------------------------------------------------


    # ------------------------- IRC -------------------------
    IRC = "Para poder iniciar el chat, son necesarios los datos de identificación\n"
    NICK = "Ingrese el Nick del usuario del chat: "
    REAL_NAME = "Ingrese el nombre real para uso del chat: "
    CERRAR_IRC = "Cerrando la sesión de IRC\n"
    # -------------------------------------------------------

    def __init__(self):
        pass