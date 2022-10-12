import socket

from Desempaquetamiento import *

# "192.168.5.177"  # Standard loopback interface address (localhost)
#HOST = "192.168.5.177"#"localhost"
#PORT = 5000  # Port to listen on (non-privileged ports are > 1023)

def TCP_connection(host, port):
    s = socket.socket(socket.AF_INET, #internet
                    socket.SOCK_STREAM) #TCP
    s.bind((host, port))
    s.listen(5)
    print(f"Listening on {host}:{port}")
    while True:
        conn, addr = s.accept()
        print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')
        paquetes = []
        while True:
            try:
                data = conn.recv(1024)
                if data == b'':
                    break
                header = getHeader(data)
                if header['protocol'] != '5':
                    parseData(header,data)
                else:
                    paquetes.append(data)
                    #ToDo definir como manejar paquetes fragmentados
            except ConnectionResetError:
                break

            print(f"Recibido {data}")
            #conn.send(data.encode())

        conn.close()
        print('Desconectado')
