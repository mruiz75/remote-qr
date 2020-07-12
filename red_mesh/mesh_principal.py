import socket
from threading import Thread

import MAC_generator
import manejo_nodos as mn

#Clase que funciona como un servidor de registro a la red mesh
class MeshPrincipal:

    def __init__(self):
        ip = '0.0.0.0'
        mac = MAC_generator.MACGenerator()
        puerto = 1505
        self.datosNodo = mn.CrearNodo(ip, mac.generate(), puerto)
        self.nodosConectados = mn.ListaNodos()


    #Funcion que crear un nodo nuevo con el ip y puerto del solicitante y una mac única
    def crear_nodo_registro(self, direccion_cliente):
        generador = MAC_generator.MACGenerator()
        generarMAC = True

        while generarMAC:
            mac_cliente = generador.generate()
            repetido = False
            if mac_cliente != self.datosNodo.get_mac():
                for nodo in self.nodosConectados.get_lista():
                    if nodo.get_mac() == mac_cliente:
                        repetido = True
            else:
                repetido = True

            if repetido == False:
                generarMAC = False

        nodo_cliente = mn.CrearNodo(direccion_cliente[0], mac_cliente, int(direccion_cliente[1]))
        return nodo_cliente


    #Funcion que informa a toda la red del nuevo cliente
    def agregar_cliente(self, cliente, direccion):
        nodoCliente = self.crear_nodo_registro(direccion)
        string_datos = nodoCliente.to_string()
        codificacion = 'utf-8'
        for nodo in self.nodosConectados.get_lista():
            try:
                conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conexion.connect((nodo.get_ip(), nodo.get_puerto()))
                conexion.send(('NEWNODE ' + string_datos).encode(codificacion))
                conexion.close()
            except:
                pass
        cliente.send(nodoCliente.to_string().encode(codificacion))
        cliente.send(self.datosNodo.to_string().encode(codificacion))
        cliente.send(self.nodosConectados.to_string().encode(codificacion))
        cliente.close()
        self.nodosConectados.agregar_nodo(nodoCliente)
        print("Agregado el nodo %s:%s" % (nodoCliente.get_ip(), str(nodoCliente.get_puerto())))


    #Funcion que desconecta al cliente de la red mesh
    def borrar_cliente(self, macNodo):
        for nodo in self.nodosConectados.get_lista():
            try:
                conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                conexion.connect((nodo.get_ip(), nodo.get_puerto()))
                conexion.send(('DEL ' + macNodo).encode('utf-8'))
                conexion.close()
            except:
                pass
        indiceNodo = self.nodosConectados.buscar_nodo(macNodo)
        datosBorrado = self.nodosConectados.eliminar_nodo(indiceNodo)
        print('Se elimino el cliente: ' + datosBorrado.get_mac())


    #Funcion principal que esta en la escucha de conexiones o desconexiones en la red
    def registro(self):
        # Valores del socket
        dataConection = (self.datosNodo.get_ip(), self.datosNodo.get_puerto())

        # Creamos el servidor.
        # socket.AF_INET para indicar que utilizaremos Ipv4
        # socket.SOCK_STREAM para utilizar TCP/IP (no udp)
        socketRegistro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketRegistro.bind(dataConection)
        socketRegistro.listen()
        print("Esperando conexiones en %s:%s" % (self.datosNodo.get_ip(), self.datosNodo.get_puerto()))

        while True:
            cliente, direccion = socketRegistro.accept()
            print("Conexion establecida con %s:%s" % (direccion[0], direccion[1]))
            solicitud = cliente.recv(20).decode('utf-8')
            solicitud = solicitud.split()
            if solicitud[0] == 'CONNECT':
                hilo_nuevo_registro = Thread(target=self.agregar_cliente, args=(cliente
                                                                            , direccion))
                hilo_nuevo_registro.start()
                hilo_nuevo_registro.join()
            else:
                cliente.close()
                hilo_borrar_registro = Thread(target=self.borrar_cliente, args=(solicitud[1],))

                hilo_borrar_registro.start()
                hilo_borrar_registro.join()


#
#
# if __name__ == "__main__":
#     mesh = MeshPrincipal()
#     mesh.registro()
