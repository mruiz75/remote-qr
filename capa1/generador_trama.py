#!/usr/bin/python

import sys

"""
Este archivo contiene los métodos necesarios para poder generar una trama de 128 bytes para la generación
de un código QR.
"""


"""
Método principal que le da la estructura a la creación de la trama
"""
def crear_trama(version, cont, direccion, payload):
    trama = ""

    header = armar_header(version, cont, direccion)
    trama += header
    trama, payload_restante = armar_payload(trama, payload)

    return trama, payload_restante


"""
Método que le da la estructura la header concatenando los valores hexadecimales de los parámetros separados
por un '|' 
"""
def armar_header(version, cont, direccion):
    header = ""

    version_hex = hex(version)[2:]
    cont_hex = hex(cont)[2:]
    direccion_hex = hex(direccion)[2:]

    header += version_hex + "|"
    header += cont_hex + "|"
    header += direccion_hex + "|"

    return header


"""
Método que calcula el checksum de cada trama, retornando su valor numérico (int)
@param:payload un string conteniendo todo el payload restante
"""
def calcular_checksum(payload):
    divisor = 24
    sum = 0

    for i in payload:
        sum += ord(i)

    checksum = sum % divisor
    return checksum


"""
Método que arma el payload concatenando el checksum con el payload utilizado. 
Retorna la trama lista y el payload restante
@param:trama string con la trama incompleta
@param:payload string de valores hexadecimales con la información por transmitir
"""
def armar_payload(trama, payload):
    payload_procesado = ""

    while(sys.getsizeof(trama) < 125 and len(payload) > 0):
        trama += payload[0]
        payload_procesado += payload[0]
        payload = payload[1:]

    trama += "|"

    checksum = calcular_checksum(payload_procesado)
    trama += hex(checksum)[2:]

    return trama, payload