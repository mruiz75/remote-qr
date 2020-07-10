import utilidades_IRC as UIRC
from threading import Thread
import argparse

#Clase que corre el bot de la conexion con el servidor
class BotIRC:

    def __init__(self, nick, realname):
        self.host = 'agility.nl.eu.dal.net'
        self.puerto = 6667
        self.nick = nick #'remote-qr'
        self.realName = realname #'admin remote-qr'
        self.canal = '#QR-IRC'
        self.conexionIRC = UIRC.IRC()
        print(self.conexionIRC.conexion_servidor(self.host, self.puerto, self.nick, self.realName,
                                           self.canal))

    #Funcion que esta leyendo constantemente mensajes que llegen al canal del IRC
    def buzon(self):
        while True:
            mensaje = self.conexionIRC.respuesta()
            if mensaje.find('PRIVMSG') != -1:
                mensaje = mensaje.split('PRIVMSG', 1)[1]
                print(mensaje)
                print(self.canal + ': ')

    #Funcion que da el espacio para que el cliente le diga al bot que mensaje desea enviar al canal
    def terminal_usuario(self):
        print('Bienvenido al chat del canal %s, aquí puede escribir los mensaje que serán vistos'
              'por los miembros del canal' % self.canal)
        while True:
            mensaje = input(self.canal + ': ')
            if mensaje.lower() != 'salir':
                self.conexionIRC.enviar(self.canal, mensaje)
            else:
                print('Cerrando sesion')
                break

    #Funcion que activa el bot para ser utilizado
    def activar(self):
        hilo_buzon = Thread(target=self.buzon)
        hilo_buzon.start()

        hilo_usuario = Thread(target=self.terminal_usuario())
        hilo_usuario.start()

        hilo_buzon.join()
        hilo_usuario.join()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Ingresos de datos para el IRC')
    parser.add_argument('nick', help='El Nick user del IRC')
    parser.add_argument('realName', help='El nombre real para el uso del IRC')
    args = parser.parse_args()
    bot = BotIRC(args.nick, args.realName)
    bot.activar()
