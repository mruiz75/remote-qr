#Clase que representa el paquete que se envia por la red mesh
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
