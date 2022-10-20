from struct import unpack, pack
from pickle import dumps, loads
import datetime
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

    
def response(ID_protocol:int, transport_layer:int):
    return pack("<BB", ID_protocol,transport_layer)

def getHeader(packet):
    header = packet[:12]
    header = headerDict(header)
    print(header)
    return header

def parseData(header, packet):
    dataD = dataDict(header["ID_protocol"], packet)
    if dataD is not None:
        dataSave(header, dataD)
        print(header)
        print(dataD)
        
    return None if dataD is None else {**header, **dataD}

def protUnpack(protocol:int, data):
    #"<B", 
    protocol_unpack = ["<BB4B", "<BB4Bf4BBf", "<BB4Bf4BBff", "<BB4Bf4BBff6f", "<BB4Bf4BBf2000f2000f2000f"] #ToDo TimeStamp vendra vacio. llenarlo al momento de guardar la info en la base de datos
    return unpack(protocol_unpack[protocol], data)

def headerDict(data):
    ID_Device, M1, M2, M3, M4, M5, M6, transport_layer, protocol, leng_msg = unpack("<2B6BBB2B", data)#ToDo revisar formato de unpacking
    MAC = ".".join([hex(x)[2:] for x in [M1, M2, M3, M4, M5, M6]])
    return {"ID_device":ID_Device, "MAC":MAC, "ID_protocol":protocol, "Transport_layer":transport_layer, "length":leng_msg}

def dataDict(protocol:int, data):
    #, 5
    if protocol not in [0, 1, 2, 3, 4]:
        print("Error: protocol doesnt exist")
        return None
    def protFunc(protocol, keys):
        def p(data):
            unp = protUnpack(protocol, data)
            data_dict = {}
            for (key,val) in zip(keys,unp):
                if key == "Timestamp":
                    data_dict[key] = datetime.datetime.now()
                if key in ["Acc_X", "Acc_Y", "Acc_Z"]:
                    data_dict[key] = dumps(val)
                else:
                    data_dict[key] = val
            return data_dict
        return p
    p00 = ["OK"] #ToDo definir este protocolo 00 y eliminar timestamp
    p0 = ["Data1" ,"Batt_level", "Timestamp"]
    p1 = ["Data1" ,"Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co"]
    p2 = ["Data1" ,"Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co", "RMS"]
    p3 = ["Data1" ,"Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co", "RMS", "Amp_X", "Frec_X", "Amp_Y", "Frec_Y", "Amp_Z", "Frec_Z"]
    p4 = ["Data1" ,"Batt_level", "Timestamp", "Temp", "Press", "Hum", "Co", "Acc_X", "Acc_Y", "Acc_Z"]
    #p00, 
    p = [p0, p1, p2, p3, p4]

    try:
        return protFunc(protocol, p[protocol])(data)
    except Exception:
        print("Data unpacking Error:", traceback.format_exc())
        return None