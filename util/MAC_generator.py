'''
Utilidad para generar las direcciones MAC necesarias en las conexiones
'''
from random import choice

valores = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           'A', 'B', 'C', 'D', 'E', 'F']
extension = 10

def generate():

    new_address = ''

    for i in range(extension):
        new_address += choice(valores)

    return new_address
