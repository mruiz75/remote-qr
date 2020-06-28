import socket
from _thread import start_new_thread

import MAC_generator
import manejo_nodos as mn

class MeshPrincipal:

    def __init__(self):
        ip = '0.0.0.0'
        mac = MAC_generator.MACGenerator()
        puerto = 1505
        self.datosNodo = mn.CrearNodo(ip, mac.generate(), puerto)
        self.nodosConectados = mn.ListaNodos()

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

    def agregar_cliente(self, cliente, direccion):
        nodoCliente = self.crear_nodo_registro(direccion)
        string_datos = nodoCliente.to_string()
        codificacion = 'utf-8'

        for nodo in self.nodosConectados.get_lista():
            conexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            conexion.connect((nodo.get_ip(), nodo.get_puerto()))
            conexion.send(string_datos.encode(codificacion))
            conexion.close()
        cliente.send(nodoCliente.get_mac().encode(codificacion))
        cliente.send(self.datosNodo.to_string().encode(codificacion))
        cliente.send(self.nodosConectados.to_string().encode(codificacion))
        self.nodosConectados.agregar_nodo(nodoCliente)


    def registro(self):
        # Valores del socket
        dataConection = (self.datosNodo.get_ip(), self.datosNodo.get_puerto())

        # Creamos el servidor.
        # socket.AF_INET para indicar que utilizaremos Ipv4
        # socket.SOCK_STREAM para utilizar TCP/IP (no udp)
        socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketServidor.bind(dataConection)
        socketServidor.listen()
        print("Esperando conexiones en %s:%s" % (self.datosNodo.get_ip(), self.datosNodo.get_puerto()))

        while True:
            cliente, direccion = socketServidor.accept()
            print("Conexion establecida con %s:%s" % (direccion[0], direccion[1]))



if __name__ == "__main__":
    mesh = MeshPrincipal()
    #p = mesh.crear_nodo_registro(['0.0.0.0', 1616])
    #print(p.get_ip())
    #print(p.get_mac())
    #print(p.get_puerto())

    p = mesh.agregar_cliente(0, ['0.0.0.0', 1616])

'''
ip = "0.0.0.0"
puerto = 1505
dataConection = (ip, puerto)

#Creamos el servidor.
#socket.AF_INET para indicar que utilizaremos Ipv4
#socket.SOCK_STREAM para utilizar TCP/IP (no udp)
socketServidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketServidor.bind(dataConection) #Asignamos los valores del servidor
socketServidor.listen() #Asignamos el número máximo de conexiones

print("Esperando conexiones en %s:%s" %(ip, puerto))
cliente, direccion = socketServidor.accept()
print("Conexion establecida con %s:%s" %(direccion[0], direccion[1]))

#Bucle de escucha. En él indicamos la forma de actuar al recibir las tramas del cliente
while True:
    datos = cliente.recv(1024).decode('utf-8') #El número indica el número maximo de bytes
    if datos == "exit":
        cliente.send("exit".encode('utf-8'))
        break
    print("RECIBIDO: %s" %datos)
    cliente.sendall("-- Recibido --".encode('utf-8'))

print("------- CONEXIÓN CERRADA ---------")
socketServidor.close()
'''