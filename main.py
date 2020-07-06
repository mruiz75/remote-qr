import capa1.generador_trama
from capa1.generador_qr import *
from capa1.interpretador_qr import *

def main():
    version = "01"
    ip = "192.168.112.011"
    mac = "F8FFDDEEAA00"
    filename1 = "/Users/Manuel/Documents/TEC/2020/Redes/Proyectos/remote-qr/capa1/texto1.txt"
    filename2 = "/Users/Manuel/Documents/TEC/2020/Redes/Proyectos/remote-qr/capa1/prueba.pdf"
    filename3 = "/Users/Manuel/Documents/TEC/2020/Redes/Proyectos/remote-qr/capa1/img.png"
    #texto_a_qr(version, ip, mac, filename)
    file_a_qr(version, ip, mac, filename1)

    #leer_png()
    leer_qr()

main()