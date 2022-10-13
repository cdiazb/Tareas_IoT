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
        paquetes = {}
        index = []
        while True:
            payload, client_address = sUDP.recvfrom(1)
            if payload == b'':
                print("Error: empty payload")
                pass
            header = getHeader(payload)
            if header['protocol'] != '4':
                parseData(header,payload[12:])
            
            else:
                if header['val'] != 'f':
                    if header['val'] is not index:
                        index.append(header['val'])
                        paquetes[header['val']] = payload[12:]
                else:
                    index.sort() #se ordenan los indices, por si acaso
                    index.append(len(index)) #se agrega el ultimo indice f
                    reconstruct_data=''
                    for i in index:
                        reconstruct_data += paquetes[i] #se concatenan fragmentos de paquetes
                    
                    parseData(header,reconstruct_data) #se parsean los datos y se guardan en la base de datos
                #ToDo definir como manejar paquetes fragmentados
            print("Echoing data back to " + str(client_address) + ": " + payload)
            #sent = sUDP.sendto(payload, client_address)