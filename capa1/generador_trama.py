#!/usr/bin/python

def crear_trama(version, id, ip0, ipf, mac, payload):
    trama = b''

    header = armar_header(version, id, ip0, ipf, mac)
    trama += header
    trama += armar_payload(payload)

    return trama

def armar_header(version, id, ip0, ipf, mac):
    header = b''

    version_bin = bytes([version])
    id_bin = bytes([id])
    ip0_bin = ip0.encode('utf-8')
    ipf_bin = ipf.encode('utf-8')
    mac_bin = mac.encode('utf-8')

    header += version_bin
    header += id_bin
    header += ip0_bin
    header += ipf_bin
    header += mac_bin

    return header

def calcular_checksum(payload):
    divisor = 24
    sum = 0

    for i in payload:
        sum += ord(i)

    checksum = bytes([sum % divisor])
    return checksum

def armar_payload(payload):
    b_payload = b''
    result = b''

    checksum = calcular_checksum(payload)
    result += checksum

    # convertir payload a bytes
    for letter in payload:
        b_payload += bytes(letter, encoding='utf-8')

    result += b_payload

    return result