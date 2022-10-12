from email import header
import socket
from Desempaquetamiento import *

#UDP_IP = "192.168.5.177"# "localhost" 
#UDP_PORT = 5010


def UDP_connection(host, port):
    sUDP = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
    sUDP.bind((host, port))


    print(f"Listening for UDP packets in {host}:{port}")
    while True:
        paquetes = []
        while True:
            payload, client_address = sUDP.recvfrom(1)
            if payload == b'':
                print("Error: empty payload")
                pass
            header = getHeader(payload)
            if header['protocol'] != '5':
                parseData(header,payload)
            
            else:
                paquetes.append(payload) 
                #ToDo definir como manejar paquetes fragmentados
            print("Echoing data back to " + str(client_address) + ": " + payload)
            sent = sUDP.sendto(payload, client_address)