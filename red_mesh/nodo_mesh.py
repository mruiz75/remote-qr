import socket #util de red y conexion
import argparse

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

if __name__ == "__main__":
    nose()
    #parametros = datos()
    #print(parametros.ip)