/*
 * gps.c
 *
 *  Created on: 10 janv. 2023
 *      Author: scant
 */


#include "gps.h"


#include "cmsis_os.h"
#include "main.h"
#include "math.h"
#include "string.h"

uint8_t rxBufferGPS[RX_BUFFER_SIZE];
uint8_t rx_index = 0;
long double latitude, longitude;

#define GPS_UART &huart2
void configure_gps();
void ublox_send_message(const char *message, size_t message_length);
void parse_nmea_sentence(uint8_t *sentence) ;

CordoGPS extract_lat_long_from_gngga(const uint8_t *gngga_buffer){
	CordoGPS result;
	long double lat, lon;
	    int lat_deg, lon_deg;
	    long double lat_min, lon_min;
	    char lat_dir, lon_dir;
	    int n;

	    n = sscanf(gngga_buffer, "GNGGA,%*f,%Lf,%c,%Lf,%c,%*d,%*d,%*f,%*f,%*c,%*f,%*c,%*f,%*c,%*f,%*c", &lat, &lat_dir, &lon, &lon_dir);
	    if (n != 4) {
	    	result.latitude = 0;
			result.longitude = 0;
			return result;	        }

	        lat_deg = (int)(lat / 100);
	        lat_min = lat - lat_deg * 100;
	        lon_deg = (int)(lon / 100);
	        lon_min = lon - lon_deg * 100;

	        result.latitude = lat_deg + lat_min / 60;
	        result.longitude = lon_deg + lon_min / 60;

	        if (lat_dir == 'S') {
	        	result.latitude = -result.latitude;
	        }

	        //*latitude = *latitude / 10;
	        //*longitude = *longitude / 10;
	        if (lon_dir == 'W') {
	        	result.longitude = -result.longitude;
	        }

	        return result;
	}


void GPS_RxCpltCallback(){
	char received_char = rxDataGPS;
	    if (received_char == '$') {
	        rx_index = 0;
	    } else if (received_char == '\n') {
	    	rxBufferGPS[rx_index] = '\0';
	        parse_nmea_sentence(rxBufferGPS);
	        rx_index = 0;
	    } else {
	    	rxBufferGPS[rx_index] = rxDataGPS;
	        rx_index = (rx_index + 1) % RX_BUFFER_SIZE;

	    }

	    HAL_UART_Receive_IT(&huart2, &rxDataGPS, 1);

	/*
	static int indexRxBuffer = 0;

	if (rxDataGPS != '\n')
	{
		UART2_rxBuffer[indexRxBuffer] = rxDataGPS;
		indexRxBuffer++;
	}
	else if (rxDataGPS == '\n')
	{
		processData(indexRxBuffer);
		//RAZ Buffer
		for (int i = 0 ; i<RX_BUFFER_SIZE;i++)
		{
			UART2_rxBuffer[i]=0;
		}
		indexRxBuffer = 0;


	}
	HAL_UART_Receive_IT (&huart2, &rxDataGPS, 1);
	*/

}
long double round_precision(long double value, int precision) {
    long double factor = powl(10, precision);
    return roundl(value * factor) / factor;
}

void parse_nmea_sentence(uint8_t *sentence) {
    // Exemple: extraction de la latitude et de la longitude d'une trame GGA
    if (strncmp((char*)sentence, "GNGGA", (uint) 5) == 0) {
    	long double lat, lon;
    	CordoGPS GPScalcul;
    	//extract_lat_long_from_gngga(rxBufferGPS, &latitude, &longitude);
    	GPScalcul = extract_lat_long_from_gngga(rxBufferGPS);
       memcpy(&batonomeData.positionGPS,&GPScalcul,sizeof(GPScalcul));
        //batonomeData.positionGPS.latitude = GPScalcul;
       // batonomeData.positionGPS.longitude = lon;

    }
}
enum enumstatecommandGPS stateCommandGPS = INITGPS;;


void gpsTask()
{
	for(;;)
	{
		switch (stateCommandGPS)
		        {
		        case INITGPS:
		        	//Démarrage de la PWM
		        	configure_gps();
		        	stateCommandGPS = RUNNING;

		        	break;
		        case RUNNING:

		        	break;

			//Code
	}
}
}

void ublox_send_message(const char *message, size_t message_length) {
    char ubx_header[] = {0xB5, 0x62}; // En-tête UBX
   // HAL_UART_Transmit(GPS_UART, (uint8_t *)ubx_header, 2, 100);
    HAL_UART_Transmit(GPS_UART, (uint8_t *)message, message_length, 100);
    osDelay(200);

}

void configure_gps() {
	uint8_t ubx_mon_ver[] = {0xB5, 0x62, 0x0A, 0x04, 0x00, 0x00, 0x0E, 0x34};
	ublox_send_message(ubx_mon_ver, sizeof(ubx_mon_ver));

    // Configurer UART1 pour 115200 bauds
    /*const char uart_config[] = {0x06, 0x00, 0x14, 0x00, 0x01, 0x00, 0x00, 0x00, 0xD0, 0x08, 0x00, 0x00, 0x00, 0xC2, 0x01, 0x00, 0x07, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00};
    ublox_send_message(uart_config,sizeof(uart_config));*/

    // Activer les trames NMEA GNGGA et GNVTG pour UART1 et USB
//    const char gngga_config[] = {0x06, 0x01, 0x08, 0x00, 0xF0, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01};
//    ublox_send_message(gngga_config,sizeof(gngga_config));
//
//    const char gnvtg_config[] = {0x06, 0x01, 0x08, 0x00, 0xF0, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01};
//    ublox_send_message(gnvtg_config,sizeof(gnvtg_config));
//
//    // Configurer la fréquence des trames GNGGA et GNVTG pour 1 Hz
//    const char rate_config[] = {0x06, 0x08, 0x06, 0x00, 0xE8, 0x03, 0x01, 0x00, 0x01, 0x00};
//    ublox_send_message(rate_config,sizeof(rate_config));
//
//    // Désactiver les trames NMEA GQGSV pour UART1 et USB
//    const char gqgsv_disable[] = {0x06, 0x01, 0x08, 0x00, 0xF0, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
//    ublox_send_message(gqgsv_disable,sizeof(gqgsv_disable));

    const uint8_t gngll_disable[] = {0xB5, 0x62, 0x06, 0x8A, 0x0E, 0x00, 0x01, 0x00, 0x00, 0x00, 0xDD, 0x00, 0x91, 0x20, 0x00, 0x00, 0x00, 0x00, 0x4E, 0x1A};
    ublox_send_message(gngll_disable, sizeof(gngll_disable));
}




void gps_Init()
{
	/* Definitions for zigbee_com */
	osThreadId_t gpsHandle;
	const osThreadAttr_t gps_attributes = {
	  .name = "gps",
	  .stack_size = 128 * 4,
	  .priority = (osPriority_t) osPriorityNormal,
	};

	//gpsHandle = osThreadNew(gpsTask, NULL, &gps_attributes);
}
