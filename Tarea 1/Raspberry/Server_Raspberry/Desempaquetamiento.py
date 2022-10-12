from struct import unpack, pack
import traceback
from DatabaseWork import * 

# Documentación struct unpack,pack :https://docs.python.org/3/library/struct.html#
'''
Estas funciones se encargan de parsear y guardar los datos recibidos.
Usamos struct para pasar de un array de bytes a una lista de numeros/strings. (https://docs.python.org/3/library/struct.html)
(La ESP32 manda los bytes en formato little-endian, por lo que los format strings deben empezar con <)

-dataSave: Guarda los datos en la BDD
-response: genera un OK para mandar de vuelta cuando se recibe un mensaje, con posibilidad de pedir que se cambie el status/protocol
-protUnpack: desempaca un byte array con los datos de un mensaje (sin el header)
-headerDict: Transforma el byte array de header (los primeros 10 bytes de cada mensaje) en un diccionario con la info del header
-dataDict: Transforma el byta array de datos (los bytes luego de los primeros 10) en un diccionario con los datos edl mensaje

'''

    
def response(change:bool=False, transport_layer:int=255, protocol:int=255):
    OK = 1
    CHANGE = 1 if change else 0
    return pack("<BBBB", OK, CHANGE, transport_layer, protocol)

def getHeader(packet):
    header = packet[:12]
    header = headerDict(header)
    return header

def parseData(header, packet):
    data = packet[12:]
    dataD = dataDict(header["protocol"], data)
    if dataD is not None:
        dataSave(header, dataD)
        
    return None if dataD is None else {**header, **dataD}

def protUnpack(protocol:int, data):
    protocol_unpack = ["<B", "<BB4B", "<BB4BB4BBf", "<BB4BB4BBff", "<BB4BB4BBff6f", "<BB4BB4BBf2000f2000f2000f"] #ToDo verificar el formato correcto para timestamp
    return unpack(protocol_unpack[protocol], data)

def headerDict(data):
    ID_Device, M1, M2, M3, M4, M5, M6, transport_layer, protocol, leng_msg = unpack("<2B6BBBH", data)
    MAC = ".".join([hex(x)[2:] for x in [M1, M2, M3, M4, M5, M6]])
    return {"ID_Device":ID_Device, "MAC":MAC, "protocol":protocol, "transport_layer":transport_layer, "length":leng_msg}

def dataDict(protocol:int, data):
    if protocol not in [0, 1, 2, 3, 4, 5]:
        print("Error: protocol doesnt exist")
        return None
    def protFunc(protocol, keys):
        def p(data):
            unp = protUnpack(protocol, data)
            return {key:val for (key,val) in zip(keys, unp)}
        return p
    p00 = ["OK"]
    p0 = ["val" ,"Batt_level", "Timestamp"]
    p1 = ["val" ,"Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co"]
    p2 = ["val" ,"Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS"]
    p3 = ["val" ,"Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "RMS", "Amp_X", "Frec_X", "Amp_Y", "Frec_Y", "Amp_Z", "Frec_Z"]
    p4 = ["val" ,"Batt_level", "Timestamp", "Temp", "Pres", "Hum", "Co", "Acc_X", "Acc_Y", "Acc_Z"]
    p = [p00, p0, p1, p2, p3, p4]

    try:
        return protFunc(protocol, p[protocol])(data)
    except Exception:
        print("Data unpacking Error:", traceback.format_exc())
        return None