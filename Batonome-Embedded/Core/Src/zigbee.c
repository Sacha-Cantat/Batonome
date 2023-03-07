/*
 * zigbee.c
 *
 *  Created on: 10 janv. 2023
 *      Author: scant
 */

#include "zigbee.h"

#include "cmsis_os.h"
#include "main.h"
#include "gestionPWM.h"
#include "string.h"

#define SIZE_LONG_DOUBLE 8



void ZigbeeComTask(void *argument);
void zigbee_Init();

uint8_t rxBuffer[RX_BUFFER_SIZE];

uint8_t received_data[10];

uint8_t data[2000];

//void HAL_UART_TxCpltCallback(UART_HandleTypeDef *huart)
//{
//	if (huart->Instance == USART1) {
//		zigbeeTxCpltCallback();
//	}
//}



void sendBatonomeData(void) {
   uint8_t buffer[sizeof(batonomeData)];
   uint8_t* structPtr = (uint8_t*) &batonomeData;
   for (int i =0 ; i<sizeof(batonomeData);i++)
   {
	  buffer[i]= *structPtr++;

   }
   HAL_UART_Transmit(&huart1, buffer, sizeof(buffer), HAL_MAX_DELAY);
}

void receiveConf()
{
	//Request for conf
	if (UART1_rxBuffer[1] == '0')
	{
		//Send ACK ready to receive
		//HAL_UART_Transmit(&huart1, (uint8_t*) 0x41, sizeof(0x41), HAL_MAX_DELAY);
		//receive balise data
		memcpy(&batonomeDataConf.balise.latitude,&UART1_rxBuffer[8],SIZE_LONG_DOUBLE);
		memcpy(&batonomeDataConf.balise.longitude,&UART1_rxBuffer[16],SIZE_LONG_DOUBLE);
		int i = 0;

		//On va enregristrer 20 coordonés GPS de perimetre de navigation
		memcpy(&batonomeDataConf.perimetreNav,&UART1_rxBuffer[24],SIZE_LONG_DOUBLE*20);




		//REceive coordo GPS


		//Ready to receive 1 byte +1 byte + 2 byte + 40byte
	}

	if (UART1_rxBuffer[1] == '1')
	{
		//memcpy(&batonomeConf.balise[0],)

		//Send ACK ready to receive
		//HAL_UART_Transmit(&huart1, 43, sizeof(43), HAL_MAX_DELAY);

		//Ready to receive 1 byte +1 byte + 2 byte + 40byte
		HAL_UART_Receive_IT(&huart1, UART1_rxBuffer, 3);
	}



}
void batonomeControl(enum key_pressed key)
{
	if (key == RIGHT)
		{
			if (deriveState.directionDerive==TRIBORD && deriveState.forceDerive < 4 )
			{
				deriveToSet.forceDerive = deriveState.forceDerive+1;
			}
			else if(deriveState.directionDerive==BABORD && deriveState.forceDerive > 0)
			{
				deriveToSet.forceDerive = deriveState.forceDerive-1;
				deriveToSet.directionDerive = TRIBORD;
				deriveToSet.forceDerive = POWER_0;
			}
			else if(deriveState.directionDerive==AVANT)
			{
				deriveToSet.directionDerive = TRIBORD;
				deriveToSet.forceDerive = POWER_0;
			}
			setCommandBato(REQUEST_COMMAND_DERIVE);
		}
	else if (key == LEFT)
		{
		if (deriveState.directionDerive==BABORD && deriveState.forceDerive < 4 )
		{
			deriveToSet.forceDerive = deriveState.forceDerive+1;
		}
		else if(deriveState.directionDerive==TRIBORD && deriveState.forceDerive > 0)
		{
			deriveToSet.forceDerive = deriveState.forceDerive-1;
			deriveToSet.directionDerive = TRIBORD;
			deriveToSet.forceDerive = POWER_0;
		}
		else if(deriveState.directionDerive==AVANT)
		{
			deriveToSet.directionDerive = BABORD;
			deriveToSet.forceDerive = POWER_0;
		}
		setCommandBato(REQUEST_COMMAND_DERIVE);

		}
	else if (key == SPACE)
			{
				deriveToSet.directionDerive = AVANT;
				deriveToSet.forceDerive = POWER_0;
			}
			setCommandBato(REQUEST_COMMAND_DERIVE);
}

void processData(int sizeData)
{
	if (UART1_rxBuffer[0] == 'A')
		{
			//HAL_UART_Transmit(&huart1, UART1_txBuffer, 1, 100);
			sendBatonomeData();

			//HAL_UART_Receive_IT (&huart1, UART1_rxBuffer, 2);
		}
		else if(UART1_rxBuffer[0]== 'B')
		{
			receiveConf();
			//HAL_UART_Receive_IT (&huart1, UART1_rxBuffer, 2);
		}

		else if(UART1_rxBuffer[0]== 'C') //Touche RIGHT ou LEFT
		{
			if (UART1_rxBuffer[1]== '0')
			{
				batonomeControl(RIGHT);
			}

			if (UART1_rxBuffer[1]== '1')
			{
				batonomeControl(LEFT);
			}

			if (UART1_rxBuffer[1]== '2')
			{
				batonomeControl(SPACE);
			}

			//HAL_UART_Receive_IT (&huart1, UART1_rxBuffer, 2);
		}
		else if(UART1_rxBuffer[0]== 'D') //Touche UP ou DOWN
		{
			if (UART1_rxBuffer[1]== '0')
			{
				batonomeControl(UP);
			}

			if (UART1_rxBuffer[1]== '1')
			{
				batonomeControl(DOWN);
			}
		}

}


void zigbeeTxCpltCallback(){
	static int indexRxBuffer = 0;

	if (rxData != '\n')
	{
		UART1_rxBuffer[indexRxBuffer] = rxData;
		indexRxBuffer++;
	}
	else if (rxData == '\n')
	{
		processData(indexRxBuffer);
		//RAZ Buffer
		for (int i = 0 ; i<RX_BUFFER_SIZE;i++)
		{
			UART1_rxBuffer[i]=0;
		}
		indexRxBuffer = 0;


	}
	HAL_UART_Receive_IT (&huart1, &rxData, 1);

}



//
//	static uint16_t rxBufferIndex = 0;
//
//	if(UART1_rxBuffer[0] == 'C')
//	{
//		processData();
//		rxBufferIndex = 0;
//		//reset rxBuffer
//		memset(rxBuffer, 0, RX_BUFFER_SIZE);
//
//	}
//	else
//	{
//		rxBuffer[rxBufferIndex]=UART1_rxBuffer[0];
//		rxBufferIndex++;
//
//
//		if (rxBufferIndex >= RX_BUFFER_SIZE)
//		{
//			rxBufferIndex = 0;
//		}
//	}


//	HAL_UART_Receive_IT(&huart1, UART1_rxBuffer, 3);
	//else HAL_UART_Receive_IT(&huart1, UART1_rxBuffer, 1);







void ZigbeeComTask(void *argument)
{
  /* USER CODE BEGIN 5 */
  /* Infinite loop */
 received_data[0]= 0x05;
 batonomeData.positionGPS.latitude = 52.46184682371661;
 batonomeData.positionGPS.longitude = 53.46184682371661;
 batonomeData.angle = 320;
 batonomeData.autreInformation=3;
  for(;;)
  {


	  char data[] = "Hello World\r\n";

	  static int valstate = 1;
	  //osDelay(1000);
	  if(valstate)
	  {
		 /* deriveToSet.directionDerive=TRIBORD;
		  deriveToSet.forceDerive=FORCE_4;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);

		  deriveToSet.directionDerive=TRIBORD;
		  deriveToSet.forceDerive=FORCE_3;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);

		  deriveToSet.directionDerive=TRIBORD;
		  deriveToSet.forceDerive=FORCE_2;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);

		  deriveToSet.directionDerive=TRIBORD;
		  deriveToSet.forceDerive=FORCE_1;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);

		  deriveToSet.directionDerive=TRIBORD;
		  deriveToSet.forceDerive=FORCE_0;
		  setCommandBato(REQUEST_COMMAND_DERIVE);

		  osDelay(1000);


		  deriveToSet.directionDerive=AVANT;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);

		  deriveToSet.directionDerive=BABORD;
		  deriveToSet.forceDerive=FORCE_0;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);

		  deriveToSet.directionDerive=BABORD;
		  deriveToSet.forceDerive=FORCE_1;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);

		  deriveToSet.directionDerive=BABORD;
		  deriveToSet.forceDerive=FORCE_2;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);

		  deriveToSet.directionDerive=BABORD;
		  deriveToSet.forceDerive=FORCE_3;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);

		  deriveToSet.directionDerive=BABORD;
		  deriveToSet.forceDerive=FORCE_4;
		  setCommandBato(REQUEST_COMMAND_DERIVE);
		  osDelay(1000);*/




	  }
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
	  .stack_size = 256 * 4,
	  .priority = (osPriority_t) osPriorityHigh,
	};
	printf("Start task Zigbee \n");

	zigbeeComHandle = osThreadNew(ZigbeeComTask, NULL, &zigbee_com_attributes);


}





