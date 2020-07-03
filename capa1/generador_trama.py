#!/usr/bin/python
import sys

def crear_trama(version, cont, ip, mac, payload):
    trama = b''

    header = armar_header(version, cont, ip, mac)
    trama += header
    len_header = sys.getsizeof(trama)
    trama, payload_restante = armar_payload(trama, payload)
    #trama += payload_usado
    print(sys.getsizeof(trama))

    return trama, payload_restante


def armar_header(version, cont, ip, mac):
    header = b''

    version_b = (version + "|").encode('utf-8')
    cont_b = (cont + "|").encode('utf-8')
    ip_b = (ip + "|").encode('utf-8')
    mac_b = (mac +"|").encode('utf-8')

    header += version_b
    header += cont_b
    header += ip_b
    header += mac_b

    return header


def calcular_checksum(payload):
    payload = payload.decode()
    divisor = 24
    sum = 0

    for i in payload:
        sum += ord(i)

    checksum = sum % divisor
    return str(checksum)


def armar_payload(trama, payload):
    payload_procesado = b''

    while(sys.getsizeof(trama) < 125 and len(payload) > 0):
        trama += bytes([payload[0]])
        payload_procesado += bytes([payload[0]])
        payload = payload[1:]

    trama += "|".encode()

    checksum = calcular_checksum(payload_procesado)
    trama += (checksum).encode('utf-8')


    return trama, payload