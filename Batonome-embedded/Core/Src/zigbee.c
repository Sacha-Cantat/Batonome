/*
 * zigbee.c
 *
 *  Created on: 5 janv. 2023
 *      Author: scant
 */

#include "zigbee.h"
#include "cmsis_os.h"
#include "main.h"


void StartZigbeeCom(void *argument);
void zigbee_Init();

void sendData(uint8_t *data, uint16_t size) {
    HAL_UART_Transmit(&huart1, data, size, 100);
}

void receiveData(uint8_t *data, uint16_t size) {
    HAL_UART_Receive(&huart1, data, size, 100);
}


void StartZigbeeCom(void *argument)
{
  /* USER CODE BEGIN 5 */
  /* Infinite loop */


  for(;;)
  {
//	  HAL_UART_Transmit(&huart1, "a", 1, 100);
	  //HAL_UART_Transmit(&huart1, received_data, 1, 100);

	
	


  }
  /* USER CODE END 5 */
}

void zigbee_Init()
{
	/* Definitions for zigbee_com */
	osThreadId_t zigbeeComHandle;
	const osThreadAttr_t zigbee_com_attributes = {
	  .name = "zigbee_com",
	  .stack_size = 128 * 4,
	  .priority = (osPriority_t) osPriorityNormal,
	};

	zigbeeComHandle = osThreadNew(StartZigbeeCom, NULL, &zigbee_com_attributes);
}




