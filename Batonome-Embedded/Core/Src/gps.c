/*
 * gps.c
 *
 *  Created on: 10 janv. 2023
 *      Author: scant
 */


#include "gps.h"


#include "cmsis_os.h"
#include "main.h"

uint8_t rxBufferGPS[RX_BUFFER_SIZE];
uint8_t rx_index = 0;

#define GPS_UART &huart2
void configure_gps();
void ublox_send_message(const char *message, size_t message_length);
void GPS_RxCpltCallback(){
	char received_char = rxDataGPS;
	    if (received_char == '$') {
	        rx_index = 0;
	    } else if (received_char == '\n') {
	    	rxBufferGPS[rx_index] = '\0';
	        parse_nmea_sentence(rxBufferGPS);
	        rx_index = 0;
	    } else {
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

void parse_nmea_sentence(char *sentence) {
    // Exemple: extraction de la latitude et de la longitude d'une trame GGA
    if (strncmp(sentence, "GNGGA", 5) == 0) {
        char *token = strtok(sentence, ",");

        for (int i = 0; i < 9; i++) {
            token = strtok(NULL, ",");
            if (i == 1) {
                double latitude = atof(token) / 100.0;
                int degrees = (int)latitude;
                double minutes = (latitude - degrees) * 100.0;
                latitude = degrees + minutes / 60.0;
                // Stocker ou utiliser la latitude
            } else if (i == 3) {
                double longitude = atof(token) / 100.0;
                int degrees = (int)longitude;
                double minutes = (longitude - degrees) * 100.0;
                longitude = degrees + minutes / 60.0;
                // Stocker ou utiliser la longitude
            }
        }
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
    HAL_UART_Transmit(GPS_UART, (uint8_t *)ubx_header, 2, 100);
    HAL_UART_Transmit(GPS_UART, (uint8_t *)message, message_length, 100);
}

void configure_gps() {
    // Configurer UART1 pour 115200 bauds
    const char uart_config[] = {0x06, 0x00, 0x14, 0x00, 0x01, 0x00, 0x00, 0x00, 0xD0, 0x08, 0x00, 0x00, 0x00, 0xC2, 0x01, 0x00, 0x07, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00};
    ublox_send_message(uart_config,sizeof(uart_config));

    // Activer les trames NMEA GNGGA et GNVTG pour UART1 et USB
    const char gngga_config[] = {0x06, 0x01, 0x08, 0x00, 0xF0, 0x00, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01};
    ublox_send_message(gngga_config,sizeof(uart_config));

    const char gnvtg_config[] = {0x06, 0x01, 0x08, 0x00, 0xF0, 0x05, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01};
    ublox_send_message(gnvtg_config,sizeof(uart_config));

    // Configurer la fréquence des trames GNGGA et GNVTG pour 1 Hz
    const char rate_config[] = {0x06, 0x08, 0x06, 0x00, 0xE8, 0x03, 0x01, 0x00, 0x01, 0x00};
    ublox_send_message(rate_config,sizeof(uart_config));

    // Désactiver les trames NMEA GQGSV pour UART1 et USB
    const char gqgsv_disable[] = {0x06, 0x01, 0x08, 0x00, 0xF0, 0x03, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
    ublox_send_message(gqgsv_disable,sizeof(uart_config));

    const uint8_t gngll_disable[] = {0x06, 0x01, 0x08, 0x00, 0xF0, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00};
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

	gpsHandle = osThreadNew(gpsTask, NULL, &gps_attributes);
}
