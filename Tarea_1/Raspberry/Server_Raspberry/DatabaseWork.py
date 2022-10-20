import json
import datetime
import sqlite3 as sql

# Documentación https://docs.python.org/3/library/sqlite3.html

def dataSave(header, data):
    with sql.connect("DB.sqlite") as con:
        cur = con.cursor()
        current_datetime = datetime.datetime.now()
        if header["ID_protocol"] == 0:
            cur.execute('''insert into Datos (ID_device, MAC, Data1, Batt_level, Timestamp) values (?, ?, ?, ?, ?)''', (header["ID_device"], header["MAC"], current_datetime, json.dumps(data)))

        elif header["ID_protocol"] == 1:
            cur.execute('''insert into Datos (ID_device, MAC, Data1, Batt_level, Timestamp, Temp, Press, Hum, Co) values (?, ?, ?, ?, ?, ?, ?, ?, ?)''', (header["ID_device"], header["MAC"], current_datetime, json.dumps(data)))

        elif header["ID_protocol"] == 2:
            cur.execute('''insert into Datos (ID_device, MAC, Data1, Batt_level, Timestamp, Temp, Press, Hum, Co, RMS) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (header["ID_device"], header["MAC"], current_datetime, json.dumps(data)))
        
        elif header["ID_protocol"] == 3:
            cur.execute('''insert into Datos (ID_device, MAC, Data1, Batt_level, Timestamp, Temp, Press, Hum, Co, RMS, Amp_X, Frec_X, Amp_Y, Frec_Y, Amp_Z, Frec_Z) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (header["ID_device"], header["MAC"], current_datetime, json.dumps(data)))
        
        elif header["ID_protocol"] == 4:
            cur.execute('''insert into Datos (ID_device, MAC, Data1, Batt_level, Timestamp, Temp, Press, Hum, Co, Acc_X, Acc_Y, Acc_Z) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (header["ID_device"], header["MAC"], current_datetime, json.dumps(data)))

        if header["ID_protocol"] == 00: #ToDo definir este protocolo
            cur.execute('''insert into Config (ID_protocol, Transport_layer) values (?, ?)''', (header["ID_protocol"], header["Transport_layer"]))

        cur.execute('''insert into LOGS (ID_device, Transport_layer, Timestamp, ID_protocol) values (?, ?, ?, ?)''', (header["ID_device"], header["Transport_layer"], data["Timestamp"], header["ID_protocol"]))

        
        
        
    
    
#cur.execute('''insert into Datos (MAC, Transport_layer, Protocol, Data1) values (?, ?, ?, ?)''', (header["MAC"], header["status"], header["protocol"], json.dumps(data)))