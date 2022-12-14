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
            if  header['ID_protocol'] != '4':
                print("protocolo: "+  header['ID_protocol'])
                parseData(header,payload[12:])
            
            else:
                print("protocolo: "+  header['ID_protocol'])
                while len(index) != 24:
                    if header['Data1'] not in index:
                        paquetes[header['Data1']] = payload[12:] #ToDo probablemente no basta con guardar data directamente en el dict
                        index.append(header['Data1'])
                    
                index.sort() #se ordenan los indices, por si acaso
                reconstruct_data=''
                for i in index:
                    reconstruct_data += paquetes[i] #se concatenan fragmentos de paquetes
                    paquetes.clear()
                    index.clear()
                
                parseData(header,reconstruct_data) #se parsean los datos y se guardan en la base de datos
            print("Echoing data back to " + str(client_address) + ": " + payload)
            #sent = sUDP.sendto(payload, client_address)
    
    return None