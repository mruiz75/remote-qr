class CrearNodo:

    def __init__(self, ip, mac, puerto):
        self.ip = ip
        self.mac = mac
        self.puerto = puerto

    def to_string(self):
        string_nodo = self.ip + ' ' + self.mac + ' ' + str(self.puerto) + ' '
        return string_nodo

    def get_ip(self):
        return self.ip

    def get_mac(self):
        return self.mac

    def get_puerto(self):
        return self.puerto

class ListaNodos:

    def __init__(self):
        self.listaNodos = []

    def agregar_nodo(self, nodo):
        self.listaNodos.append(nodo)

    def to_string(self):
        string_nodos = ''

        for i in self.listaNodos:
            string_nodos += i.to_string()

        return string_nodos

    def to_list(self, string_nodos):
        datos = string_nodos.split()

        for i in range(0, len(datos), 3):
            nodo = CrearNodo(datos[i], datos[i+1], int(datos[i+2]))
            self.agregar_nodo(nodo)

    def get_lista(self):
        return self.listaNodos

'''
nodo = CrearNodo('12', 'as', 34)
nodo2 = CrearNodo('13', 'hola', 35)
lista = ListaNodos()
lista.agregar_nodo(nodo)
lista.agregar_nodo(nodo2)
print(lista.get_lista()[1].get_ip())
str_prueba = lista.to_string()
print(str_prueba)
lista2 = ListaNodos()
lista2.to_list(str_prueba)
print(lista2.get_lista()[1].get_ip())
'''
