#include <math.h>
#include <stdlib.h>
#include <stdint.h>

// Funcion para calcular un valor random entre floats
float floatrand(float min, float max){
    return min + (float)rand()/(float)(RAND_MAX/(max-min));
}

// Funcion para calcular RMS. 4 bytes
float rms(float x, float y, float z){
    return sqrtf(powf(x,2) + powf(y,2) + powf(z,2));
}

// Generador de datos sinteticos para el sensor de bateria. 1 byte
uint8_t batt_sensor(){
    return (uint8_t) (1 + rand() % 100);
}

// Generador de datos sinteticos para el acelerometro, 2000 datos por eje. 8000 bytes cada uno
// Aceleracion en x
float* acc_sensor_x(){
    float* arr = malloc(2000 * sizeof(float));
    for (int i = 0 ; i < 2000; i++){
        arr[i] = 2 * sin(0.002 * M_PI * rand());
    }
    return arr;
}

// Aceleracion en y
float* acc_sensor_y(){
    float* arr = malloc(2000 * sizeof(float));
    for (int i = 0; i < 2000; i++ ){
        arr[i] = 3 * cos(0.002 * M_PI * rand());
    }
    return arr;
}

// Aceleracion en z
float* acc_sensor_z(){
    float* arr = malloc(2000 * sizeof(float));
    for (int i = 0; i < 2000; i++ ){
        arr[i] = 10 * sin(0.002 * M_PI * rand());
    }
    return arr;
}


// Generador de datos sinteticos para el sensor THPC
// Temperatura, se podria codificar los valores para usar un datatype menos costoso. 1 byte **
float thpc_sensor_temp(){
    return floatrand(5.0, 30.0);
}

// Humedad. 1 byte
uint8_t thpc_sensor_hum(){
    return 30 + rand() % 51;
}

// Presion, podemos codificar los valores para usar un datatype menos costoso. 4 bytes **
uint16_t thpc_sensor_pres(){
    return 1000 + rand() % 201;
}

// CO2, se podria codificar los valores para usar un datatype menos costoso. 4 bytes
float thpc_sensor_co2(){
    return floatrand(30.0, 200.0);
}


// Generador de datos sinteticos para el acelerometro kpi
// Amplitud en x. 4 bytes
float acc_kpi_ampx(){
    return floatrand(0.0059, 0.12);
}

// Amplitud en y. 4 bytes
float acc_kpi_ampy(){
    return floatrand(0.0041, 0.11);
}

// Amplitud en z. 4 bytes
float acc_kpi_ampz(){
    return floatrand(0.008, 0.15);
}

// Frecuencia en x. 4 bytes
float acc_kpi_frecx(){
    return floatrand(29.0, 31.0);
}

// Frecuencia en y. 4 bytes
float acc_kpi_frecy(){
    return floatrand(59.0, 61.0);
}

// Frecuencia en z. 4 bytes
float acc_kpi_frecz(){
    return floatrand(89.0, 91.0);
}