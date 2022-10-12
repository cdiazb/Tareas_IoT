#include "sensors.c"
#include <math.h>
#include <stdlib.h>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"

// Genera el header de un mensaje, con la MAC, el protocolo, status, y el largo del mensaje.
// The C library function void *memcpy(void *dest, const void *src, size_t n) copies n 
// characters from memory area src to memory area dest.
char* header(char protocol, char transportLayer){
	char* head = malloc(12);

	// 2 bytes para ID Device
    char ID = 'D1'
    memcpy((void*) &(head[0]), (void*) MACaddrs, 2);
	
	// 6 bytes para MAC Adress
	uint8_t* MACaddrs = malloc(6);
	esp_efuse_mac_get_default(MACaddrs);
	memcpy((void*) &(head[2]), (void*) MACaddrs, 6);
	free(MACaddrs);

	// 1 byte para Transport Layer
    head[8]= transportLayer;

	// 1 byte para ID Protocol
	head[9]= protocol;

	// 2 bytes para Length Message
	unsigned short dataLen = dataLength(protocol);
	memcpy((void*) &(head[10]), (void*) &dataLen, 2);

	return head;
}

// Largo de los mensajes incluyendo el header
unsigned short lengmsg[5] = {6, 16, 20, 44, 24016};

unsigned short  (char protocol){
    return lengmsg[ (unsigned int) protocol]-1;
}

unsigned short messageLength(char protocol){
    return 13 + dataLength(protocol);
}

char* mensaje (char protocol, char transportLayer){
	char* mnsj = malloc(messageLength(protocol));
	mnsj[messageLength(protocol)-1]= '\0';
	char* hdr = header(protocol, transportLayer);
	char* data;
	switch (protocol) {
		case 0:
			data = dataprotocol00();
			break;
		case 1:
			data = dataprotocol0();
			break;
		case 2:
			data = dataprotocol1();
			break;
		case 3:
			data = dataprotocol2();
			break;
        case 4:
			data = dataprotocol3();
			break;
        case 5:
			data = dataprotocol4();
			break;
		default:
			data = dataprotocol0();
			break;
	}
	memcpy((void*) mnsj, (void*) hdr, 12);
	memcpy((void*) &(mnsj[12]), (void*) data, dataLength(protocol));
	free(hdr);
	free(data);
	return mnsj;
}

// Arma un paquete para el protocolo de inicio, que busca solo respuesta
char* dataprotocol00(){
    char* msg = malloc(dataLength(0));
    msg[0] = 1;
    return msg;
}

// Arma un paquete para el protocolo 0, con la bateria
char* dataprotocol0(){
    
    char* msg = malloc(dataLength(1));
    float batt = batt_sensor();
    msg[0] = batt;
    long t = 0;
    memcpy((void*) &(msg[1]), (void*) &t, 4);
    return msg;
}

'''
char* dataprotocol1(){
    
    char* msg = malloc(dataLength(2));

    float batt = batt_sensor();
    msg[0] = batt;


    int t = 0;
    memcpy((void*) &(msg[1]), (void*) &t, 4);

    char temp = THPC_sensor_temp();
    msg[5] = temp;


    float press = THPC_sensor_pres();
    memcpy((void*) &(msg[6]), (void*) &press, 4);

    char hum = THPC_sensor_hum();
    msg[10] = hum;

    float co = THPC_sensor_co();
    memcpy((void*) &(msg[11]), (void*) &co, 4);

    return msg;
}
'''