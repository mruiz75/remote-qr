class Paquete:

    def __init__(self, ipDestino, puertoDestino, mensaje):
        self.ipDestino = ipDestino
        self.puertoDestino = puertoDestino
        self.mensaje = mensaje

    def to_string(self):
        if type(self.mensaje) == str:
            stringPaquete = 'RV ' + self.ipDestino + ' ' + str(self.puertoDestino) + ' MSJ ' \
                            + self.mensaje
        else:
            stringPaquete = 'RV ' + self.ipDestino + ' ' + str(self.puertoDestino) + ' ' +\
                            self.mensaje.to_string()

        return stringPaquete


'''
pa = Paquete('12', '13', Paquete('14', '15', 'hola'))
print(pa.to_string())
'''