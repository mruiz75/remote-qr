class Paquete:

    def __init__(self, macDestino, macOrigen, mensaje):
        self.macOrigen = macOrigen
        self.macDestino = macDestino
        self.mensaje = mensaje

    def to_string(self):
        if type(self.mensaje) == str:
            stringPaquete = self.macOrigen + ' ' + self.macDestino + ' msj ' + self.mensaje
        else:
            stringPaquete = self.macOrigen + ' ' + self.macDestino + ' ' + self.mensaje.to_string()

        return  stringPaquete

pa = Paquete('12', '13', Paquete('14', '15', 'hola'))
print(pa.to_string())
