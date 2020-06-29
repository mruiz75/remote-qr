import socket
from threading import Thread
import random

import manejo_nodos
import paquete_mesh
import argparse

class NodoMesh:

    def __init__(self, ipServidor, puertoServidor):

        datosConexion = (ipServidor, puertoServidor)
        socketRegistro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketRegistro.connect(datosConexion)
        print("Registrando con el servidor ---> %s:%s" % datosConexion)
        datos = socketRegistro.recv(2048).decode('utf-8')

        datos = datos.split()
        datosNodo = datos[:3]
        datosRegistro = datos[3:6]
        listaVecinos = datos[6:]
        (self.nodoDatos, self.nodoRegistro, self.listaVecinos) = self.guardar_registro(datosNodo,
                                                                                     datosRegistro,
                                                                                     listaVecinos)
        if datosNodo:
            print("Registro Exitoso, su id es: " + self.nodoDatos.get_mac())
        else:
            print("Ocurrio un error en el registro")
        #print(self.nodoDatos.get_puerto())
        #print(self.nodoRegistro.get_puerto())
        #print(self.listaVecinos.get_lista())

    def guardar_registro(self, datosNodo, datosRegistro, listaVecinos):
        nodoDatos = manejo_nodos.CrearNodo(datosNodo[0], datosNodo[1], int(datosNodo[2]))
        nodoRegistro = manejo_nodos.CrearNodo(datosRegistro[0], datosRegistro[1], int(datosRegistro[2]))
        vecinos = manejo_nodos.ListaNodos()
        vecinos.to_list(listaVecinos)
        return nodoDatos, nodoRegistro, vecinos

    def solicitudes(self):

        socketEscucha = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketEscucha.bind((self.nodoDatos.get_ip(), self.nodoDatos.get_puerto()))
        socketEscucha.listen()

        while True:
            cliente, direccion = socketEscucha.accept()
            datosSolicitud = cliente.recv(2048).decode('utf-8')
            cliente.close()
            solicitud = Thread(target=self.trabajar_solicitud, args=(datosSolicitud,))
            solicitud.start()
            solicitud.join()

    def trabajar_solicitud(self, datos):
        datos = datos.split()
        if datos[0] == 'NEWNODE':
            self.agregar_vecino(datos[1:])
            print("Agregado nuevo vecino: " + datos[2])
        elif datos[0] == 'RV':
            print("\n Redireccionando paquete \n")
            self.reenviar_paquete(datos)
        elif datos[0] == 'MSJ':
            print('\n RECIBIDO: ' + " ".join(datos[1:]) + '\n')
        else:
            pass


    def agregar_vecino(self, datosVecino):
        nodoVecino = manejo_nodos.CrearNodo(datosVecino[0], datosVecino[1], int(datosVecino[2]))
        self.listaVecinos.agregar_nodo(nodoVecino)

    def reenviar_paquete(self, paquete):
        ipDestino = paquete[1]
        puertoDestino = int(paquete[2])
        mensajeNuevo = " ".join(paquete[3:])
        #print(mensajeNuevo)

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((ipDestino, puertoDestino))
            cliente.send(mensajeNuevo.encode('utf-8'))
            cliente.close()
        except:
            print("Fallo al enviar un mensaje")

    def generar_ruta_aleatoria(self, macDestino):
        posDestino = self.listaVecinos.buscar_nodo(macDestino)
        cantidadNodos = len(self.listaVecinos.get_lista())

        if posDestino == -1:
            print("Destino inexistente \n")
            ruta = None
        elif cantidadNodos == 2:
            if posDestino == 0:
                ruta = [1, 0]
            else:
                ruta = [0, 1]
        else:
            ruta = []
            while len(ruta) < 2:
                pos = random.randint(0, cantidadNodos-1)
                if pos != posDestino and pos not in ruta:
                    ruta.append(pos)
            ruta.append(posDestino)
        return ruta

    def crear_paquete(self, ruta, mensaje):
        nodos = len(ruta) - 1

        vecino = self.listaVecinos.get_lista()[ruta[nodos]]
        paquete = paquete_mesh.Paquete(vecino.get_ip(), vecino.get_puerto(), mensaje)
        nodos -= 1

        while nodos > -1:
            vecino = self.listaVecinos.get_lista()[ruta[nodos]]
            paquete = paquete_mesh.Paquete(vecino.get_ip(), vecino.get_puerto(), paquete)
            nodos -= 1

        return paquete

    def crear_ruta(self, macDestino, mensaje):
        paquete = None

        if len(self.listaVecinos.get_lista()) < 1:
            print("No existen vecinos \n")
        elif macDestino == self.nodoDatos.get_mac():
            print(mensaje)
        elif len(self.listaVecinos.get_lista()) == 1 and \
                self.listaVecinos.get_lista()[0].get_mac() == macDestino:
            vecino = self.listaVecinos.get_lista()[0]
            paquete = paquete_mesh.Paquete(vecino.get_ip(), vecino.get_puerto(), mensaje)
            paquete = paquete.to_string()
        else:
            ruta = self.generar_ruta_aleatoria(macDestino)
            paquete = self.crear_paquete(ruta, mensaje)
            paquete = paquete.to_string()

        return paquete

    def enviar_mensaje(self):
        activo = True

        while activo:
            mensaje = input(self.nodoDatos.get_mac() + '# ')
            if mensaje.lower() == 'salir':
                activo = False
            else:
                mensaje = mensaje.split()
                if len(mensaje) < 3:
                    print("Formato incorrecto.\n")
                elif mensaje[0].lower() != 'para':
                    print("Formato incorrecto.\n")
                elif mensaje[1] == self.nodoDatos.get_mac():
                    print(" ".join(mensaje[2:]))
                elif self.listaVecinos.buscar_nodo(mensaje[1]) == -1:
                    print("Destinatario innexistente. \n")
                else:
                    paquete = self.crear_ruta(mensaje[1], " ".join(mensaje[2:]))
                    if paquete:
                        #print(paquete)
                        paquete = paquete.split()
                        #print(paquete)
                        self.reenviar_paquete(paquete)

    def main(self):
        hilo_solicitudes = Thread(target=self.solicitudes)
        hilo_solicitudes.start()

        hilo_envios = Thread(target=self.enviar_mensaje)
        hilo_envios.start()

        hilo_solicitudes.join()
        hilo_envios.join()




if __name__ == "__main__":
    cliente = NodoMesh('127.0.0.1', 1505)
    cliente.main()


    #parametros = datos()
    #print(parametros.ip)


'''
#declaramos las variables
ipServidor = "127.0.0.1" #es lo mismo que "localhost" o "0.0.0.0"
puertoServidor = 1505

#Configuramos los datos para conectarnos con el servidor
#socket.AF_INET para indicar que utilizaremos Ipv4
#socket.SOCK_STREAM para utilizar TCP/IP (no udp)
#Estos protocolos deben ser los mismos en el principal
def nose():
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((ipServidor, puertoServidor))
    print("Conectado con el servidor ---> %s:%s" %(ipServidor, puertoServidor))

    #Bucle de escucha. En él indicamos la forma de actuar al recibir las tramas del cliente
    while True:
        msg = input("> ")
        cliente.send(msg.encode('utf-8'))
        respuesta = cliente.recv(4096).decode('utf-8')
        print(respuesta)
        if respuesta == "exit":
            break;

    print("------- CONEXIÓN CERRADA ---------")
    cliente.close()

def datos():
    parser = argparse.ArgumentParser(description='IP y puerto del servidor a conectar')
    parser.add_argument('ip', help='Server ip')
    parser.add_argument('p', help='Server port')

    args = parser.parse_args()

    return args
'''