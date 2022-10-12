#include "sensors.c"
#include <math.h>
#include <stdlib.h>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"

// Largo de la data
uint16_t DATALENGTH[5] = {6, 16, 20, 44, 24016};

// Largo de los mensajes incluyendo el header
uint16_t messageLength(uint16_t protocol){
    return (uint16_t) (12 + DATALENGTH[protocol]);
}

// Genera el header de un mensaje, con la MAC, el protocolo, status, y el largo del mensaje.
// The C library function void *memcpy(void *dest, const void *src, size_t n) copies n 
// characters from memory area src to memory area dest.
char* header(uint8_t protocol, uint8_t transportLayer){
	// 12 bytes en total para el header
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
	memcpy((void*) &(head[8]), (void*) &transportLayer, 1);

	// 1 byte para ID Protocol
	memcpy((void*) &(head[9]), (void*) &protocol, 1);

	// 2 bytes para Length Message
	uint16_t dataLen = DATALENGTH[protocol];
	memcpy((void*) &(head[10]), (void*) &dataLen, 2);

	return head;
}

// Creamos el mensaje dependiendo del protocolo que necesitamos y la capa de transporte(TCP o UDP)
char* mensaje(uint8_t protocol, uint8_t transportLayer){
	// Alocamos memoria para el mensaje
	char* mnsj = malloc(messageLength(protocol));
	// Marcamos el final del mensaje
	mnsj[messageLength(protocol)-1]= '\0';
	// Creamos el header y copiamos su contenido al mensaje y liberamos memoria
	char* hdr = header(protocol, transportLayer);
	memcpy((void*) mnsj, (void*) hdr, 12);
	free(hdr);

	char* data;
	// Dependiendo del protocolo crearemos los datos sinteticos, protocolos pueden ser o-4 de no ser ninguno de estos se considera como protocolo 0.
	switch (protocol) {
		case 0:
			data = dataprotocol0();
			break;
		case 1:
			data = dataprotocol1();
			break;
		case 2:
			data = dataprotocol2();
			break;
		case 3:
			data = dataprotocol3();
			break;
        case 4:
			data = dataprotocol4();
			break;
		default:
			data = dataprotocol0();
			break;
	}

	// Copiamos los contenidos de data al mensaje y luego liberamos memoria
	memcpy((void*) &(mnsj[12]), (void*) data, DATALENGTH[protocol]);
	free(data);
	
	// Entregamos el mensaje
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