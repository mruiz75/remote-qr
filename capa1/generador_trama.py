#!/usr/bin/python
import sys

def crear_trama(version, cont, mac, payload):
    #trama = b''
    trama = ""

    header = armar_header(version, cont, mac)
    trama += header
    len_header = sys.getsizeof(trama)
    trama, payload_restante = armar_payload(trama, payload)
    #trama += payload_usado
    #print(sys.getsizeof(trama))
    print(trama)
    return trama, payload_restante


def armar_header(version, cont, mac):
    #header = b''
    header = ""

    # version_b = (version + "|").encode('utf-8')
    # cont_b = (cont + "|").encode('utf-8')
    # mac_b = (mac +"|").encode('utf-8')
    version_hex = hex(version)[2:]
    cont_hex = hex(cont)[2:]
    mac_hex = hex(mac)[2:]

    header += version_hex + "|"
    header += cont_hex + "|"
    header += mac_hex + "|"

    return header


def calcular_checksum(payload):
    #payload = payload.decode()
    divisor = 24
    sum = 0

    for i in payload:
        sum += ord(i)
        #sum += i

    checksum = sum % divisor
    #return str(checksum)
    return checksum


def armar_payload(trama, payload):
    payload_procesado = ""

    while(sys.getsizeof(trama) < 125 and len(payload) > 0):
        #trama += bytes([payload[0]])
        trama += payload[0]
        # payload_procesado += bytes([payload[0]])
        payload_procesado += payload[0]
        payload = payload[1:]

    #trama += "|".encode()
    trama += "|"

    checksum = calcular_checksum(payload_procesado)
    #trama += (checksum).encode('utf-8')
    trama += hex(checksum)[2:]

    return trama, payload