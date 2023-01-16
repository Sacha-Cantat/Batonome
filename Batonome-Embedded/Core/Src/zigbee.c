/*
 * zigbee.c
 *
 *  Created on: 10 janv. 2023
 *      Author: scant
 */

#include "zigbee.h"

#include "cmsis_os.h"
#include "main.h"


void ZigbeeComTask(void *argument);
void zigbee_Init();



void ZigbeeComTask(void *argument)
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

	zigbeeComHandle = osThreadNew(ZigbeeComTask, NULL, &zigbee_com_attributes);
}





