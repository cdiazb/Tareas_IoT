'''create = CREATE TABLE Info (
    MessageId TEXT PRIMARY KEY,
    MAC TEXT NOT NULL,
    Status INTEGER NOT NULL,
    Protocol INTEGER NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    Data1 INTEGER,
    Data2 FLOAT,
    Data3 FLOAT
    
);'''

create_datos = '''CREATE TABLE Datos (
    ID_device TEXT,
    MAC TEXT NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    Data1 INTEGER NOT NULL,
    Batt_level INTEGETR NOT NULL,
    Temp FLOAT,
    Press INTEGER,
    Hum INTEGER,
    Co FLOAT,
    RMS FLOAT,
    Amp_X FLOAT,
    Frec_X FLOAT,
    Amp_Y FLOAT,
    Frec_Y FLOAT,
    Amp_Z FLOAT,
    Frec_Z FLOAT,
    Acc_X BLOB,
    Acc_Y BLOB,
    Acc_Z BLOB,
    PRIMARY KEY (ID_device, Timestamp)
);'''

create_logs = '''CREATE TABLE LOGS (
    ID_device TEXT PRIMARY KEY,
    Transport_layer INTEGER NOT NULL,
    Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    ID_protocol INTEGER NOT NULL,
    FOREIGN KEY (ID_device, Timestamp) REFERENCES Datos(ID_device, Timestamp)
);'''

create_config = '''CREATE TABLE Config (
    ID_protocol TEXT,
    Transport_layer INTEGER NOT NULL,
);'''

import sqlite3 as sql


conn = sql.connect("DB.sqlite")
cur = conn.cursor()
cur.execute(create_datos)
cur.execute(create_logs)
cur.execute(create_config)
conn.close()

# inicializa la BDD