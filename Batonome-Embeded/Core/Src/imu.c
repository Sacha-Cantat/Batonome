/*
 * imu.c
 *
 *  Created on: 10 janv. 2023
 *      Author: scant
 */


#include "imu.h"


#include "cmsis_os.h"
#include "main.h"

void ImuManagementTask()
{
	printf("IMU management task is launched\n");

	for(;;)
	  {
		//Code
	  }


}



void imu_Init()
{
	/* Definitions for zigbee_com */
	osThreadId_t imuHandle;
	const osThreadAttr_t imu_attributes = {
	  .name = "imu",
	  .stack_size = 128 * 4,
	  .priority = (osPriority_t) osPriorityNormal,
	};

	imuHandle = osThreadNew(ImuManagementTask, NULL, &imu_attributes);
}
