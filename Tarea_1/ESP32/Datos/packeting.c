
#include "sensors.c"
#include <math.h>
#include <stdlib.h>
#include <stdint.h>
#include "esp_system.h"
#include "esp_mac.h"
#include "esp_log.h"
#include <string.h>

#define PROTOCOL_TCP 0
#define PROTOCOL_UDP 1


// Largo de la data, se agrego un bit para los protocolos 1-4 para que calce el dato de humedad
uint16_t DATALENGTH[5] = {6, 17, 21, 45, 24017};

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
    char* ID = "D1";
    memcpy((void*) &(head[0]), (void*) ID, 2);
	
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
// Funciones para crear los paquetes de los distintos protocolos, dejaremos que el servidor se encargue del timestamp por lo que lo dejaremos como 0.
// Arma un paquete para el protocolo 0: Bateria y timestamp
char* dataprotocol0(){
	char* mssg = malloc(DATALENGTH[0]);
	uint8_t data_1 = 1;
	uint8_t bateria = batt_sensor();
	uint32_t timestamp = 0;
	
	mssg[0] = data_1;
	mssg[1] = bateria;
	memcpy((void*) &(mssg[2]), (void*) &timestamp, 4);
	return mssg;
}

// Arma un paquete para el protocolo 1: Bateria, timestamp, temperatura, presion, humedad y CO2
char* dataprotocol1(){
	char* mssg = malloc(DATALENGTH[1]);
	uint8_t data_1 = 1;
	uint8_t bateria = batt_sensor();
	uint32_t timestamp = 0;
	float temperatura = thpc_sensor_temp();
	uint16_t presion = thpc_sensor_pres();
	uint8_t humedad = thpc_sensor_hum();
	float co2 = thpc_sensor_co2();
	
	mssg[0] = data_1;
	mssg[1] = bateria;
	memcpy((void*) &(mssg[2]), (void*) &timestamp, 4);
	memcpy((void*) &(mssg[6]), (void*) &temperatura, 4);
	memcpy((void*) &(mssg[10]), (void*) &presion, 2);
	mssg[12] = humedad;
	memcpy((void*) &(mssg[13]), (void*) &co2, 4);
	return mssg;
}

// Arma un paquete para el protocolo 2: Bateria, timestamp, temperatura, presion, humedad, CO2 y RMS
char* dataprotocol2(){
	char* mssg = malloc(DATALENGTH[2]);
	uint8_t data_1 = 1;
	uint8_t bateria = batt_sensor();
	uint32_t timestamp = 0;
	float temperatura = thpc_sensor_temp();
	uint16_t presion = thpc_sensor_pres();
	uint8_t humedad = thpc_sensor_hum();
	float co2 = thpc_sensor_co2();
	float root = rms(acc_kpi_ampx(),acc_kpi_ampy(),acc_kpi_ampz());
	
	mssg[0] = data_1;
	mssg[1] = bateria;
	memcpy((void*) &(mssg[2]), (void*) &timestamp, 4);
	memcpy((void*) &(mssg[6]), (void*) &temperatura, 4);
	memcpy((void*) &(mssg[10]), (void*) &presion, 2);
	mssg[12] = humedad;
	memcpy((void*) &(mssg[13]), (void*) &co2, 4);
	memcpy((void*) &(mssg[17]), (void*) &root, 4);
	return mssg;
}

// Arma un paquete para el protocolo 3: Bateria, timestamp, temperatura, presion, humedad, CO2, RMS, amplitudes y frecuencias
char* dataprotocol3(){
	char* mssg = malloc(DATALENGTH[2]);
	uint8_t data_1 = 1;
	uint8_t bateria = batt_sensor();
	uint32_t timestamp = 0;
	float temperatura = thpc_sensor_temp();
	uint16_t presion = thpc_sensor_pres();
	uint8_t humedad = thpc_sensor_hum();
	float co2 = thpc_sensor_co2();
	float ampx = acc_kpi_ampx();
	float ampy = acc_kpi_ampy();
	float ampz = acc_kpi_ampz();
	float root = rms(ampx,ampy,ampz);
	float frecx = acc_kpi_frecx();
	float frecy = acc_kpi_frecy();
	float frecz = acc_kpi_frecz();
	
	mssg[0] = data_1;
	mssg[1] = bateria;
	memcpy((void*) &(mssg[2]), (void*) &timestamp, 4);
	memcpy((void*) &(mssg[6]), (void*) &temperatura, 4);
	memcpy((void*) &(mssg[10]), (void*) &presion, 2);
	mssg[12] = humedad;
	memcpy((void*) &(mssg[13]), (void*) &co2, 4);
	memcpy((void*) &(mssg[17]), (void*) &root, 4);
	memcpy((void*) &(mssg[21]), (void*) &ampx, 4);
	memcpy((void*) &(mssg[25]), (void*) &frecx, 4);
	memcpy((void*) &(mssg[29]), (void*) &ampy, 4);
	memcpy((void*) &(mssg[33]), (void*) &frecy, 4);
	memcpy((void*) &(mssg[37]), (void*) &ampz, 4);
	memcpy((void*) &(mssg[41]), (void*) &frecz, 4);
	return mssg;
}

// Arma un paquete para el protocolo 4: Bateria, timestamp, temperatura, presion, humedad, CO2 y aceleraciones
char* dataprotocol4(){
	char* mssg = malloc(DATALENGTH[4]);
	uint8_t data_1 = 1;
	uint8_t bateria = batt_sensor();
	uint32_t timestamp = 0;
	float temperatura = thpc_sensor_temp();
	uint16_t presion = thpc_sensor_pres();
	uint8_t humedad = thpc_sensor_hum();
	float co2 = thpc_sensor_co2();
	float* accx = acc_sensor_x();
	float* accy = acc_sensor_y();
	float* accz = acc_sensor_z();

	mssg[0] = data_1;
	mssg[1] = bateria;
	memcpy((void*) &(mssg[2]), (void*) &timestamp, 4);
	memcpy((void*) &(mssg[6]), (void*) &temperatura, 4);
	memcpy((void*) &(mssg[10]), (void*) &presion, 2);
	mssg[12] = humedad;
	memcpy((void*) &(mssg[13]), (void*) &co2, 4);
	memcpy((void*) &(mssg[17]), (void*) accx, 8000);
	memcpy((void*) &(mssg[8017]), (void*) accy, 8000);
	memcpy((void*) &(mssg[1617]), (void*) accz, 8000);

	return mssg;
}

// Arma un paquete para el protocolo de inicio, que busca solo respuesta
char* dataprotocol00(){
    char* mssg = malloc(1);
    mssg[0] = 1;
    return mssg;
}
// Creamos el mensaje dependiendo del protocolo que necesitamos y la capa de transporte(TCP o UDP)
char* create_message(uint8_t protocol, uint8_t transportLayer){
	// Alocamos memoria para el mensaje
	char* mnsj = malloc(messageLength(protocol));
	// Creamos el header, copiamos su contenido al mensaje y liberamos memoria
	char* hdr = header(protocol, transportLayer);
	memcpy((void*) mnsj, (void*) hdr, 12);
	free(hdr);

	char* data;
	// Dependiendo del protocolo crearemos los datos sinteticos, protocolos pueden ser 0-4 de no ser ninguno de estos se considerara  protocolo 0.
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
