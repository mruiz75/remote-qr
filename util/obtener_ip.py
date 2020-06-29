import socket

class IP:

    def __init__(self):
        self.ip_publica = self._get_ip_publica()
        self.ip_privada = self._get_ip_privada()

    def _get_ip_privada(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def _get_ip_publica(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()

        return ip

ips = IP()
print(ips.ip_privada)
print(ips.ip_publica)
