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

void StartZigbeeCom(void *argument)
{
  /* USER CODE BEGIN 5 */
  /* Infinite loop */
  for(;;)
  {
    osDelay(1000);
    //HAL_UART_Transmit(&huart1, "Test", strlen("Test"), HAL_MAX_DELAY);
    //printf("Send Message");
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




