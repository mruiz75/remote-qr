'''
Utilidad para generar las direcciones MAC necesarias en las conexiones
'''
from random import choice
class MACGenerator:
    def __init__(self):
        self.valores = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',]
        self.extension = 10

    def generate(self):
        new_address = ''

        for i in range(self.extension):
            new_address += choice(self.valores)

        return new_address
