import socket
from threading import Thread
import random

import red_mesh.manejo_nodos
import red_mesh.paquete_mesh

#Clase que representa cada cliente de la red mesh
class NodoMesh:

    def __init__(self, ipServidor, puertoServidor):

        datosConexion = (ipServidor, puertoServidor)
        socketRegistro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketRegistro.connect(datosConexion)
        socketRegistro.send('CONNECT'.encode('utf-8'))
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
            print()
            print('----- Indicaciones --------')
            print('Formato para enviar un mensaje: "Para" [mac_destino] [mensaje]')
            print('Para salir utilizar la palabra "Salir"\n')
        else:
            print("Ocurrio un error en el registro")

    #Funcion que guarda todos los datos propios dentro de la red mesh
    def guardar_registro(self, datosNodo, datosRegistro, listaVecinos):
        nodoDatos = manejo_nodos.CrearNodo(datosNodo[0], datosNodo[1], int(datosNodo[2]))
        nodoRegistro = manejo_nodos.CrearNodo(datosRegistro[0], datosRegistro[1], int(datosRegistro[2]))
        vecinos = manejo_nodos.ListaNodos()
        vecinos.to_list(listaVecinos)
        return nodoDatos, nodoRegistro, vecinos

    #Funcion que esta escuchando a la espera de acciones realizadas por los otros clientes
    # de la red
    def solicitudes(self):

        socketEscucha = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketEscucha.bind((self.nodoDatos.get_ip(), self.nodoDatos.get_puerto()))
        socketEscucha.listen()

        while True:
            cliente, direccion = socketEscucha.accept()
            datosSolicitud = cliente.recv(2048).decode('utf-8')
            cliente.close()
            datosSolicitud = datosSolicitud.split()
            if datosSolicitud[0] == 'DEL' and datosSolicitud[1] == self.nodoDatos.get_mac():
                break
            else:
                solicitud = Thread(target=self.trabajar_solicitud, args=(datosSolicitud,))
                solicitud.start()
                solicitud.join()

    #Funcion que ejecuta la accion que se le solicito al nodo
    def trabajar_solicitud(self, datos):
        if datos[0] == 'NEWNODE':
            self.agregar_vecino(datos[1:])
            print("\nAgregado nuevo vecino: " + datos[2] + '\n')
        elif datos[0] == 'RV':
            print("\nRedireccionando paquete \n")
            self.reenviar_paquete(datos)
        elif datos[0] == 'MSJ':
            print('\nRECIBIDO: ' + " ".join(datos[1:]) + '\n')
        elif datos[0] == 'DEL':
            indiceVecino = self.listaVecinos.buscar_nodo(datos[1])
            vecinoEliminado = self.listaVecinos.eliminar_nodo(indiceVecino)
            print("\nEl vecino %s se desconecto.\n" %vecinoEliminado.get_mac())
        else:
            pass
        print(self.nodoDatos.get_mac() + '# ')

    #Funcion que agrega algun cliente que se acabe de conectar a la red
    def agregar_vecino(self, datosVecino):
        nodoVecino = manejo_nodos.CrearNodo(datosVecino[0], datosVecino[1], int(datosVecino[2]))
        self.listaVecinos.agregar_nodo(nodoVecino)

    #Funcion que reenvia el paquete quitandole quien lo envio
    def reenviar_paquete(self, paquete):
        ipDestino = paquete[1]
        puertoDestino = int(paquete[2])
        mensajeNuevo = " ".join(paquete[3:])

        try:
            cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            cliente.connect((ipDestino, puertoDestino))
            cliente.send(mensajeNuevo.encode('utf-8'))
            cliente.close()
        except:
            print("Fallo al reenviar un mensaje")

    #Funcion que crea un camino aleatorio por el que pasara el paquete sin seguimiento
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

    #Funcion que encapsula el paquete que se enviara
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

    #Funcion que hace el proceso de preparar los datos para el envio
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

    #Funcion que desconecta al cliente de la red mesh
    def desconetar(self):
        try:
            servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            servidor.connect((self.nodoRegistro.get_ip(), self.nodoRegistro.get_puerto()))
            servidor.send(('DEl ' + self.nodoDatos.get_mac()).encode('utf-8'))
            servidor.close()
        except:
            print("Fallo al desconectar en el servidor")

    #Funcion que habilita el envio de mensajes al usuario
    def enviar_mensaje(self):
        activo = True

        while activo:
            mensaje = input(self.nodoDatos.get_mac() + '# ')
            if mensaje.lower() == 'salir':
                self.desconetar()
                break
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
                        paquete = paquete.split()
                        self.reenviar_paquete(paquete)

    #Funcion que activa tanto la parte de escucha el nodo como la parte de aplicacion y uso
    # del cliente
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
