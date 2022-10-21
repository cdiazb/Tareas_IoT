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
        paquetes = {}
        index = []
        while True:
            try:
                data = conn.recv(1024)
                if data == b'':
                    break

                header = getHeader(data)

                if  header['ID_protocol'] != 4:
                    parseData(header,data[12:])
                else:
                    while len(index) != 24:
                        i = getData(data[12:])
                        if i not in index:
                            if i == 0:
                                paquetes[i] = data[12:]
                            else:
                                paquetes[i] = data[13:] #ToDo probablemente no basta con guardar data directamente en el dict
                            index.append(i)
                    
                    index.sort() #se ordenan los indices, por si acaso
                    reconstruct_data=''
                    for i in index:
                        reconstruct_data += paquetes[i] #se concatenan fragmentos de paquetes

                    paquetes.clear()
                    index.clear()
                    parseData(header,reconstruct_data) #se parsean los datos y se guardan en la base de datos
                        
            except ConnectionResetError:
                break
            conn.send("Recibido".encode())
        conn.close()
        print('Desconectado')
    return None
