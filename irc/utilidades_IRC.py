import socket
from time import sleep

#Clase que maneja la conexion del bot con el servidor IRC
class IRC:

    def __init__(self):
        self.conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Funcion que inicia la conexion con un servidor IRC de acuerdo a los parametros ingresados
    def conexion_servidor(self, direccion, puerto, nick, realname, canal):
        usuario = 'USER %s %s %s :%s\n' % (nick, nick, nick, realname)
        nickname = 'NICK %s\n' % nick
        ingresarCanal = 'JOIN %s\n' % canal

        try:
            print("Conectando a: " + direccion)
            self.conexion.connect((direccion, puerto))

            self.conexion.send(usuario.encode("UTF-8"))
            self.conexion.send(nickname.encode("UTF-8"))
            sleep(5)
            self.conexion.send(ingresarCanal.encode("UTF-8"))
            reglas = ''
            while reglas.find("End of /NAMES list.") == -1:
                reglas = self.conexion.recv(2048).decode("UTF-8")
                print(reglas)
            return 'Conexion exitosa'
        except:
            return 'Fallo al conectar'

    #Funcion que envia mensaje al canal en que se esta
    def enviar(self, canal, mensaje):
        mensaje = 'PRIVMSG %s :%s\n' % (canal, mensaje)
        self.conexion.send(mensaje.encode("UTF-8"))

    #Funcion obtiene los mensajes enviados al canal por el server
    def respuesta(self):
        sleep(1)
        res = self.conexion.recv(2048).decode("UTF-8")

        if res.find('PING') != -1:
            activo = 'PONG pingid\n'
            self.conexion.send(activo.encode("UTF-8"))
            return None
        else:
            return res


