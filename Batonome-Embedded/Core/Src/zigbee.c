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

uint8_t received_data[10];

uint8_t data[2000];

//void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
//{
//	if (huart->Instance == USART1) {
//		zigbeeTxCpltCallback();
//	}
//}






void zigbeeTxCpltCallback(){
	if (UART1_rxBuffer[0] == 52)
	{
		HAL_UART_Transmit(&huart1, UART1_txBuffer, 1, 100);
	}
	HAL_UART_Receive_IT(&huart1, UART1_rxBuffer, 1);
}

void ZigbeeComTask(void *argument)
{
  /* USER CODE BEGIN 5 */
  /* Infinite loop */
 received_data[0]= 0x05;

  for(;;)
  {
	  char data[] = "Hello World\r\n";
	 // HAL_UART_Transmit(&huart1, (uint8_t*)data, sizeof(data), HAL_MAX_DELAY);
	 // HAL_UART_Transmit_IT(&huart2, data, sizeof (data));

	  //osDelay(1000);
	  //printf("Send \n");





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
	  .priority = (osPriority_t) osPriorityHigh,
	};
	printf("Start task Zigbee \n");

	zigbeeComHandle = osThreadNew(ZigbeeComTask, NULL, &zigbee_com_attributes);
}





