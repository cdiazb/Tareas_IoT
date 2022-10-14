import socket
#from struct import unpack, pack

#from matplotlib import rc_params_from_file
from Desempaquetamiento import *
from TCPRaspServer import *
from UDPRaspServer import *

# "192.168.5.177"  # Standard loopback interface address (localhost)
TCP_HOST = "192.168.5.177"#"localhost"
TCP_PORT = 5000  # Port to listen on (non-privileged ports are > 1023)
UDP_IP = "192.168.5.177"# "localhost" 
UDP_PORT = 5010
STOP = True

s = socket.socket(socket.AF_INET, #internet
                    socket.SOCK_STREAM) #TCP
s.bind((TCP_HOST, TCP_PORT))
s.listen(5)
transport_layer = 0 #definiedo variable
print(f"Listening on {TCP_HOST}:{TCP_PORT}")

while True:
    conn, addr = s.accept()
    print(f'Conectado por alguien ({addr[0]}) desde el puerto {addr[1]}')
    transport_layer = 0 #ToDo obtener valor de la base de datos

    #config = response(False,transport_layer) #ToDo definir valores que empaqueta la funcion response

    #conn.send(config.encode())
    #data = conn.recv(1024)
    #ToDo manejar protocolo p00
    conn.close()

    while STOP: # ToDo definir como detener el loop
        if transport_layer == '0':
            TCP_connection(TCP_HOST,TCP_PORT)
            break

        elif transport_layer == '1':
            UDP_connection(UDP_IP,UDP_PORT)
            break

        else:
            print("Error: protocol doesnt exist")
            break

    